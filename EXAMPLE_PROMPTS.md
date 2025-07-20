# Example Prompts Used to Generate Security Reports

This document shows the actual prompts used to generate the example security reports in the `./reports/` directory, demonstrating the SuperClaude Framework's security analysis capabilities.

## IOC Enrichment Examples

### 1. Domain Enrichment: superstarts.top

**Prompt:**
```
/security:enrich superstarts.top
```

**Generated Report:** `reports/ioc_enrichment_report_superstarts.top_20250720_0830.md`

**Description:** Basic domain enrichment using the `/security:enrich` command with a suspicious domain. The system automatically:
- Detected the indicator type as domain
- Queried Google Threat Intelligence
- Generated comprehensive threat assessment
- Provided actionable recommendations

### 2. Hash Enrichment: Conti Ransomware Sample

**Prompt:**
```
/security:enrich --type=hash 227164b06f201b07a8b82800adcc6a831cadaed6709d1473fd4182858fbd80a5
```

**Generated Report:** `reports/ioc_enrichment_report_conti_hash_20250720_0835.md`

**Description:** File hash enrichment with explicit type specification. The system:
- Analyzed the SHA256 hash using Google Threat Intelligence
- Identified it as Conti ransomware (CRITICAL risk)
- Extracted behavioral patterns and YARA rule matches
- Provided detailed malware analysis and IOC package

## Detection Engineering Examples

### 3. Detection Rule Creation from IOC Report

**Prompt:**
```
/security:detect create search for the IoCs from @reports/ioc_enrichment_report_conti_hash_20250720_0835.md
```

**Generated Report:** `reports/detection_rules_conti_ransomware_20250720_0840.md`

**Description:** Automatic detection rule generation from enrichment report. The system:
- Extracted IOCs and behavioral patterns from the source report
- Created 8 YARA-L detection rules for Chronicle SIEM
- Mapped rules to MITRE ATT&CK techniques
- Provided comprehensive rule documentation and hunt queries

### 4. Detection Rule Deployment Planning

**Prompt:**
```
/security:detect deploy @reports/detection_rules_conti_ransomware_20250720_0840.md
```

**Generated Report:** `reports/deployment_plan_conti_rules_20250720_0845.md`

**Description:** Production deployment planning for detection rules. The system:
- Validated rule syntax and structure
- Created 5-phase staged deployment plan
- Generated monitoring and alerting configurations
- Provided comprehensive rollback procedures

## Additional Security Reports

### 5. Rule Triage Report

**Report:** `reports/rule_triage_report_ru_99d1f620_20250720_0215.md`

**Description:** Example of Chronicle SIEM rule analysis and triage, showing how the system can assess detection rule performance and provide optimization recommendations.

### 6. Threat Hunt Report

**Report:** `reports/ursnif_hunt_report_2025-07-19.md`

**Description:** Example of proactive threat hunting analysis for Ursnif banking trojan, demonstrating comprehensive threat intelligence correlation and investigation workflow.

## SOAR Integration Examples

### 7. SOAR Case Investigation: BigQuery Exfiltration

**Prompt:**
```
/security:investigate 3519
```

**Generated Report:** `reports/case_investigation_3519_20250720.md`

**Description:** Complete SOAR case investigation for potential BigQuery data exfiltration incident. The system:
- Retrieved and analyzed case details with 4 related high-priority alerts
- Identified primary threat actor (ADMIN@WSEXAMPLE.ORG) accessing from external IP
- Correlated 32 underlying security events across all alerts
- Mapped activity to MITRE ATT&CK techniques (TA0010/T1537)
- Provided immediate response recommendations and investigation checklist

### 8. Multi-Alert Correlation Analysis

**Prompt:**
```
/security:correlate alerts de_6fad8a67-bd32-259b-cb7c-9a234818db3e de_2bb3c4fc-fe49-f607-d2cd-89889b05e57f de_951b2da3-b335-2b95-a45e-ea52e55224c3 de_9c49f199-37c2-cfb2-57fe-439a0950bc5e
```

**Generated Report:** `reports/alert_correlation_report_20250720_0845.md`

