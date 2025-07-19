---
allowed_tools:
  - chronicle_mcp
  - google_cloud_security
  - gti_mcp
  - scc_mcp
  - bigquery_mcp
  - soar_mcp
description: Execute proactive threat hunting workflows to discover hidden threats
---

# /security:hunt Command

## Purpose
Proactively search for threats, adversaries, and malicious activities that may have evaded detection. This command enables hypothesis-driven hunting, TTP-based searches, and anomaly detection across the environment.

## Usage
```
/security:hunt [options]
```

## Options
- `--hypothesis <description>`: Hunt based on specific hypothesis
  - Example: "APT group using living-off-the-land techniques"
  
- `--ttp <technique_id>`: Hunt for specific MITRE ATT&CK techniques
  - Format: `T1003`, `T1055.001`, multiple: `T1003,T1055`
  - Special values: `lateral_movement`, `persistence`, `exfiltration`
  
- `--threat-actor <name>`: Hunt for specific threat actor TTPs
  - Examples: `APT29`, `FIN7`, `Lazarus`

- `--collection <collection_id>`: Hunt based on GTI collection
  - Format: Google Threat Intelligence Collection ID
  - Examples: `c-12345678-1234-1234-1234-123456789abc`
  - Supports: threat-actor, malware-family, campaign, vulnerability collections
  
- `--anomaly <type>`: Hunt for behavioral anomalies
  - Values: `network`, `process`, `authentication`, `data_access`
  
- `--scope <environment>`: Define hunting scope
  - Values: `endpoints`, `network`, `cloud`, `identities`, `all`
  - Default: `all`
  
- `--timeframe <period>`: Hunting lookback window
  - Format: `24h`, `7d`, `30d`, `90d`
  - Default: `30d`
  
- `--baseline <period>`: Baseline period for anomaly detection
  - Format: `7d`, `30d`, `90d`
  - Default: `90d`
  
- `--persona <persona_name>`: Use specific hunter persona
  - Values: `threat_hunter`, `tier3_soc_analyst`, `detection_engineer`
  - Default: `threat_hunter`
  
- `--campaign`: Hunt for campaign-related activities
- `--crown-jewels`: Focus on critical assets
- `--zero-day`: Hunt for unknown/novel techniques
- `--report`: Generate hunt report with findings

## Execution Steps

### 1. Hunt Preparation
- Define hunt objectives
- Load hunter persona with specialized skills
- Prepare data sources and tools
- Establish success criteria

### 2. Persona Activation
Threat Hunter capabilities:
- Advanced query construction
- Pattern recognition
- Anomaly detection
- TTP expertise
- Creative thinking
- Statistical analysis

### 3. Hunt Methodology Selection

#### Hypothesis-Driven Hunting
1. **Hypothesis Formation**
   - Based on threat intelligence
   - Recent attack trends
   - Environmental weaknesses
   - Industry targeting

2. **Data Collection Strategy**
   - Identify relevant data sources
   - Define search parameters
   - Plan analysis approach
   - Set detection thresholds

#### TTP-Based Hunting
1. **Technique Analysis**
   - Understand technique details
   - Map to environment
   - Identify artifacts
   - Build detection logic

2. **Variant Consideration**
   - Known implementations
   - Possible variations
   - Environmental adaptations
   - Evasion techniques

#### Collection-Based Hunting
1. **Collection Analysis**
   - Retrieve collection details and type
   - Extract related IOCs (domains, IPs, file hashes, URLs)
   - Map MITRE ATT&CK techniques
   - Analyze timeline events and attribution

2. **Environment Correlation**
   - Search SIEM for collection IOCs
   - Hunt for related TTPs and behaviors
   - Correlate with historical events
   - Assess environmental presence

#### Anomaly-Based Hunting
1. **Baseline Establishment**
   - Normal behavior patterns
   - Statistical distributions
   - Temporal patterns
   - Peer group analysis

2. **Outlier Detection**
   - Statistical anomalies
   - Behavioral deviations
   - Rare events
   - Impossible travel

### 4. Hunt Execution

#### Phase 1: Wide-Net Casting
```
- Broad searches for indicators
- Pattern matching across data
- Anomaly detection algorithms
- Correlation analysis
```

#### Phase 2: Focused Investigation
```
- Deep-dive suspicious findings
- Expand search around discoveries
- Validate through multiple sources
- Eliminate false positives
```

#### Phase 3: TTP Mapping
```
- Map findings to ATT&CK
- Identify technique chains
- Assess sophistication
- Profile potential adversary
```

### 5. Hunt Techniques

