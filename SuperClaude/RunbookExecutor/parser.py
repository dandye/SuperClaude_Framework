"""
RunbookParser - Parse AI Runbooks markdown files into executable workflows.

This module handles parsing of security runbook markdown files from the rules_bank,
extracting metadata, workflow steps, and mapping actions to MCP tools.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class RunbookType(Enum):
    """Types of runbooks supported by the system."""
    TRIAGE = "triage"
    INVESTIGATION = "investigation"
    HUNT = "hunt"
    RESPONSE = "response"
    IRP = "irp"
    COMMON_STEP = "common_step"
    ENRICHMENT = "enrichment"


@dataclass
class RunbookMetadata:
    """Metadata extracted from runbook YAML frontmatter."""
    title: str
    type: RunbookType
    category: str
    status: str
    tags: List[str]
    severity_levels: Optional[List[str]] = None
    required_tools: Optional[List[str]] = None
    personas: Optional[List[str]] = None
    estimated_time: Optional[str] = None
    
    @classmethod
    def from_yaml(cls, yaml_data: Dict[str, Any]) -> 'RunbookMetadata':
        """Create RunbookMetadata from parsed YAML frontmatter."""
        return cls(
            title=yaml_data.get('title', 'Untitled'),
            type=RunbookType(yaml_data.get('type', 'triage')),
            category=yaml_data.get('category', 'general'),
            status=yaml_data.get('status', 'draft'),
            tags=yaml_data.get('tags', []),
            severity_levels=yaml_data.get('severity_levels'),
            required_tools=yaml_data.get('required_tools'),
            personas=yaml_data.get('personas'),
            estimated_time=yaml_data.get('estimated_time')
        )


@dataclass
class WorkflowStep:
    """Individual step in a runbook workflow."""
    number: int
    title: str
    description: str
    actions: List[str]
    tools: List[str]
    decision_points: Optional[List[Dict[str, Any]]] = None
    output: Optional[str] = None
    
    def has_decisions(self) -> bool:
        """Check if this step contains decision points."""
        return bool(self.decision_points)


@dataclass
class ParsedRunbook:
    """Complete parsed runbook with metadata and workflow."""
    metadata: RunbookMetadata
    objective: str
    scope: str
    inputs: Dict[str, str]
    tools: List[str]
    workflow_steps: List[WorkflowStep]
    completion_criteria: List[str]
    related_runbooks: Optional[List[str]] = None
    
    def get_all_tools(self) -> List[str]:
        """Get comprehensive list of all tools used in the runbook."""
        tools = set(self.tools)
        for step in self.workflow_steps:
            tools.update(step.tools)
        if self.metadata.required_tools:
            tools.update(self.metadata.required_tools)
        return sorted(list(tools))


class RunbookParser:
    """Parser for AI Runbooks markdown files."""
    
    def __init__(self, rules_bank_path: Path):
        """Initialize parser with path to rules_bank directory."""
        self.rules_bank_path = Path(rules_bank_path)
        self.runbooks_path = self.rules_bank_path / "run_books"
        
    def parse_runbook(self, runbook_path: str) -> ParsedRunbook:
        """Parse a runbook markdown file into structured data."""
        full_path = self._resolve_path(runbook_path)
        content = full_path.read_text()
        
        # Extract frontmatter and content
        frontmatter, markdown_content = self._extract_frontmatter(content)
        metadata = RunbookMetadata.from_yaml(frontmatter)
        
        # Parse sections
        sections = self._parse_sections(markdown_content)
        
        # Extract workflow steps
        workflow_steps = self._parse_workflow_steps(sections.get('Workflow', ''))
        
        return ParsedRunbook(
            metadata=metadata,
            objective=sections.get('Objective', ''),
            scope=sections.get('Scope', ''),
            inputs=self._parse_inputs(sections.get('Inputs', '')),
            tools=self._parse_tools(sections.get('Tools Required', '')),
            workflow_steps=workflow_steps,
            completion_criteria=self._parse_list_section(sections.get('Completion Criteria', '')),
            related_runbooks=self._parse_list_section(sections.get('Related Runbooks', ''))
        )
    
    def _resolve_path(self, runbook_path: str) -> Path:
        """Resolve runbook path relative to rules_bank."""
        if runbook_path.startswith('/'):
            return Path(runbook_path)
        
        # Check common locations
        possible_paths = [
            self.runbooks_path / runbook_path,
            self.runbooks_path / "common_steps" / runbook_path,
            self.runbooks_path / "irps" / runbook_path,
            self.rules_bank_path / runbook_path
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
                
        raise FileNotFoundError(f"Runbook not found: {runbook_path}")
    
    def _extract_frontmatter(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and remaining content."""
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            yaml_content = match.group(1)
            markdown_content = match.group(2)
            frontmatter = yaml.safe_load(yaml_content) or {}
        else:
            frontmatter = {}
            markdown_content = content
            
        return frontmatter, markdown_content
    
    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown sections into dictionary."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
            
        return sections
    
    def _parse_workflow_steps(self, workflow_content: str) -> List[WorkflowStep]:
        """Parse workflow section into structured steps."""
        steps = []
        current_step = None
        
        for line in workflow_content.split('\n'):
            # Match step headers like "### 1. Initial Triage"
            step_match = re.match(r'^###\s+(\d+)\.\s+(.+)$', line)
            if step_match:
                if current_step:
                    steps.append(self._finalize_step(current_step))
                current_step = {
                    'number': int(step_match.group(1)),
                    'title': step_match.group(2),
                    'content': []
                }
            elif current_step:
                current_step['content'].append(line)
        
        if current_step:
            steps.append(self._finalize_step(current_step))
            
        return steps
    
    def _finalize_step(self, step_data: Dict) -> WorkflowStep:
        """Convert raw step data into WorkflowStep object."""
        content = '\n'.join(step_data['content']).strip()
        
        # Extract components from content
        description_lines = []
        actions = []
        tools = []
        decision_points = []
        output = None
        
        in_actions = False
        in_tools = False
        in_decisions = False
        
        for line in content.split('\n'):
            if line.startswith('**Actions:**'):
                in_actions = True
                in_tools = False
                in_decisions = False
            elif line.startswith('**Tools:**'):
                in_actions = False
                in_tools = True
                in_decisions = False
            elif line.startswith('**Decision Points:**'):
                in_actions = False
                in_tools = False
                in_decisions = True
            elif line.startswith('**Output:**'):
                output = line.replace('**Output:**', '').strip()
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                item = line.strip()[2:]
                if in_actions:
                    actions.append(item)
                elif in_tools:
                    tools.append(self._extract_tool_name(item))
                elif in_decisions:
                    decision_points.append(self._parse_decision_point(item))
            elif not in_actions and not in_tools and not in_decisions:
                description_lines.append(line)
        
        return WorkflowStep(
            number=step_data['number'],
            title=step_data['title'],
            description='\n'.join(description_lines).strip(),
            actions=actions,
            tools=tools,
            decision_points=decision_points if decision_points else None,
            output=output
        )
    
    def _extract_tool_name(self, tool_line: str) -> str:
        """Extract tool name from tool line."""
        # Handle format like "`chronicle_mcp` - Query SIEM"
        if '`' in tool_line:
            match = re.search(r'`([^`]+)`', tool_line)
            if match:
                return match.group(1)
        return tool_line.split(' - ')[0].strip()
    
    def _parse_decision_point(self, decision_line: str) -> Dict[str, Any]:
        """Parse a decision point line."""
        # Handle format like "If true positive → Escalate to Tier 2"
        if '→' in decision_line:
            condition, action = decision_line.split('→', 1)
            return {
                'condition': condition.strip(),
                'action': action.strip()
            }
        return {'raw': decision_line}
    
    def _parse_inputs(self, inputs_content: str) -> Dict[str, str]:
        """Parse inputs section into dictionary."""
        inputs = {}
        for line in inputs_content.split('\n'):
            if line.strip().startswith('- '):
                # Handle format like "- Alert ID: Unique identifier"
                parts = line[2:].split(':', 1)
                if len(parts) == 2:
                    inputs[parts[0].strip()] = parts[1].strip()
        return inputs
    
    def _parse_tools(self, tools_content: str) -> List[str]:
        """Parse tools section into list."""
        tools = []
        for line in tools_content.split('\n'):
            if line.strip().startswith('- '):
                tool = self._extract_tool_name(line[2:])
                if tool:
                    tools.append(tool)
        return tools
    
    def _parse_list_section(self, content: str) -> Optional[List[str]]:
        """Parse a section containing a list of items."""
        if not content.strip():
            return None
            
        items = []
        for line in content.split('\n'):
            if line.strip().startswith('- '):
                items.append(line[2:].strip())
        return items if items else None


def create_parser(rules_bank_path: str = "/Users/dandye/Projects/dandye_ai_runbooks__worktree__super_claude/rules_bank") -> RunbookParser:
    """Factory function to create a RunbookParser instance."""
    return RunbookParser(Path(rules_bank_path))