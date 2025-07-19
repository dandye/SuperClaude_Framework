"""
RunbookExecutor - Execute parsed runbook workflows with MCP tool integration.

This module handles the execution of security runbooks by coordinating
MCP tools, managing workflow state, and handling decision points.
"""

from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

from .parser import ParsedRunbook, WorkflowStep, RunbookType
from .mcp_mapper import MCPMapper, MCPToolCall


class ExecutionStatus(Enum):
    """Status of runbook execution."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class StepStatus(Enum):
    """Status of individual workflow steps."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


@dataclass
class StepResult:
    """Result from executing a workflow step."""
    step_number: int
    status: StepStatus
    outputs: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    decisions_made: Dict[str, str] = field(default_factory=dict)
    duration_seconds: Optional[float] = None
    
    def is_successful(self) -> bool:
        """Check if step executed successfully."""
        return self.status == StepStatus.COMPLETED


@dataclass
class ExecutionContext:
    """Context maintained throughout runbook execution."""
    runbook_name: str
    case_id: Optional[str] = None
    severity: Optional[str] = None
    persona: Optional[str] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    facts: Dict[str, Any] = field(default_factory=dict)
    decisions: Dict[str, str] = field(default_factory=dict)
    iocs: List[Dict[str, str]] = field(default_factory=list)
    
    def add_fact(self, key: str, value: Any):
        """Add a discovered fact to context."""
        self.facts[key] = value
    
    def add_ioc(self, ioc_type: str, value: str, context: str = ""):
        """Add an IOC to the context."""
        self.iocs.append({
            "type": ioc_type,
            "value": value,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def make_decision(self, decision_point: str, choice: str):
        """Record a decision made during execution."""
        self.decisions[decision_point] = choice


@dataclass
class ExecutionResult:
    """Complete result from runbook execution."""
    runbook: ParsedRunbook
    status: ExecutionStatus
    context: ExecutionContext
    step_results: List[StepResult]
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    
    def get_duration(self) -> Optional[float]:
        """Get total execution duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def get_successful_steps(self) -> List[StepResult]:
        """Get list of successfully completed steps."""
        return [r for r in self.step_results if r.is_successful()]
    
    def to_report(self) -> Dict[str, Any]:
        """Generate execution report."""
        return {
            "runbook": self.runbook.metadata.title,
            "type": self.runbook.metadata.type.value,
            "status": self.status.value,
            "duration_seconds": self.get_duration(),
            "steps_completed": len(self.get_successful_steps()),
            "total_steps": len(self.runbook.workflow_steps),
            "context": {
                "case_id": self.context.case_id,
                "severity": self.context.severity,
                "persona": self.context.persona
            },
            "facts_discovered": self.context.facts,
            "decisions_made": self.context.decisions,
            "iocs_found": self.context.iocs,
            "errors": [r.errors for r in self.step_results if r.errors]
        }


class RunbookExecutor:
    """Execute parsed runbooks with MCP tool coordination."""
    
    def __init__(self, mcp_mapper: MCPMapper, 
                 tool_executor: Optional[Callable[[MCPToolCall], Dict[str, Any]]] = None):
        """
        Initialize executor with MCP mapper and tool executor.
        
        Args:
            mcp_mapper: Mapper for converting actions to MCP tool calls
            tool_executor: Function to execute MCP tool calls (for testing/mocking)
        """
        self.mcp_mapper = mcp_mapper
        self.tool_executor = tool_executor or self._default_tool_executor
        self.execution_hooks: Dict[str, List[Callable]] = {
            'pre_step': [],
            'post_step': [],
            'on_decision': [],
            'on_error': []
        }
    
    def execute(self, runbook: ParsedRunbook, context: Optional[ExecutionContext] = None,
                dry_run: bool = False) -> ExecutionResult:
        """
        Execute a parsed runbook.
        
        Args:
            runbook: Parsed runbook to execute
            context: Initial execution context
            dry_run: If True, simulate execution without calling tools
            
        Returns:
            ExecutionResult with complete execution details
        """
        # Initialize context if not provided
        if context is None:
            context = ExecutionContext(runbook_name=runbook.metadata.title)
        
        # Create execution result
        result = ExecutionResult(
            runbook=runbook,
            status=ExecutionStatus.RUNNING,
            context=context,
            step_results=[],
            start_time=datetime.utcnow()
        )
        
        try:
            # Execute each workflow step
            for step in runbook.workflow_steps:
                step_result = self._execute_step(step, context, dry_run)
                result.step_results.append(step_result)
                
                # Handle step failure
                if not step_result.is_successful():
                    result.status = ExecutionStatus.FAILED
                    result.error_message = f"Step {step.number} failed"
                    break
                
                # Handle decision points
                if step.has_decisions() and step_result.decisions_made:
                    # Check if any decision leads to early termination
                    for decision, choice in step_result.decisions_made.items():
                        if self._should_terminate(choice):
                            result.status = ExecutionStatus.COMPLETED
                            result.end_time = datetime.utcnow()
                            return result
            
            # All steps completed successfully
            if result.status == ExecutionStatus.RUNNING:
                result.status = ExecutionStatus.COMPLETED
                
        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error_message = str(e)
        
        result.end_time = datetime.utcnow()
        return result
    
    def _execute_step(self, step: WorkflowStep, context: ExecutionContext, 
                      dry_run: bool = False) -> StepResult:
        """Execute a single workflow step."""
        start_time = datetime.utcnow()
        step_result = StepResult(
            step_number=step.number,
            status=StepStatus.RUNNING
        )
        
        # Run pre-step hooks
        for hook in self.execution_hooks['pre_step']:
            hook(step, context)
        
        try:
            # Execute each action in the step
            for action in step.actions:
                # Map action to MCP tool call
                tool_calls = self.mcp_mapper.map_action(action, context)
                
                for tool_call in tool_calls:
                    if dry_run:
                        # Simulate tool execution
                        tool_result = {
                            "tool": tool_call.tool,
                            "operation": tool_call.operation,
                            "simulated": True,
                            "status": "success"
                        }
                    else:
                        # Execute actual tool call
                        tool_result = self.tool_executor(tool_call)
                    
                    step_result.tool_results.append(tool_result)
                    
                    # Process tool results
                    self._process_tool_result(tool_result, context)
            
            # Handle decision points
            if step.has_decisions():
                for decision_point in step.decision_points:
                    decision = self._evaluate_decision(decision_point, context)
                    step_result.decisions_made[decision_point['condition']] = decision
                    context.make_decision(decision_point['condition'], decision)
                    
                    # Run decision hooks
                    for hook in self.execution_hooks['on_decision']:
                        hook(decision_point, decision, context)
            
            # Mark step as completed
            step_result.status = StepStatus.COMPLETED
            
        except Exception as e:
            step_result.status = StepStatus.FAILED
            step_result.errors.append(str(e))
            
            # Run error hooks
            for hook in self.execution_hooks['on_error']:
                hook(step, e, context)
        
        # Calculate duration
        step_result.duration_seconds = (datetime.utcnow() - start_time).total_seconds()
        
        # Run post-step hooks
        for hook in self.execution_hooks['post_step']:
            hook(step, step_result, context)
        
        return step_result
    
    def _default_tool_executor(self, tool_call: MCPToolCall) -> Dict[str, Any]:
        """Default tool executor - placeholder for actual MCP integration."""
        # This would be replaced with actual MCP tool execution
        return {
            "tool": tool_call.tool,
            "operation": tool_call.operation,
            "parameters": tool_call.parameters,
            "status": "simulated",
            "message": "Tool execution not implemented - override tool_executor"
        }
    
    def _process_tool_result(self, tool_result: Dict[str, Any], context: ExecutionContext):
        """Process results from tool execution and update context."""
        # Extract relevant information based on tool type
        tool_name = tool_result.get('tool', '')
        
        if tool_name == 'chronicle_mcp':
            # Process SIEM query results
            if 'events' in tool_result:
                context.add_fact('siem_event_count', len(tool_result['events']))
                for event in tool_result.get('events', []):
                    # Extract IOCs from events
                    if 'source_ip' in event:
                        context.add_ioc('ip', event['source_ip'], 'SIEM event')
                    if 'destination_domain' in event:
                        context.add_ioc('domain', event['destination_domain'], 'SIEM event')
        
        elif tool_name == 'gti_mcp':
            # Process threat intelligence results
            if 'reputation' in tool_result:
                context.add_fact('threat_reputation', tool_result['reputation'])
            if 'threat_actor' in tool_result:
                context.add_fact('attributed_actor', tool_result['threat_actor'])
        
        elif tool_name == 'soar_mcp':
            # Process SOAR automation results
            if 'case_created' in tool_result:
                context.outputs['case_id'] = tool_result['case_id']
            if 'containment_status' in tool_result:
                context.add_fact('containment_completed', tool_result['containment_status'])
    
    def _evaluate_decision(self, decision_point: Dict[str, Any], 
                          context: ExecutionContext) -> str:
        """Evaluate a decision point based on context."""
        condition = decision_point.get('condition', '')
        
        # Simple decision evaluation based on context facts
        if 'true positive' in condition.lower():
            # Check if we have evidence of true positive
            reputation = context.facts.get('threat_reputation', {})
            if isinstance(reputation, dict) and reputation.get('malicious', False):
                return decision_point.get('action', 'Escalate')
        
        elif 'false positive' in condition.lower():
            # Check if we have evidence of false positive
            event_count = context.facts.get('siem_event_count', 0)
            if event_count == 0:
                return decision_point.get('action', 'Close alert')
        
        # Default action if no specific condition matches
        return decision_point.get('action', 'Continue investigation')
    
    def _should_terminate(self, decision: str) -> bool:
        """Check if a decision should terminate execution."""
        termination_keywords = ['close', 'terminate', 'complete', 'resolved']
        return any(keyword in decision.lower() for keyword in termination_keywords)
    
    def add_hook(self, hook_type: str, hook_function: Callable):
        """Add execution hook for monitoring and extension."""
        if hook_type in self.execution_hooks:
            self.execution_hooks[hook_type].append(hook_function)
    
    def validate_runbook(self, runbook: ParsedRunbook) -> List[str]:
        """Validate runbook before execution."""
        issues = []
        
        # Check required tools are available
        for tool in runbook.get_all_tools():
            if not self.mcp_mapper.is_tool_available(tool):
                issues.append(f"Required tool not available: {tool}")
        
        # Check workflow steps are properly numbered
        expected_numbers = list(range(1, len(runbook.workflow_steps) + 1))
        actual_numbers = [step.number for step in runbook.workflow_steps]
        if actual_numbers != expected_numbers:
            issues.append("Workflow steps are not consecutively numbered")
        
        # Validate metadata
        if not runbook.metadata.title:
            issues.append("Runbook missing title")
        if runbook.metadata.status == "draft":
            issues.append("Runbook is still in draft status")
        
        return issues


def create_executor() -> RunbookExecutor:
    """Factory function to create a RunbookExecutor instance."""
    mcp_mapper = MCPMapper()
    return RunbookExecutor(mcp_mapper)