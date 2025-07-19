"""
RunbookExecutor - Execute AI Runbooks with MCP tool integration.

This module provides functionality to parse and execute security runbooks
from the AI Runbooks project, integrating with SuperClaude's command system
and MCP tools for automated security operations.
"""

from .parser import (
    RunbookParser,
    ParsedRunbook,
    RunbookMetadata,
    WorkflowStep,
    RunbookType,
    create_parser
)

from .mcp_mapper import (
    MCPMapper,
    MCPToolCall,
    MCPTool
)

from .executor import (
    RunbookExecutor,
    ExecutionContext,
    ExecutionResult,
    ExecutionStatus,
    StepStatus,
    StepResult,
    create_executor
)

from .validator import (
    RunbookValidator,
    ValidationResult,
    ValidationIssue,
    ValidationSeverity,
    ValidationCategory,
    create_validator
)

__all__ = [
    # Parser exports
    'RunbookParser',
    'ParsedRunbook',
    'RunbookMetadata',
    'WorkflowStep',
    'RunbookType',
    'create_parser',
    
    # MCP Mapper exports
    'MCPMapper',
    'MCPToolCall',
    'MCPTool',
    
    # Executor exports
    'RunbookExecutor',
    'ExecutionContext',
    'ExecutionResult',
    'ExecutionStatus',
    'StepStatus',
    'StepResult',
    'create_executor',
    
    # Validator exports
    'RunbookValidator',
    'ValidationResult',
    'ValidationIssue',
    'ValidationSeverity',
    'ValidationCategory',
    'create_validator'
]

# Version information
__version__ = '1.0.0'
__author__ = 'AI Runbooks Integration'