**Description:** Correlation analysis framework for multiple security alerts. The system:
- Created structured correlation methodology across temporal, entity, and behavioral dimensions
- Provided correlation matrix template for systematic analysis
- Identified investigation priorities and required data points
- Established framework for determining if alerts represent coordinated attack

### 9. Detection Rule Analysis

**Prompt:**
```
/security:analyze rule ur_ur_ttp_GCP_SCC_BQExtraction_with_DLP_Context
```

**Generated Report:** `reports/rule_analysis_ur_ur_ttp_GCP_SCC_BQExtraction_with_DLP_20250720_1445.md`

**Description:** Comprehensive analysis of Chronicle SIEM detection rule. The system:
- Decoded rule naming convention and purpose
- Identified threat scenarios (insider threat, compromised accounts, supply chain attacks)
- Provided detailed investigation checklist and response recommendations
- Suggested rule tuning for false positive reduction and enhanced detection
- Mapped to compliance frameworks (CIS, PCI DSS, NIST CSF)

## Command Workflow Patterns

### Pattern 1: IOC to Detection Pipeline
```
1. /security:enrich <indicator>           # Enrich IOC
2. /security:detect create @<report>      # Create detection rules
3. /security:detect deploy @<rules>       # Deploy to production
```

### Pattern 2: Threat Intelligence Workflow
```
1. /security:enrich <suspicious_indicator>
2. Analyze enrichment results
3. Create hunting queries from findings
4. Convert successful hunts to detection rules
```

### Pattern 3: Incident Response Workflow
```
1. /security:enrich <incident_indicators>
2. /security:investigate <case_id>
3. /security:detect create <incident_findings>
4. /security:report <comprehensive_analysis>
```

### Pattern 4: SOAR Case Analysis Workflow
```
1. /security:investigate <case_id>          # Full SOAR case analysis
2. /security:correlate alerts <alert_ids>   # Cross-alert correlation
3. /security:analyze rule <rule_id>         # Detection rule analysis
4. /security:hunt <attack_pattern>          # Hunt for similar patterns
```

## Key Features Demonstrated

### Automated Analysis
- **Context-Aware Processing:** System understands indicator types and applies appropriate analysis
- **Multi-Source Intelligence:** Integrates Google Threat Intelligence, Chronicle SIEM, and behavioral analysis
- **Risk Assessment:** Provides standardized risk scoring and confidence levels

### Detection Engineering
- **Rule Generation:** Automatically creates YARA-L rules from threat intelligence
- **MITRE Mapping:** Maps detections to ATT&CK framework
- **Deployment Planning:** Provides production-ready deployment strategies

### Integration Capabilities
- **MCP Tool Integration:** Leverages Model Context Protocol tools for security platforms
- **Report Chaining:** Uses output from one command as input to another
- **File Reference:** Can reference and analyze existing reports using `@filename` syntax

## Technical Implementation Notes

### Tool Integration
The examples use MCP (Model Context Protocol) tools for:
- `mcp__gti__get_domain_report` - Google Threat Intelligence domain analysis
- `mcp__gti__get_file_report` - File hash analysis
- `mcp__secops-mcp__lookup_entity` - Chronicle SIEM entity lookup
- `mcp__secops-soar__get_case_full_details` - SOAR case investigation
- `mcp__secops-soar__list_alerts_by_case` - Alert correlation analysis
- `mcp__secops-mcp__get_security_alert_by_id` - Individual alert details
- Various other security platform integrations

### Report Generation
All reports follow standardized formats with:
- YAML frontmatter for metadata
- Markdown structure for readability
- Standardized sections (Executive Summary, Technical Details, IOC Package, etc.)
- Actionable recommendations and next steps

### Quality Assurance
The system includes built-in validation for:
- Detection rule syntax checking
- Performance impact assessment
- False positive risk evaluation
- MITRE ATT&CK technique mapping

---

**Generated:** 2025-07-20T08:50:00Z  
**Purpose:** Document example prompts for SuperClaude Framework security capabilities  
**Classification:** TLP:WHITE - Public Documentation