#### 1. Stack Counting
- Identify least frequent occurrences
- Find outliers in common activities
- Detect rare process launches
- Unusual network connections

#### 2. Clustering Analysis
- Group similar behaviors
- Identify outlier clusters
- Detect coordinated activities
- Find hidden campaigns

#### 3. Time-Series Analysis
- Detect temporal anomalies
- Identify beaconing
- Find scheduled tasks
- Discover data staging

#### 4. Graph Analysis
- Map entity relationships
- Find unusual connections
- Detect lateral movement paths
- Identify command and control

### 6. Automated Hunt Playbooks

#### Persistence Hunting
```yaml
targets:
  - Registry modifications
  - Scheduled tasks
  - Service installations
  - Startup folder changes
  - WMI event consumers
```

#### Lateral Movement Hunting
```yaml
targets:
  - Remote desktop usage
  - PSExec patterns
  - WMI remote execution
  - PowerShell remoting
  - Pass-the-hash indicators
```

#### Data Exfiltration Hunting
```yaml
targets:
  - Large outbound transfers
  - Unusual protocols
  - DNS tunneling
  - Cloud storage uploads
  - Encrypted archives
```

#### Collection-Based Hunting
```yaml
workflow:
  1. Collection Intelligence Gathering:
     - get_collection_report: Retrieve collection details and type
     - get_collection_mitre_tree: Map ATT&CK techniques
     - get_collection_timeline_events: Analyze temporal activity
     
  2. IOC Extraction:
     - get_entities_related_to_a_collection (domains)
     - get_entities_related_to_a_collection (files) 
     - get_entities_related_to_a_collection (ip_addresses)
     - get_entities_related_to_a_collection (urls)
     
  3. Environmental Hunt:
     - lookup_entity: Check IOC presence in SIEM
     - search_security_events: Hunt for IOC-related activity
     - get_ioc_matches: Correlate with threat feeds
     
  4. TTP Hunt:
     - Search for collection's MITRE techniques
     - Hunt for related threat actor behaviors
     - Correlate with campaign patterns
```

## Example Hunts

### Basic TTP Hunt
```
/security:hunt --ttp T1055 --scope endpoints
```

### Advanced Threat Actor Hunt
```
/security:hunt --threat-actor APT29 --timeframe 90d --crown-jewels
```

### Anomaly-Based Hunt
```
/security:hunt --anomaly authentication --baseline 30d --scope identities
```

### Campaign Hunting
```
/security:hunt --campaign --hypothesis "Supply chain compromise via update mechanism"
```

### Collection-Based Hunting
```
# Hunt based on threat actor collection
/security:hunt --collection c-12345678-1234-1234-1234-123456789abc --scope all --timeframe 90d

# Hunt for malware family with reporting
/security:hunt --collection c-malware123-1234-1234-1234-123456789abc --report --crown-jewels

# Hunt campaign collection with specific scope
/security:hunt --collection c-campaign1-1234-1234-1234-123456789abc --scope endpoints --timeframe 30d
```

## Hunt Metrics
Track hunt effectiveness:
- Coverage: % of environment analyzed
- Findings: New threats discovered
- Detection gaps: Blind spots identified
- Time to discovery: Hunt efficiency
- False positive rate: Accuracy

## Hunt Outputs

### 1. Findings Report
- Executive summary
- Technical details
- Evidence documentation
- Risk assessment
- Recommendations

### 2. Detection Opportunities
- New detection rules
- SIEM content updates
- Behavioral baselines
- Monitoring improvements

### 3. Threat Intelligence
- New IOCs discovered
- TTP documentation
- Adversary profiling
- Campaign mapping

## Integration Points
- **chronicle_mcp**: Primary hunting platform
- **gti_mcp**: Threat intelligence correlation and collection analysis
- **bigquery_mcp**: Large-scale data analysis
- **Rules Bank**: Hunt procedure documentation
  - `investigate_a_gti_collection_id.md`: Collection investigation workflow
  - `compare_gti_collection_to_iocs_and_events.md`: Collection-to-environment correlation
  - `proactive_threat_hunting_based_on_gti_campaign_or_actor.md`: Collection-driven hunting
- **Detection Engineering**: Rule creation from findings

## Hunt Automation
Scheduled hunts for:
- Weekly: Common persistence mechanisms
- Daily: Authentication anomalies
- Hourly: Critical asset access
- Continuous: Crown jewel monitoring

## Related Commands
- `/security:investigate` - Deep investigation of findings
- `/security:triage` - Initial alert validation
- `/security:respond` - Response to discovered threats
- `/security:report` - Generate hunt reports