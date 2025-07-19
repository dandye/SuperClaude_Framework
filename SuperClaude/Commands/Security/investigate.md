---
allowed_tools:
  - chronicle_mcp
  - google_cloud_security
  - gti_mcp
  - scc_mcp
  - soar_mcp
  - bigquery_mcp
description: Execute in-depth security investigation workflow for confirmed incidents
---

# /security:investigate Command

## Purpose
Perform comprehensive security investigations on confirmed incidents, suspicious activities, or alerts requiring deep analysis. This command orchestrates complex investigation workflows leveraging appropriate personas and specialized runbooks.

## Usage
```
/security:investigate <case_id> [options]
```

## Arguments
- `case_id` (required): The unique identifier for the investigation
  - Examples: `CASE-2024-001`, `INC-789`, `INV-123456`
  - Can also accept alert_id to initiate investigation from triage

## Options
- `--type <investigation_type>`: Specify investigation focus
  - Values: `compromise`, `data_breach`, `insider_threat`, `malware`, `lateral_movement`
  - Default: Auto-detected from case context
  
- `--scope <scope>`: Define investigation boundaries
  - Values: `endpoint`, `network`, `cloud`, `hybrid`, `user`, `application`
  - Default: `hybrid` (comprehensive)
  
- `--timeframe <period>`: Investigation time window
  - Format: `1h`, `24h`, `7d`, `30d`, `custom:YYYY-MM-DD to YYYY-MM-DD`
  - Default: `7d` from incident detection
  
- `--persona <persona_name>`: Use specific investigator persona
  - Values: `tier2_soc_analyst`, `tier3_soc_analyst`, `threat_hunter`, `incident_responder`
  - Default: `tier2_soc_analyst`
  
- `--runbook <runbook_path>`: Use specific investigation runbook
  - Default: Auto-selected based on investigation type
  
- `--depth <level>`: Investigation thoroughness
  - Values: `quick`, `standard`, `deep`, `forensic`
  - Default: `standard`
  
- `--parallel`: Enable parallel investigation tracks
- `--timeline`: Generate visual timeline of events
- `--ioc-hunt`: Automatically hunt for discovered IOCs
- `--report`: Generate comprehensive investigation report

## Execution Steps

### 1. Investigation Setup
- Parse case_id and validate access
- Load case context and related alerts
- Determine investigation type and scope
- Establish investigation timeline

### 2. Persona Activation
- Activate specified investigator persona
- Load investigation-specific capabilities:
  - Advanced query techniques
  - Forensic analysis skills
  - Pattern recognition abilities
  - Tool expertise levels

### 3. Runbook Selection
Investigation type mappings:
- **Compromise Assessment**: `compromise_investigation.md`
- **Data Breach**: `data_breach_investigation.md`
- **Insider Threat**: `insider_threat_investigation.md`
- **Malware Analysis**: `malware_investigation.md`
- **Lateral Movement**: `lateral_movement_investigation.md`
- **Generic**: `deep_dive_investigation.md`

### 4. Investigation Workflow

#### Phase 1: Scoping
1. **Initial Data Collection**
   - Gather all related alerts and events
   - Identify affected assets
   - Map initial timeline
   - Collect preliminary IOCs

2. **Context Enrichment**
   - Asset criticality assessment
   - User behavior analysis
   - Historical pattern review
   - Threat intelligence correlation

#### Phase 2: Deep Analysis
1. **Evidence Collection**
   - Log aggregation (Chronicle/SIEM)
   - Network traffic analysis
   - Endpoint telemetry
   - Cloud activity logs
   
2. **Forensic Analysis**
   - Memory analysis if available
   - File system artifacts
   - Registry/configuration changes
   - Persistence mechanisms

3. **Behavioral Analysis**
   - Attack pattern identification
   - TTP mapping to MITRE ATT&CK
   - Anomaly detection
   - Timeline reconstruction

#### Phase 3: Correlation
1. **Cross-Source Analysis**
   - Correlate findings across data sources
   - Identify attack progression
   - Map lateral movement
   - Discover additional compromises

2. **IOC Extraction**
   - Extract all indicators
   - Validate IOC quality
   - Categorize by confidence
   - Prepare for hunting

#### Phase 4: Conclusions
1. **Impact Assessment**
   - Determine data exposure
   - Identify affected systems/users
   - Assess business impact
   - Calculate risk score

2. **Attribution Analysis**
   - TTP comparison
   - Infrastructure analysis
   - Threat actor profiling
   - Confidence assessment

### 5. Investigation Actions
Automated actions based on findings:
- **High Confidence IOCs**: Auto-create detection rules
- **Confirmed Compromise**: Initiate containment
- **Data Exfiltration**: Trigger DLP response
- **Lateral Movement**: Network segmentation
- **Persistent Threat**: Full incident response

### 6. Documentation & Reporting
- Maintain investigation journal
- Document all findings with evidence
- Track hypothesis testing
- Generate timeline visualization
- Produce executive summary
- Create technical deep-dive report

## Example Workflows

### Standard Compromise Investigation
```
/security:investigate CASE-2024-001 --type compromise --depth standard
```

### Insider Threat with Extended Timeframe
```
/security:investigate INC-789 --type insider_threat --timeframe 30d --timeline
```

### Deep Forensic Analysis
```
/security:investigate INV-123456 --depth forensic --persona tier3_soc_analyst --report
```

### Parallel Multi-Scope Investigation
```
/security:investigate CASE-2024-002 --scope hybrid --parallel --ioc-hunt
```

## Investigation Techniques

### 1. Hypothesis-Driven Investigation
- Form initial hypotheses
- Test with targeted queries
- Refine based on evidence
- Document conclusion

### 2. Timeline Analysis
- Reconstruct event sequence
- Identify temporal anomalies
- Correlate across sources
- Visualize attack flow

### 3. Diamond Model Application
- Adversary analysis
- Infrastructure mapping
- Capability assessment
- Victim profiling

### 4. Kill Chain Mapping
- Identify completed stages
- Predict next steps
- Find defensive gaps
- Prioritize responses

## MCP Tool Integration
- **chronicle_mcp**: Primary SIEM queries and correlation
- **gti_mcp**: Threat intelligence enrichment
- **scc_mcp**: Cloud security posture and findings
- **soar_mcp**: Automated investigation playbooks
- **bigquery_mcp**: Large-scale data analysis

## Quality Checkpoints
- Evidence chain of custody
- Finding reproducibility
- Conclusion confidence levels
- Peer review for critical findings
- Legal/compliance validation

## Escalation Triggers
Auto-escalate when detecting:
- Nation-state indicators
- Critical asset compromise
- Ongoing data exfiltration
- Ransomware pre-deployment
- Supply chain compromise

## Related Commands
- `/security:triage` - Initial alert assessment
- `/security:hunt` - Proactive threat hunting
- `/security:respond` - Incident response
- `/security:report` - Generate reports