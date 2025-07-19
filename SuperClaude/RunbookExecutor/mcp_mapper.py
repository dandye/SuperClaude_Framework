"""
MCPMapper - Map runbook actions to MCP tool calls.

This module handles the translation of runbook action descriptions
into specific MCP tool calls with appropriate parameters.
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class MCPTool(Enum):
    """Available MCP tools for security operations."""
    CHRONICLE = "chronicle_mcp"
    GTI = "gti_mcp"
    SOAR = "soar_mcp"
    SCC = "scc_mcp"
    BIGQUERY = "bigquery_mcp"
    # SuperClaude tools
    CONTEXT7 = "Context7"
    SEQUENTIAL = "Sequential"
    MAGIC = "Magic"
    PLAYWRIGHT = "Playwright"


@dataclass
class MCPToolCall:
    """Represents a specific MCP tool call."""
    tool: str
    operation: str
    parameters: Dict[str, Any]
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "tool": self.tool,
            "operation": self.operation,
            "parameters": self.parameters,
            "description": self.description
        }


class ActionPattern:
    """Pattern for matching actions to MCP tools."""
    
    def __init__(self, pattern: str, tool: MCPTool, operation: str, 
                 param_extractor: Optional[callable] = None):
        """
        Initialize action pattern.
        
        Args:
            pattern: Regex pattern to match action text
            tool: MCP tool to use
            operation: Operation name for the tool
            param_extractor: Function to extract parameters from match
        """
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.tool = tool
        self.operation = operation
        self.param_extractor = param_extractor or (lambda m, c: {})
    
    def match(self, action: str, context: Dict[str, Any]) -> Optional[MCPToolCall]:
        """Try to match action and create tool call."""
        match = self.pattern.search(action)
        if match:
            params = self.param_extractor(match, context)
            return MCPToolCall(
                tool=self.tool.value,
                operation=self.operation,
                parameters=params,
                description=action
            )
        return None


class MCPMapper:
    """Map runbook actions to MCP tool calls."""
    
    def __init__(self):
        """Initialize mapper with action patterns."""
        self.patterns = self._initialize_patterns()
        self.available_tools = set(MCPTool)
    
    def _initialize_patterns(self) -> List[ActionPattern]:
        """Initialize action patterns for MCP mapping."""
        return [
            # Chronicle/SIEM patterns
            ActionPattern(
                r"query (?:siem|chronicle|logs?)(?: for)? (.+)",
                MCPTool.CHRONICLE,
                "search_events",
                lambda m, c: {"query": m.group(1), "timeframe": c.get("timeframe", "1h")}
            ),
            ActionPattern(
                r"search (?:for )?(.+) in (?:siem|chronicle|logs?)",
                MCPTool.CHRONICLE,
                "search_events",
                lambda m, c: {"query": m.group(1), "timeframe": c.get("timeframe", "1h")}
            ),
            ActionPattern(
                r"get (?:all )?events? (?:for|from|related to) (.+)",
                MCPTool.CHRONICLE,
                "get_events",
                lambda m, c: {"entity": m.group(1), "limit": 100}
            ),
            ActionPattern(
                r"correlate (.+) (?:with|and) (.+)",
                MCPTool.CHRONICLE,
                "correlate_events",
                lambda m, c: {"entity1": m.group(1), "entity2": m.group(2)}
            ),
            
            # GTI/Threat Intelligence patterns
            ActionPattern(
                r"(?:lookup|check|enrich) (?:reputation (?:of|for)|ioc) (.+)",
                MCPTool.GTI,
                "lookup_reputation",
                lambda m, c: {"indicator": m.group(1), "type": self._detect_ioc_type(m.group(1))}
            ),
            ActionPattern(
                r"get threat (?:intelligence|intel) (?:on|for|about) (.+)",
                MCPTool.GTI,
                "get_threat_intel",
                lambda m, c: {"indicator": m.group(1)}
            ),
            ActionPattern(
                r"check (?:if )?(.+) is (?:malicious|suspicious|known)",
                MCPTool.GTI,
                "check_malicious",
                lambda m, c: {"indicator": m.group(1)}
            ),
            
            # SOAR/Automation patterns
            ActionPattern(
                r"create (?:case|ticket|incident)(?: for)? (.+)",
                MCPTool.SOAR,
                "create_case",
                lambda m, c: {"title": m.group(1), "severity": c.get("severity", "medium")}
            ),
            ActionPattern(
                r"(?:block|quarantine|isolate) (.+)",
                MCPTool.SOAR,
                "containment_action",
                lambda m, c: {"target": m.group(1), "action": "block"}
            ),
            ActionPattern(
                r"run (?:playbook|automation) (.+)",
                MCPTool.SOAR,
                "execute_playbook",
                lambda m, c: {"playbook_name": m.group(1)}
            ),
            ActionPattern(
                r"update case (.+) with (.+)",
                MCPTool.SOAR,
                "update_case",
                lambda m, c: {"case_id": m.group(1), "update": m.group(2)}
            ),
            
            # SCC/Cloud Security patterns
            ActionPattern(
                r"(?:check|get) cloud security (?:posture|findings)(?: for)? (.+)",
                MCPTool.SCC,
                "get_findings",
                lambda m, c: {"resource": m.group(1)}
            ),
            ActionPattern(
                r"scan (.+) for (?:vulnerabilities|misconfigurations)",
                MCPTool.SCC,
                "scan_resource",
                lambda m, c: {"resource": m.group(1), "scan_type": "vulnerability"}
            ),
            
            # BigQuery/Analytics patterns
            ActionPattern(
                r"analyze (.+) (?:data|logs|patterns)",
                MCPTool.BIGQUERY,
                "analyze_data",
                lambda m, c: {"dataset": m.group(1), "analysis_type": "pattern"}
            ),
            ActionPattern(
                r"(?:run|execute) (?:query|sql) (.+)",
                MCPTool.BIGQUERY,
                "execute_query",
                lambda m, c: {"query": m.group(1)}
            ),
            
            # Generic patterns
            ActionPattern(
                r"(?:gather|collect|retrieve) (.+) (?:information|data|details)",
                MCPTool.CHRONICLE,
                "gather_info",
                lambda m, c: {"target": m.group(1)}
            ),
            ActionPattern(
                r"(?:document|record|log) (.+)",
                MCPTool.SOAR,
                "document_finding",
                lambda m, c: {"finding": m.group(1)}
            )
        ]
    
    def map_action(self, action: str, context: Optional[Dict[str, Any]] = None) -> List[MCPToolCall]:
        """
        Map an action description to MCP tool calls.
        
        Args:
            action: Action description from runbook
            context: Execution context with additional information
            
        Returns:
            List of MCP tool calls to execute the action
        """
        if context is None:
            context = {}
        
        tool_calls = []
        
        # Try to match against patterns
        for pattern in self.patterns:
            tool_call = pattern.match(action, context)
            if tool_call:
                tool_calls.append(tool_call)
                break
        
        # If no pattern matches, try to infer from keywords
        if not tool_calls:
            tool_call = self._infer_tool_call(action, context)
            if tool_call:
                tool_calls.append(tool_call)
        
        # If still no match, create a generic investigation call
        if not tool_calls:
            tool_calls.append(MCPToolCall(
                tool=MCPTool.CHRONICLE.value,
                operation="generic_search",
                parameters={"query": action, "context": str(context)},
                description=f"Generic search for: {action}"
            ))
        
        return tool_calls
    
    def _detect_ioc_type(self, indicator: str) -> str:
        """Detect the type of IOC from its format."""
        # IP address patterns
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', indicator):
            return "ip"
        # Domain patterns
        elif re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-_]*\.?[a-zA-Z0-9][a-zA-Z0-9-_]*\.[a-zA-Z]{2,}$', indicator):
            return "domain"
        # Hash patterns
        elif re.match(r'^[a-fA-F0-9]{32}$', indicator):
            return "md5"
        elif re.match(r'^[a-fA-F0-9]{40}$', indicator):
            return "sha1"
        elif re.match(r'^[a-fA-F0-9]{64}$', indicator):
            return "sha256"
        # URL pattern
        elif indicator.startswith(('http://', 'https://')):
            return "url"
        # Email pattern
        elif '@' in indicator and '.' in indicator:
            return "email"
        else:
            return "unknown"
    
    def _infer_tool_call(self, action: str, context: Dict[str, Any]) -> Optional[MCPToolCall]:
        """Try to infer tool call from action keywords."""
        action_lower = action.lower()
        
        # Chronicle/SIEM keywords
        if any(keyword in action_lower for keyword in ['log', 'event', 'siem', 'chronicle', 'search']):
            return MCPToolCall(
                tool=MCPTool.CHRONICLE.value,
                operation="search_events",
                parameters={"query": action, "context": str(context)},
                description=action
            )
        
        # GTI keywords
        elif any(keyword in action_lower for keyword in ['reputation', 'threat', 'malicious', 'ioc']):
            return MCPToolCall(
                tool=MCPTool.GTI.value,
                operation="lookup_reputation",
                parameters={"query": action},
                description=action
            )
        
        # SOAR keywords
        elif any(keyword in action_lower for keyword in ['block', 'contain', 'isolate', 'case', 'ticket']):
            return MCPToolCall(
                tool=MCPTool.SOAR.value,
                operation="automation_action",
                parameters={"action": action},
                description=action
            )
        
        # Cloud security keywords
        elif any(keyword in action_lower for keyword in ['cloud', 'gcp', 'aws', 'azure', 'finding']):
            return MCPToolCall(
                tool=MCPTool.SCC.value,
                operation="cloud_security_check",
                parameters={"query": action},
                description=action
            )
        
        return None
    
    def is_tool_available(self, tool_name: str) -> bool:
        """Check if a tool is available for use."""
        try:
            tool = MCPTool(tool_name)
            return tool in self.available_tools
        except ValueError:
            return False
    
    def get_tool_capabilities(self, tool_name: str) -> Dict[str, List[str]]:
        """Get capabilities of a specific tool."""
        capabilities = {
            MCPTool.CHRONICLE.value: [
                "search_events", "get_events", "correlate_events", 
                "timeline_analysis", "entity_investigation"
            ],
            MCPTool.GTI.value: [
                "lookup_reputation", "get_threat_intel", "check_malicious",
                "ioc_enrichment", "threat_actor_info"
            ],
            MCPTool.SOAR.value: [
                "create_case", "update_case", "containment_action",
                "execute_playbook", "notification"
            ],
            MCPTool.SCC.value: [
                "get_findings", "scan_resource", "compliance_check",
                "vulnerability_assessment"
            ],
            MCPTool.BIGQUERY.value: [
                "execute_query", "analyze_data", "statistical_analysis",
                "pattern_detection"
            ]
        }
        return capabilities.get(tool_name, [])