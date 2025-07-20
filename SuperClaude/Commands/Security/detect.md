---
allowed_tools: 
  - chronicle_mcp
  - google_cloud_security
  - gti_mcp
  - bigquery_mcp
  - github_mcp
description: Manage security detection rules lifecycle - create, validate, tune, and deploy
---

# /security:detect Command

## Purpose
Comprehensive detection engineering workflow for creating, validating, tuning, and deploying security detection rules. This command enables AI agents to manage the full lifecycle of detection rules from initial creation through continuous improvement.

## Usage
```
/security:detect <action> [target] [options]
```

## Actions
- `create`: Create new detection rule from threat intelligence or incident
- `validate`: Validate detection logic against historical data
- `tune`: Tune existing rule to reduce false positives
- `test`: Test rule in sandbox environment
- `deploy`: Deploy rule to production
- `coverage`: Analyze detection coverage against MITRE ATT&CK
- `review`: Review rule performance metrics

## Arguments
- `action` (required): The detection engineering action to perform
- `target` (conditional): Rule ID, threat ID, or incident ID depending on action
  - For create: Threat collection ID or incident ID
  - For validate/tune/test/deploy: Rule ID
  - For coverage: Optional MITRE tactic/technique

## Options
- `--rule-type <type>`: Type of detection rule
  - Values: `yara-l`, `sigma`, `splunk`, `kql`, `custom`
  - Default: `yara-l` for Chronicle
  
- `--severity <level>`: Set rule severity
  - Values: `informational`, `low`, `medium`, `high`, `critical`
  - Default: Based on threat intelligence
  
- `--confidence <level>`: Set detection confidence
  - Values: `low`, `medium`, `high`
  - Default: `medium`
  
- `--lookback <duration>`: Historical data lookback period
  - Format: `1h`, `24h`, `7d`, `30d`
  - Default: `7d`
  
- `--threshold <number>`: Alert threshold for matches
  - Default: `1` for high-confidence rules
  
- `--test-mode`: Run in test/silent mode
- `--auto-tune`: Enable automatic tuning based on false positive rate
- `--mitre-mapping`: Map to MITRE ATT&CK techniques
- `--generate-tests`: Generate test cases for validation

## Execution Steps

### 1. Create Detection Rule
When action is `create`:
- Extract IOCs and TTPs from source (threat intel or incident)
- Generate detection logic based on:
  - Behavioral patterns
  - Network indicators
  - File/process indicators
  - Authentication anomalies
- Map to MITRE ATT&CK framework
- Create rule metadata and documentation

### 2. Validate Detection
When action is `validate`:
- Load rule definition
- Query historical data using lookback period
- Analyze matches for:
  - True positive rate
  - False positive rate
  - Coverage gaps
  - Performance impact
- Generate validation report

### 3. Tune Detection
When action is `tune`:
- Analyze false positive patterns
- Identify tuning opportunities:
  - Add exclusions/allowlists
  - Adjust thresholds
  - Refine pattern matching
  - Add contextual conditions
- Test tuned version
- Compare before/after metrics

### 4. Test Detection
When action is `test`:
- Deploy to test environment
- Run against:
  - Known malicious samples
  - Benign baseline data
  - Edge cases
- Monitor for:
  - Detection accuracy
  - Performance impact
  - Resource utilization

### 5. Deploy Detection
When action is `deploy`:
- Perform final validation
- Create deployment package
- Deploy to production with:
  - Version tracking
  - Rollback capability
  - Change documentation
- Configure alerting/response

### 6. Coverage Analysis
When action is `coverage`:
- Map existing rules to MITRE ATT&CK
- Identify coverage gaps
- Prioritize based on:
  - Threat landscape
  - Environment risks
  - Recent incidents
- Generate coverage heatmap

### 7. Review Performance
When action is `review`:
- Collect rule performance metrics:
  - Alert volume
  - True/false positive rates
  - Mean time to detect
  - Resource consumption
- Identify improvement opportunities
- Generate performance report

## Integration with Runbooks

### Primary Runbook
- `detection_rule_validation_tuning.md`: Core workflow for rule lifecycle

### Supporting Runbooks
- `detection_as_code_workflows.md`: CI/CD integration
- `advanced_threat_hunting.md`: Hunt hypothesis to detection

## Example Workflows

### Create Rule from Threat Intelligence
```
/security:detect create GTI-COLLECTION-123 --rule-type yara-l --severity high --mitre-mapping
```

### Validate Existing Rule
```
/security:detect validate CHR-RULE-456 --lookback 30d --generate-tests
```

### Tune High-Volume Rule
```
/security:detect tune CHR-RULE-789 --auto-tune --threshold 5
```

### Full Deployment Workflow
```
/security:detect create INCIDENT-2024-001 --test-mode
/security:detect validate RULE-DRAFT-001 --lookback 14d
/security:detect tune RULE-DRAFT-001 --auto-tune
/security:detect test RULE-DRAFT-001
/security:detect deploy RULE-DRAFT-001 --severity high
```

### Coverage Gap Analysis
```
/security:detect coverage --mitre-mapping
/security:detect coverage T1055 --rule-type yara-l
```

## Quality Gates

### Rule Creation
- Valid detection logic syntax
- Minimum documentation requirements
- MITRE ATT&CK mapping
- Test case availability

### Validation Criteria
- False positive rate < 20%
- True positive validation
- Performance impact < 100ms
- No syntax errors

### Deployment Requirements
- Validation passed
- Approval workflow completed
- Rollback plan documented
- Monitoring configured

## Automation Features

### Auto-Tuning Algorithm
1. Collect false positive samples
2. Identify common patterns
3. Generate exclusion logic
4. Test updated rule
5. Deploy if metrics improve

### Coverage Recommendations
1. Analyze recent incidents
2. Review threat intelligence
3. Identify missing detections
4. Prioritize by risk score
5. Generate rule templates

## Output Formats

### Detection Rule
- YARA-L format for Chronicle
- Sigma universal format
- Platform-specific syntax
- JSON rule definition

### Reports
- Validation report (markdown)
- Coverage heatmap (HTML)
- Performance metrics (JSON)
- Deployment summary

## Error Handling
- Invalid rule syntax: Provide syntax correction suggestions
- High false positive rate: Recommend tuning options
- Performance issues: Suggest optimization strategies
- Deployment failures: Automatic rollback

## Related Commands
- `/security:hunt` - Convert hunt findings to detections
- `/security:investigate` - Create rules from incident patterns
- `/security:metrics` - Track detection effectiveness
- `/security:compliance` - Ensure detection compliance