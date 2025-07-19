---
allowed_tools:
  - chronicle_mcp
  - google_cloud_security
  - soar_mcp
  - scc_mcp
  - gti_mcp
description: Execute incident response workflows following the PICERL lifecycle
---

# /security:respond Command

## Purpose
Orchestrate comprehensive incident response activities following the PICERL (Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned) framework. This command coordinates response actions, manages incident lifecycle, and ensures proper documentation.

## Usage
```
/security:respond --incident <type> [options]
```

## Arguments
- `--incident <type>` (required): Type of security incident
  - Values: `ransomware`, `data_breach`, `compromise`, `insider`, `dos`, `malware`, `supply_chain`
  - Custom types supported with appropriate runbook

## Options
- `--severity <level>`: Incident severity
  - Values: `low`, `medium`, `high`, `critical`
  - Default: Auto-assessed based on impact
  
- `--stage <phase>`: Current PICERL stage
  - Values: `identification`, `containment`, `eradication`, `recovery`, `lessons_learned`
  - Default: `identification` for new incidents
  
- `--case-id <id>`: Link to existing case
  - Format: `INC-2024-001`, `SOC-789`
  - Default: Auto-generated
  
- `--scope <affected_scope>`: Incident scope
  - Values: `single_host`, `department`, `site`, `global`
  - Default: Assessed during response
  
- `--persona <persona_name>`: Response team lead
  - Values: `incident_responder`, `tier3_soc_analyst`, `soc_manager`
  - Default: `incident_responder`
  
- `--team <members>`: Additional team members
  - Format: Comma-separated list of personas
  
- `--playbook <path>`: Specific response playbook
  - Default: Auto-selected based on incident type
  
- `--communication`: Enable stakeholder communications
- `--legal`: Include legal team
- `--executive`: Executive-level incident
- `--report`: Generate incident report

## Execution Framework

### 1. Incident Initialization
- Create/load incident record
- Assess initial severity and scope
- Activate incident response team
- Establish command structure
- Open communication channels

### 2. PICERL Lifecycle Execution

#### P - Preparation (Pre-incident)
```yaml
Already completed:
- Response procedures documented
- Tools and access configured
- Team roles defined
- Communication plans ready
```

#### I - Identification
1. **Incident Validation**
   - Confirm security incident
   - Gather initial evidence
   - Assess business impact
   - Determine incident type

2. **Initial Assessment**
   - Affected systems count
   - Data exposure risk
   - Service availability impact
   - Regulatory implications

3. **Severity Classification**
   ```
   Critical: Business-critical systems, data breach, ransomware
   High: Multiple systems, potential data loss
   Medium: Limited scope, contained impact
   Low: Single system, minimal impact
   ```

#### C - Containment
1. **Short-term Containment**
   - Isolate affected systems
   - Block malicious IPs/domains
   - Disable compromised accounts
   - Preserve evidence

2. **Long-term Containment**
   - Deploy temporary fixes
   - Implement monitoring
   - Strengthen controls
   - Prepare for eradication

3. **Evidence Collection**
   - System images
   - Memory dumps
   - Network captures
   - Log preservation

#### E - Eradication
1. **Root Cause Removal**
   - Remove malware/backdoors
   - Close vulnerabilities
   - Reset credentials
   - Patch systems

2. **Verification**
   - Scan for persistence
   - Validate removal
   - Check for reinfection
   - Monitor for callbacks

#### R - Recovery
1. **System Restoration**
   - Restore from backups
   - Rebuild if necessary
   - Apply all patches
   - Harden configurations

2. **Monitoring Enhancement**
   - Deploy additional sensors
   - Increase logging
   - Set up alerts
   - Watch for recurrence

3. **Validation Testing**
   - Functionality tests
   - Security validation
   - Performance checks
   - User acceptance

#### L - Lessons Learned
1. **Post-Incident Review**
   - Timeline reconstruction
   - Decision evaluation
   - Gap identification
   - Improvement opportunities

2. **Documentation**
   - Incident report
   - Metrics collection
   - Process updates
   - Training needs

## Incident-Specific Workflows

### Ransomware Response
```yaml
immediate_actions:
  - Isolate infected systems
  - Identify ransomware variant
  - Check backup integrity
  - Notify executive team
  
containment:
  - Network segmentation
  - Disable shares
  - Block C2 communications
  - Preserve encryption evidence

recovery:
  - Assess decryption options
  - Restore from backups
  - Rebuild if necessary
  - Implement anti-ransomware
```

### Data Breach Response
```yaml
immediate_actions:
  - Identify data scope
  - Stop ongoing exfiltration
  - Preserve evidence
  - Engage legal team

assessment:
  - Data classification
  - Record count
  - Regulatory requirements
  - Notification obligations

containment:
  - Access revocation
  - Data loss prevention
  - Network monitoring
  - Forensic analysis
```

### Insider Threat Response
```yaml
immediate_actions:
  - Suspend access discretely
  - Preserve evidence
  - Monitor activities
  - Engage HR/Legal

investigation:
  - Access pattern analysis
  - Data movement tracking
  - Communication review
  - Behavioral indicators

containment:
  - Gradual restriction
  - Covert monitoring
  - Evidence collection
  - Legal coordination
```

## Command Examples

### Critical Ransomware Incident
```
/security:respond --incident ransomware --severity critical --executive
```

### Data Breach with Legal
```
/security:respond --incident data_breach --legal --communication
```

### Ongoing Incident - Containment Phase
```
/security:respond --case-id INC-2024-001 --stage containment
```

### Full Team Response
```
/security:respond --incident compromise --team "tier3_soc_analyst,security_engineer" --report
```

## Automated Response Actions

### Immediate Containment
- Auto-isolate confirmed infected hosts
- Block malicious indicators (IOCs)
- Disable compromised credentials
- Initiate evidence collection

### Communication Triggers
- Severity >= High: SOC Manager notification
- Data breach: Legal team engagement
- Ransomware: Executive briefing
- Critical assets: Business continuity team

### Evidence Collection
- Automated memory dumps
- Network traffic capture
- System state snapshots
- Configuration backups

## Response Metrics
- **MTTD**: Mean Time to Detect
- **MTTA**: Mean Time to Acknowledge  
- **MTTC**: Mean Time to Contain
- **MTTR**: Mean Time to Recover
- **Impact**: Business impact assessment
- **Coverage**: % of incidents with playbooks

## Integration Points
- **soar_mcp**: Automated response orchestration
- **chronicle_mcp**: Investigation and timeline
- **scc_mcp**: Cloud security response
- **Rules Bank**: IRP documentation
- **Case Management**: Incident tracking

## Communication Templates
- Initial notification
- Status updates (hourly/daily)
- Stakeholder briefings
- External communications
- Post-incident report

## Escalation Matrix
```yaml
Low: SOC handles independently
Medium: SOC Manager informed
High: CISO briefed, legal consulted
Critical: Executive team, board notification
```

## Related Commands
- `/security:investigate` - Deep investigation
- `/security:triage` - Initial assessment  
- `/security:hunt` - Threat hunting
- `/security:report` - Report generation