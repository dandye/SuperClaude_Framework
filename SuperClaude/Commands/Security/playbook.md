---
allowed_tools: 
  - chronicle_mcp
  - soar_mcp
  - gti_mcp
  - github_mcp
  - all_mcp_tools
description: Execute and manage custom security playbooks with parameter substitution and versioning
---

# /security:playbook Command

## Purpose
Manage, validate, execute, and track custom security playbooks from the rules_bank. This command enables dynamic playbook execution with parameter substitution, conditional logic, and comprehensive execution tracking for security automation workflows.

## Usage
```
/security:playbook <action> <playbook_name> [options]
```

## Actions
- `run`: Execute a playbook
- `validate`: Validate playbook syntax and structure
- `list`: List available playbooks
- `inspect`: Show playbook details and parameters
- `track`: Track playbook execution history
- `test`: Test playbook in dry-run mode
- `customize`: Create customized playbook variant

## Arguments
- `action` (required): The playbook action to perform
- `playbook_name` (required for most actions): Name of the playbook
  - Format: `filename.md` or `category/filename.md`
  - Examples: `malware_triage.md`, `irps/ransomware_response.md`

## Options
- `--params <json>`: Parameters for playbook execution
  - Format: JSON object with key-value pairs
  - Example: `{"case_id": "CASE-123", "severity": "high"}`
  
- `--persona <persona_name>`: Execute with specific persona
  - Default: Auto-selected based on playbook requirements
  
- `--mode <mode>`: Execution mode
  - Values: `interactive`, `automated`, `supervised`
  - Default: `supervised`
  
- `--timeout <minutes>`: Maximum execution time
  - Default: `60`
  
- `--checkpoint`: Enable checkpoint/resume capability
- `--parallel`: Enable parallel step execution where possible
- `--strict`: Fail on any error (no graceful degradation)
- `--output <format>`: Output format for results
  - Values: `summary`, `detailed`, `json`

## Playbook Structure

### YAML Frontmatter
```yaml
---
title: Playbook Title
category: incident-response|detection|hunting|triage
severity_levels: [low, medium, high, critical]
required_tools: [chronicle_mcp, soar_mcp]
required_params:
  - case_id
  - alert_source
optional_params:
  - custom_threshold
  - notification_list
estimated_duration: 30
---
```

### Playbook Sections
1. **Prerequisites**: Required conditions
2. **Parameters**: Input parameters
3. **Steps**: Execution steps
4. **Decision Points**: Conditional logic
5. **Outputs**: Expected results
6. **Rollback**: Failure handling

## Execution Engine

### 1. Playbook Loading
- Parse markdown file
- Extract YAML frontmatter
- Validate structure
- Load step definitions
- Identify dependencies

### 2. Parameter Resolution
- Validate required parameters
- Apply defaults for optional
- Perform type checking
- Substitute variables
- Build execution context

### 3. Step Execution
- **Sequential Steps**
  ```markdown
  1. Query alert details
     - Tool: chronicle_mcp
     - Action: get_alert({{alert_id}})
  ```
  
- **Conditional Steps**
  ```markdown
  2. IF severity == "critical":
     - Escalate to incident response
     ELSE:
     - Continue triage
  ```
  
- **Parallel Steps**
  ```markdown
  3. PARALLEL:
     - Check threat intelligence
     - Query asset information
     - Review similar cases
  ```
  
- **Loop Steps**
  ```markdown
  4. FOR EACH indicator IN {{ioc_list}}:
     - Enrich indicator
     - Check detection coverage
  ```

### 4. State Management
- Track execution state
- Store intermediate results
- Enable checkpointing
- Support resume capability
- Handle rollback scenarios

### 5. Error Handling
- Try-catch blocks
- Graceful degradation
- Error logging
- Rollback triggers
- Notification on failure

## Playbook Library

### Categories
- **Incident Response** (`/irps/`)
  - Ransomware response
  - Data breach handling
  - Compromise recovery
  
- **Triage** (`/run_books/`)
  - Alert triage
  - IOC enrichment
  - Malware analysis
  
- **Hunting** (`/run_books/`)
  - APT hunting
  - Lateral movement
  - Persistence hunting
  
- **Detection** (`/run_books/`)
  - Rule validation
  - Coverage analysis
  - Tuning workflows

## Example Workflows

### Execute Triage Playbook
```
/security:playbook run alert_triage.md --params '{"alert_id": "CHR-123", "priority": "high"}'
```

### Validate Custom Playbook
```
/security:playbook validate custom_investigation.md --strict
```

### Test Incident Response Playbook
```
/security:playbook test irps/ransomware_response.md --params '{"affected_systems": ["host1", "host2"]}' --mode interactive
```

### Track Playbook Performance
```
/security:playbook track malware_triage.md --period last_30_days
```

### Create Customized Variant
```
/security:playbook customize phishing_response.md --name "phishing_response_executive.md" --params '{"vip_user": true}'
```

## Advanced Features

### Dynamic Parameter Injection
```yaml
steps:
  - name: "Enrich IOCs"
    tool: gti_mcp
    action: enrich_indicators
    params:
      indicators: "{{dynamic:extract_iocs_from_case}}"
      depth: "{{user_param:enrichment_depth|default:medium}}"
```

### Conditional Execution
```yaml
steps:
  - name: "Check severity"
    condition: "result.severity in ['high', 'critical']"
    then:
      - tool: soar_mcp
        action: escalate_case
    else:
      - tool: soar_mcp
        action: update_priority
```

### Error Recovery
```yaml
steps:
  - name: "Primary detection"
    tool: chronicle_mcp
    on_error:
      - retry: 3
      - fallback:
          tool: alternative_siem
          action: query_logs
```

### Parallel Execution
```yaml
parallel_steps:
  - group: "enrichment"
    steps:
      - name: "GTI lookup"
        tool: gti_mcp
      - name: "Asset info"
        tool: cmdb_mcp
      - name: "User context"
        tool: identity_mcp
```

## Execution Tracking

### Metrics Captured
- Execution time per step
- Success/failure rates
- Parameter usage
- Error patterns
- Resource utilization

### Execution History
```json
{
  "playbook": "malware_triage.md",
  "executions": [
    {
      "id": "exec-123",
      "timestamp": "2024-01-20T10:30:00Z",
      "duration": "12m34s",
      "status": "success",
      "parameters": {...},
      "steps_completed": 8,
      "output": {...}
    }
  ]
}
```

## Quality Assurance

### Playbook Validation
- Syntax checking
- Parameter validation
- Tool availability
- Permission verification
- Logic flow analysis

### Testing Framework
- Unit tests per step
- Integration testing
- Mock data support
- Regression testing
- Performance benchmarks

## Version Control

### Playbook Versioning
- Git integration
- Change tracking
- Approval workflow
- Rollback capability
- A/B testing support

### Update Notifications
- Breaking changes
- New capabilities
- Deprecation warnings
- Migration guides

## Error Handling
- Invalid playbook: Show validation errors
- Missing parameters: Prompt for required inputs
- Tool failures: Attempt fallback options
- Timeout: Save state and allow resume
- Permission denied: Suggest elevation

## Related Commands
- `/security:triage` - Uses triage playbooks
- `/security:respond` - Uses response playbooks
- `/security:hunt` - Uses hunting playbooks
- `/workflow` - General workflow execution