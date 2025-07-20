---
allowed_tools: 
  - chronicle_mcp
  - soar_mcp
  - gti_mcp
  - bigquery_mcp
  - google_cloud_security
description: Group and correlate related security cases for campaign detection and meta-analysis
---

# /security:correlate Command

## Purpose
Advanced case correlation and campaign detection to identify related security incidents, group similar cases, and perform meta-analysis across case clusters. This command helps SOC teams identify sophisticated attack campaigns and coordinated threats.

## Usage
```
/security:correlate <action> [target] [options]
```

## Actions
- `find`: Find cases similar to a specific case
- `group`: Group related cases into campaigns
- `analyze`: Perform meta-analysis on case groups
- `timeline`: Generate campaign timeline
- `attribute`: Attribute campaign to threat actors
- `predict`: Predict next campaign phases
- `report`: Generate campaign intelligence report

## Arguments
- `action` (required): The correlation action to perform
- `target` (conditional): Case ID, campaign ID, or search criteria
  - For find: Source case ID
  - For group: Search timeframe or criteria
  - For analyze/timeline/attribute: Campaign ID
  - For predict: Campaign ID or threat actor

## Options
- `--timeframe <duration>`: Analysis timeframe
  - Format: `24h`, `7d`, `30d`, `90d`
  - Default: `30d`
  
- `--correlation-type <type>`: Type of correlation
  - Values: `infrastructure`, `ttp`, `actor`, `timeline`, `all`
  - Default: `all`
  
- `--confidence-threshold <percent>`: Minimum correlation confidence
  - Range: 0-100
  - Default: `70`
  
- `--max-cases <number>`: Maximum cases to correlate
  - Default: `100`
  
- `--include-closed`: Include closed cases in correlation
- `--cross-tenant`: Correlate across tenants (if permitted)
- `--auto-group`: Automatically create case groups
- `--visualize`: Generate correlation graphs

## Correlation Criteria

### 1. Infrastructure Correlation
- Shared IP addresses
- Common domains
- Similar URLs patterns
- Network infrastructure overlap
- Certificate reuse

### 2. TTP Correlation
- MITRE ATT&CK techniques
- Similar attack patterns
- Common tools/malware
- Exploitation methods
- Persistence mechanisms

### 3. Temporal Correlation
- Activity time windows
- Attack sequence patterns
- Coordinated timing
- Campaign phases
- Kill chain progression

### 4. Threat Actor Correlation
- Known actor indicators
- Attribution markers
- Infrastructure preferences
- Tool preferences
- Target selection patterns

## Execution Steps

### 1. Find Similar Cases
When action is `find`:
- Load source case details
- Extract correlation indicators:
  - IOCs (IPs, domains, hashes)
  - TTPs and techniques
  - Timeline patterns
  - Entity relationships
- Search for cases with:
  - Matching indicators
  - Similar patterns
  - Overlapping timeframes
- Calculate similarity scores
- Rank by correlation confidence

### 2. Group Related Cases
When action is `group`:
- Query cases within timeframe
- Apply correlation algorithms:
  - Graph-based clustering
  - Pattern matching
  - Timeline analysis
  - Statistical correlation
- Create case groups based on:
  - High correlation scores
  - Shared infrastructure
  - Common TTPs
  - Actor attribution
- Assign campaign identifiers

### 3. Meta-Analysis
When action is `analyze`:
- Load campaign case group
- Perform analysis:
  - Extract common indicators
  - Identify patterns
  - Map kill chain progression
  - Determine campaign objectives
  - Assess impact scope
- Generate insights:
  - Campaign timeline
  - Target profile
  - Attack methodology
  - Success indicators

### 4. Campaign Timeline
When action is `timeline`:
- Collect all campaign events
- Order chronologically
- Identify:
  - Initial compromise
  - Lateral movement
  - Escalation points
  - Exfiltration events
  - Cleanup activities
- Visualize campaign progression
- Highlight critical events

### 5. Threat Attribution
When action is `attribute`:
- Analyze campaign characteristics
- Compare against threat intelligence:
  - Known actor profiles
  - Infrastructure databases
  - TTP repositories
  - Historical campaigns
- Calculate attribution confidence
- Provide evidence mapping

### 6. Predictive Analysis
When action is `predict`:
- Analyze campaign patterns
- Review threat actor playbooks
- Identify:
  - Incomplete kill chain stages
  - Likely next targets
  - Expected techniques
  - Timeline projections
- Generate predictions with confidence scores

## Integration with Runbooks

### Primary Runbooks
- `group_cases_v2.md`: Advanced case grouping logic
- `metaanalysis.md`: Meta-analysis procedures
- `compare_gti_collection_to_iocs_and_events.md`: Threat intel correlation

### Supporting Runbooks
- `close_duplicate_or_similar_cases.md`: Deduplication
- `create_an_investigation_report.md`: Campaign reporting

## Example Workflows

### Find Similar Cases
```
/security:correlate find CASE-2024-789 --timeframe 90d --correlation-type infrastructure
```

### Create Campaign Group
```
/security:correlate group --timeframe 30d --auto-group --confidence-threshold 80
```

### Analyze Suspected Campaign
```
/security:correlate analyze CAMPAIGN-2024-001 --visualize
```

### Full Campaign Investigation
```
/security:correlate find CASE-2024-100
/security:correlate group --timeframe 30d --auto-group
/security:correlate analyze CAMPAIGN-2024-002
/security:correlate timeline CAMPAIGN-2024-002 --visualize
/security:correlate attribute CAMPAIGN-2024-002
/security:correlate predict CAMPAIGN-2024-002
```

## Correlation Algorithms

### Graph-Based Clustering
1. Build relationship graph
2. Calculate edge weights
3. Apply clustering algorithm
4. Identify dense subgraphs
5. Extract campaign groups

### Pattern Matching
1. Extract behavioral patterns
2. Normalize representations
3. Calculate similarity matrices
4. Apply threshold filtering
5. Group by similarity

### Timeline Analysis
1. Extract temporal features
2. Identify activity bursts
3. Correlate across entities
4. Detect coordinated actions
5. Map campaign phases

## Output Formats

### Correlation Results
```json
{
  "campaign_id": "CAMPAIGN-2024-001",
  "confidence": 85,
  "case_count": 12,
  "timespan": "2024-01-15 to 2024-02-10",
  "common_indicators": [...],
  "shared_ttps": [...],
  "attribution": {
    "actor": "APT-XX",
    "confidence": 75
  }
}
```

### Campaign Intelligence Report
- Executive summary
- Technical analysis
- Indicator lists
- Timeline visualization
- Attribution assessment
- Defensive recommendations

## Quality Metrics

### Correlation Accuracy
- False positive rate < 15%
- Validated groupings > 80%
- Attribution accuracy tracking

### Performance Metrics
- Correlation time < 5 minutes
- Maximum 10,000 cases analyzed
- Real-time updates supported

## Auto-Activation Triggers
- Multiple similar cases detected
- Campaign keywords in conversation
- Cross-case investigation requests
- Threat actor activity mentioned

## Error Handling
- Insufficient data: Lower confidence thresholds
- Too many matches: Apply stricter filtering
- Attribution conflicts: Present multiple hypotheses
- Performance issues: Batch processing mode

## Related Commands
- `/security:investigate` - Deep-dive into campaigns
- `/security:hunt` - Hunt for campaign indicators
- `/security:intel` - Enrich with threat intelligence
- `/security:report` - Generate campaign reports