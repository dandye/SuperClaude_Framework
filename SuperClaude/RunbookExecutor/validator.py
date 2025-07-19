"""
RunbookValidator - Validate runbook execution results and quality.

This module handles validation of runbook execution results,
ensuring quality standards and completeness of security operations.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

from .executor import ExecutionResult, ExecutionStatus, StepStatus
from .parser import RunbookType


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationCategory(Enum):
    """Categories of validation checks."""
    COMPLETENESS = "completeness"
    QUALITY = "quality"
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPLIANCE = "compliance"


@dataclass
class ValidationIssue:
    """Individual validation issue found."""
    category: ValidationCategory
    severity: ValidationSeverity
    message: str
    step_number: Optional[int] = None
    recommendation: Optional[str] = None
    
    def is_blocking(self) -> bool:
        """Check if this issue should block completion."""
        return self.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]


@dataclass
class ValidationResult:
    """Complete validation result for runbook execution."""
    execution_result: ExecutionResult
    issues: List[ValidationIssue]
    score: float  # 0.0 to 1.0
    passed: bool
    validation_time: datetime
    
    def get_issues_by_severity(self, severity: ValidationSeverity) -> List[ValidationIssue]:
        """Get all issues of specific severity."""
        return [i for i in self.issues if i.severity == severity]
    
    def get_blocking_issues(self) -> List[ValidationIssue]:
        """Get all blocking issues."""
        return [i for i in self.issues if i.is_blocking()]
    
    def to_report(self) -> Dict[str, Any]:
        """Generate validation report."""
        return {
            "runbook": self.execution_result.runbook.metadata.title,
            "validation_passed": self.passed,
            "score": self.score,
            "total_issues": len(self.issues),
            "blocking_issues": len(self.get_blocking_issues()),
            "issues_by_severity": {
                severity.value: len(self.get_issues_by_severity(severity))
                for severity in ValidationSeverity
            },
            "issues_by_category": {
                category.value: len([i for i in self.issues if i.category == category])
                for category in ValidationCategory
            },
            "timestamp": self.validation_time.isoformat()
        }


class RunbookValidator:
    """Validate runbook execution results."""
    
    def __init__(self):
        """Initialize validator with default thresholds."""
        self.thresholds = {
            'min_completion_rate': 0.8,  # 80% of steps must complete
            'max_error_rate': 0.1,  # Max 10% steps can fail
            'max_duration_multiplier': 2.0,  # Max 2x estimated time
            'min_evidence_collection': 0.7,  # 70% of expected evidence
            'required_tool_success_rate': 0.9  # 90% tool calls must succeed
        }
        
        # Expected execution times by runbook type (in minutes)
        self.expected_durations = {
            RunbookType.TRIAGE: 15,
            RunbookType.INVESTIGATION: 60,
            RunbookType.HUNT: 120,
            RunbookType.RESPONSE: 30,
            RunbookType.ENRICHMENT: 5
        }
    
    def validate(self, execution_result: ExecutionResult) -> ValidationResult:
        """
        Validate a runbook execution result.
        
        Args:
            execution_result: Result from runbook execution
            
        Returns:
            ValidationResult with issues and score
        """
        issues = []
        
        # Run all validation checks
        issues.extend(self._validate_completeness(execution_result))
        issues.extend(self._validate_quality(execution_result))
        issues.extend(self._validate_performance(execution_result))
        issues.extend(self._validate_security(execution_result))
        issues.extend(self._validate_compliance(execution_result))
        
        # Calculate overall score
        score = self._calculate_score(execution_result, issues)
        
        # Determine if validation passed
        blocking_issues = [i for i in issues if i.is_blocking()]
        passed = len(blocking_issues) == 0 and score >= 0.7
        
        return ValidationResult(
            execution_result=execution_result,
            issues=issues,
            score=score,
            passed=passed,
            validation_time=datetime.utcnow()
        )
    
    def _validate_completeness(self, result: ExecutionResult) -> List[ValidationIssue]:
        """Validate execution completeness."""
        issues = []
        
        # Check execution status
        if result.status != ExecutionStatus.COMPLETED:
            issues.append(ValidationIssue(
                category=ValidationCategory.COMPLETENESS,
                severity=ValidationSeverity.ERROR,
                message=f"Execution did not complete successfully: {result.status.value}",
                recommendation="Investigate failure reason and retry execution"
            ))
        
        # Check step completion rate
        total_steps = len(result.runbook.workflow_steps)
        completed_steps = len(result.get_successful_steps())
        completion_rate = completed_steps / total_steps if total_steps > 0 else 0
        
        if completion_rate < self.thresholds['min_completion_rate']:
            issues.append(ValidationIssue(
                category=ValidationCategory.COMPLETENESS,
                severity=ValidationSeverity.ERROR,
                message=f"Low step completion rate: {completion_rate:.1%} (minimum: {self.thresholds['min_completion_rate']:.1%})",
                recommendation="Review failed steps and ensure all critical steps completed"
            ))
        
        # Check for required outputs
        if result.runbook.metadata.type == RunbookType.TRIAGE:
            if not result.context.decisions:
                issues.append(ValidationIssue(
                    category=ValidationCategory.COMPLETENESS,
                    severity=ValidationSeverity.WARNING,
                    message="No triage decisions recorded",
                    recommendation="Ensure triage decision (true/false positive) is documented"
                ))
        
        elif result.runbook.metadata.type == RunbookType.INVESTIGATION:
            if not result.context.facts:
                issues.append(ValidationIssue(
                    category=ValidationCategory.COMPLETENESS,
                    severity=ValidationSeverity.WARNING,
                    message="No investigation facts discovered",
                    recommendation="Ensure investigation findings are properly recorded"
                ))
        
        # Check for IOC collection
        if result.runbook.metadata.type in [RunbookType.INVESTIGATION, RunbookType.HUNT]:
            if not result.context.iocs:
                issues.append(ValidationIssue(
                    category=ValidationCategory.COMPLETENESS,
                    severity=ValidationSeverity.INFO,
                    message="No IOCs collected during execution",
                    recommendation="Consider if IOCs should have been found"
                ))
        
        return issues
    
    def _validate_quality(self, result: ExecutionResult) -> List[ValidationIssue]:
        """Validate execution quality."""
        issues = []
        
        # Check error rate
        failed_steps = [r for r in result.step_results if r.status == StepStatus.FAILED]
        error_rate = len(failed_steps) / len(result.step_results) if result.step_results else 0
        
        if error_rate > self.thresholds['max_error_rate']:
            issues.append(ValidationIssue(
                category=ValidationCategory.QUALITY,
                severity=ValidationSeverity.ERROR,
                message=f"High error rate: {error_rate:.1%} (maximum: {self.thresholds['max_error_rate']:.1%})",
                recommendation="Review error messages and improve error handling"
            ))
        
        # Check tool execution success
        total_tool_calls = sum(len(r.tool_results) for r in result.step_results)
        successful_tools = sum(
            1 for r in result.step_results 
            for tool in r.tool_results 
            if tool.get('status') in ['success', 'simulated']
        )
        
        if total_tool_calls > 0:
            tool_success_rate = successful_tools / total_tool_calls
            if tool_success_rate < self.thresholds['required_tool_success_rate']:
                issues.append(ValidationIssue(
                    category=ValidationCategory.QUALITY,
                    severity=ValidationSeverity.WARNING,
                    message=f"Low tool success rate: {tool_success_rate:.1%}",
                    recommendation="Check MCP tool connectivity and permissions"
                ))
        
        # Check evidence quality for investigations
        if result.runbook.metadata.type == RunbookType.INVESTIGATION:
            evidence_score = self._calculate_evidence_score(result.context)
            if evidence_score < self.thresholds['min_evidence_collection']:
                issues.append(ValidationIssue(
                    category=ValidationCategory.QUALITY,
                    severity=ValidationSeverity.WARNING,
                    message=f"Insufficient evidence collected: {evidence_score:.1%}",
                    recommendation="Ensure all data sources are queried comprehensively"
                ))
        
        return issues
    
    def _validate_performance(self, result: ExecutionResult) -> List[ValidationIssue]:
        """Validate execution performance."""
        issues = []
        
        # Check execution duration
        if result.get_duration():
            duration_minutes = result.get_duration() / 60
            expected_duration = self.expected_durations.get(
                result.runbook.metadata.type, 
                30  # Default 30 minutes
            )
            
            if duration_minutes > expected_duration * self.thresholds['max_duration_multiplier']:
                issues.append(ValidationIssue(
                    category=ValidationCategory.PERFORMANCE,
                    severity=ValidationSeverity.WARNING,
                    message=f"Execution took {duration_minutes:.1f} minutes (expected: {expected_duration} minutes)",
                    recommendation="Review slow steps and optimize queries"
                ))
        
        # Check for slow steps
        for step_result in result.step_results:
            if step_result.duration_seconds and step_result.duration_seconds > 300:  # 5 minutes
                issues.append(ValidationIssue(
                    category=ValidationCategory.PERFORMANCE,
                    severity=ValidationSeverity.INFO,
                    message=f"Step {step_result.step_number} took {step_result.duration_seconds:.1f} seconds",
                    step_number=step_result.step_number,
                    recommendation="Consider optimizing this step or running in parallel"
                ))
        
        return issues
    
    def _validate_security(self, result: ExecutionResult) -> List[ValidationIssue]:
        """Validate security aspects of execution."""
        issues = []
        
        # Check for sensitive data exposure
        sensitive_patterns = ['password', 'secret', 'key', 'token', 'credential']
        for step_result in result.step_results:
            for output_key, output_value in step_result.outputs.items():
                if any(pattern in output_key.lower() for pattern in sensitive_patterns):
                    issues.append(ValidationIssue(
                        category=ValidationCategory.SECURITY,
                        severity=ValidationSeverity.CRITICAL,
                        message=f"Potential sensitive data in output: {output_key}",
                        step_number=step_result.step_number,
                        recommendation="Remove or redact sensitive information from outputs"
                    ))
        
        # Check containment for critical incidents
        if (result.runbook.metadata.type == RunbookType.RESPONSE and 
            result.context.severity in ['critical', 'high']):
            if not any('containment' in str(r.outputs).lower() for r in result.step_results):
                issues.append(ValidationIssue(
                    category=ValidationCategory.SECURITY,
                    severity=ValidationSeverity.WARNING,
                    message="No containment actions recorded for critical incident",
                    recommendation="Ensure containment actions are properly executed and logged"
                ))
        
        return issues
    
    def _validate_compliance(self, result: ExecutionResult) -> List[ValidationIssue]:
        """Validate compliance requirements."""
        issues = []
        
        # Check case documentation
        if result.runbook.metadata.type in [RunbookType.INVESTIGATION, RunbookType.RESPONSE]:
            if not result.context.case_id:
                issues.append(ValidationIssue(
                    category=ValidationCategory.COMPLIANCE,
                    severity=ValidationSeverity.WARNING,
                    message="No case ID associated with execution",
                    recommendation="Ensure case is created in case management system"
                ))
        
        # Check decision documentation
        for step_result in result.step_results:
            if step_result.decisions_made and not step_result.outputs:
                issues.append(ValidationIssue(
                    category=ValidationCategory.COMPLIANCE,
                    severity=ValidationSeverity.INFO,
                    message=f"Step {step_result.step_number} made decisions without documenting rationale",
                    step_number=step_result.step_number,
                    recommendation="Document decision rationale for audit trail"
                ))
        
        return issues
    
    def _calculate_evidence_score(self, context: ExecutionContext) -> float:
        """Calculate evidence collection score."""
        score_components = {
            'has_facts': 0.3 if context.facts else 0.0,
            'has_iocs': 0.2 if context.iocs else 0.0,
            'has_timeline': 0.2 if any('time' in k.lower() for k in context.facts.keys()) else 0.0,
            'has_attribution': 0.15 if any('actor' in k.lower() for k in context.facts.keys()) else 0.0,
            'has_impact': 0.15 if any('impact' in k.lower() for k in context.facts.keys()) else 0.0
        }
        return sum(score_components.values())
    
    def _calculate_score(self, result: ExecutionResult, issues: List[ValidationIssue]) -> float:
        """Calculate overall validation score."""
        # Start with perfect score
        score = 1.0
        
        # Deduct for issues based on severity
        severity_weights = {
            ValidationSeverity.INFO: 0.02,
            ValidationSeverity.WARNING: 0.05,
            ValidationSeverity.ERROR: 0.15,
            ValidationSeverity.CRITICAL: 0.25
        }
        
        for issue in issues:
            score -= severity_weights.get(issue.severity, 0)
        
        # Bonus for complete execution
        if result.status == ExecutionStatus.COMPLETED:
            score += 0.1
        
        # Ensure score stays in valid range
        return max(0.0, min(1.0, score))
    
    def generate_recommendations(self, validation_result: ValidationResult) -> List[str]:
        """Generate actionable recommendations based on validation results."""
        recommendations = []
        
        # Group issues by category
        issues_by_category = {}
        for issue in validation_result.issues:
            if issue.category not in issues_by_category:
                issues_by_category[issue.category] = []
            issues_by_category[issue.category].append(issue)
        
        # Generate category-specific recommendations
        if ValidationCategory.COMPLETENESS in issues_by_category:
            recommendations.append(
                "Improve runbook completeness by ensuring all critical steps execute successfully"
            )
        
        if ValidationCategory.QUALITY in issues_by_category:
            recommendations.append(
                "Enhance execution quality through better error handling and tool integration"
            )
        
        if ValidationCategory.PERFORMANCE in issues_by_category:
            recommendations.append(
                "Optimize performance by parallelizing operations and improving query efficiency"
            )
        
        if ValidationCategory.SECURITY in issues_by_category:
            recommendations.append(
                "Review security practices and ensure sensitive data is properly handled"
            )
        
        if ValidationCategory.COMPLIANCE in issues_by_category:
            recommendations.append(
                "Strengthen compliance by improving documentation and audit trail"
            )
        
        return recommendations


def create_validator() -> RunbookValidator:
    """Factory function to create a RunbookValidator instance."""
    return RunbookValidator()