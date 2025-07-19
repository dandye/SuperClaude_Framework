---
allowed_tools: 
  - chronicle_mcp
  - google_cloud_security
  - gti_mcp
  - scc_mcp
  - soar_mcp
description: Execute security alert triage workflow with appropriate persona and runbook
---

# /security:triage Command

## Purpose
Execute comprehensive security alert triage workflow by loading the appropriate runbook, activating the suitable persona, and systematically working through the triage process.

## Usage
```
/security:triage <alert_id> [options]
```

## Arguments
- `alert_id` (required): The unique identifier for the alert to triage
  - Examples: `CHR-2024-001`, `SCC-ALERT-789`, `SIEM-123456`

## Options
- `--source <source>`: Specify the alert source
  - Values: `chronicle`, `scc`, `siem`, `soar`
  - Default: Auto-detected from alert_id format
  
- `--severity <level>`: Override the alert severity
  - Values: `low`, `medium`, `high`, `critical`
  - Default: Use alert's native severity
  
- `--persona <persona_name>`: Use specific persona
  - Values: `tier1_soc_analyst`, `tier2_soc_analyst`, `tier3_soc_analyst`
  - Default: `tier1_soc_analyst` for initial triage
  
- `--runbook <runbook_path>`: Use specific runbook
  - Default: Auto-selected based on alert type
  
- `--validate`: Validate actions before execution
- `--dry-run`: Show what would be executed without performing actions
- `--report`: Generate detailed triage report

## Execution Steps

### 1. Context Initialization
- Parse alert_id and options
- Detect or confirm alert source
- Load alert metadata from specified source

### 2. Persona Activation
- Activate specified persona or default tier1_soc_analyst
- Load persona-specific:
  - Skills and capabilities
  - Tool preferences
  - Decision thresholds
  - Escalation criteria

### 3. Runbook Selection
- If runbook specified: Load from rules_bank/run_books/
- Otherwise, auto-select based on:
  - Alert type/category
  - Source system
  - Severity level
  - Common patterns:
    - Suspicious login → suspicious_login_triage.md
    - Malware detection → malware_alert_triage.md
    - Data exfiltration → data_exfiltration_triage.md

### 4. Workflow Execution
- Parse runbook YAML frontmatter
- Execute workflow steps sequentially:
  1. **Initial Assessment**
     - Gather alert context
     - Check for related alerts
     - Assess initial severity
  
  2. **Enrichment**
     - Query threat intelligence (GTI)
     - Check asset criticality
     - Review user/entity history
  
  3. **Investigation**
     - Collect additional evidence
     - Analyze indicators
     - Determine scope
  
  4. **Decision Point**
     - True Positive → Escalate
     - False Positive → Document and close
     - Needs Investigation → Assign to tier2

### 5. Action Execution
- Use MCP tools as specified in runbook:
  - `chronicle_mcp`: Query SIEM data
  - `gti_mcp`: Threat intelligence lookups
  - `soar_mcp`: Automated response actions
  - `scc_mcp`: Cloud security context

### 6. Documentation
- Log all actions taken
- Record decision rationale
- Update case management
- Generate report if requested

## Example Workflows

### Basic Triage
```
/security:triage CHR-2024-001
```

### High-Priority Alert with Specific Persona
```
/security:triage SCC-ALERT-789 --severity critical --persona tier2_soc_analyst
```

### Dry Run with Validation
```
/security:triage SIEM-123456 --dry-run --validate
```

### Custom Runbook Execution
```
/security:triage CHR-2024-002 --runbook lateral_movement_investigation.md --report
```

## Auto-Activation Triggers
This command may be auto-activated when Claude detects:
- Alert IDs in conversation
- Keywords: "triage", "alert", "investigate alert"
- Security incident context
- SOC workflow discussions

## Integration Points
- **Runbooks**: Seamlessly executes runbooks from rules_bank/run_books/
- **Personas**: Activates appropriate security personas
- **MCP Tools**: Leverages security-focused MCP servers
- **Reporting**: Generates standardized triage reports

## Quality Gates
- Validates alert_id format
- Confirms runbook availability
- Checks MCP tool connectivity
- Enforces persona capabilities
- Validates decision criteria

## Error Handling
- Invalid alert_id: Prompt for correction
- Missing runbook: Suggest alternatives
- MCP tool failure: Graceful degradation
- Insufficient permissions: Escalate to appropriate tier

## Related Commands
- `/security:investigate` - Deep-dive investigation
- `/security:enrich` - IOC enrichment only
- `/security:hunt` - Proactive threat hunting
- `/security:respond` - Incident response