---
allowed_tools: 
  - scc_mcp
  - chronicle_mcp
  - bigquery_mcp
  - google_cloud_security
  - github_mcp
description: Validate security controls and generate compliance evidence for various frameworks
---

# /security:compliance Command

## Purpose
Comprehensive compliance validation and evidence generation for security controls across multiple regulatory frameworks and standards. This command automates compliance checking, gap analysis, and audit evidence collection to support continuous compliance monitoring.

## Usage
```
/security:compliance <action> <framework> [options]
```

## Actions
- `check`: Run compliance checks for a framework
- `audit`: Generate audit evidence package
- `gap`: Perform gap analysis
- `monitor`: Continuous compliance monitoring
- `report`: Generate compliance reports
- `remediate`: Create remediation plans
- `attest`: Generate attestation documents

## Arguments
- `action` (required): The compliance action to perform
- `framework` (required): Compliance framework or standard
  - Values: `soc2`, `iso27001`, `nist`, `pci-dss`, `hipaa`, `cis`, `custom`
  - Multiple: Use comma separation for multiple frameworks

## Options
- `--scope <scope>`: Compliance check scope
  - Values: `organization`, `project`, `service`, `control-family`
  - Default: `organization`
  
- `--control-set <set>`: Specific control set to validate
  - Examples: `AC` (Access Control), `IR` (Incident Response)
  
- `--evidence-level <level>`: Evidence collection depth
  - Values: `summary`, `detailed`, `full`
  - Default: `detailed`
  
- `--period <timeframe>`: Audit period
  - Format: `30d`, `90d`, `1y`
  - Default: `90d`
  
- `--format <format>`: Output format
  - Values: `report`, `json`, `csv`, `audit-package`
  - Default: `report`
  
- `--include-evidence`: Include supporting evidence
- `--automated-only`: Only run automated checks
- `--generate-tasks`: Create remediation tasks
- `--risk-based`: Apply risk-based prioritization

## Compliance Frameworks

### SOC 2 Type II
- **Trust Service Criteria**
  - Security (CC)
  - Availability (A)
  - Processing Integrity (PI)
  - Confidentiality (C)
  - Privacy (P)
  
- **Key Controls**
  - Access management
  - Change management
  - Risk assessment
  - Incident response
  - Monitoring

### ISO 27001:2022
- **Control Domains**
  - A.5: Organizational controls
  - A.6: People controls
  - A.7: Physical controls
  - A.8: Technological controls
  
- **Implementation**
  - Policy compliance
  - Risk treatment
  - Control effectiveness
  - Continuous improvement

### NIST Cybersecurity Framework
- **Core Functions**
  - Identify (ID)
  - Protect (PR)
  - Detect (DE)
  - Respond (RS)
  - Recover (RC)
  
- **Implementation Tiers**
  - Tier 1: Partial
  - Tier 2: Risk Informed
  - Tier 3: Repeatable
  - Tier 4: Adaptive

### PCI DSS v4.0
- **Requirements**
  - Build secure networks
  - Protect cardholder data
  - Vulnerability management
  - Access control
  - Monitoring and testing
  - Security policies

## Control Validation

### Automated Checks
```yaml
control_id: AC-2
control_name: Account Management
automated_checks:
  - name: Privileged account inventory
    tool: google_cloud_security
    query: check_privileged_accounts()
  - name: Account review process
    tool: bigquery_mcp
    query: account_review_frequency()
evidence_sources:
  - IAM audit logs
  - Access reviews
  - Account lifecycle data
```

### Manual Validation
```yaml
control_id: IR-4
control_name: Incident Handling
manual_checks:
  - Incident response plan documented
  - IR team trained and ready
  - Tabletop exercises conducted
evidence_required:
  - IR plan document
  - Training records
  - Exercise reports
```

### Continuous Monitoring
```yaml
control_id: SI-4
control_name: System Monitoring
continuous_checks:
  interval: daily
  metrics:
    - Log collection coverage
    - Alert rule coverage
    - Monitoring uptime
  thresholds:
    - coverage: ">= 95%"
    - uptime: ">= 99.9%"
```

## Execution Steps

### 1. Compliance Check
When action is `check`:
- Load framework requirements
- Map controls to environment
- Execute automated checks:
  - Query security configurations
  - Validate control implementation
  - Check control effectiveness
- Identify manual validations needed
- Calculate compliance scores
- Generate findings

### 2. Audit Evidence Collection
When action is `audit`:
- Define evidence requirements
- Collect automated evidence:
  - Configuration snapshots
  - Audit logs
  - Metrics and KPIs
  - Policy documents
- Package evidence by control
- Create evidence inventory
- Generate audit trail

### 3. Gap Analysis
When action is `gap`:
- Compare current state to requirements
- Identify:
  - Missing controls
  - Partial implementations
  - Control weaknesses
  - Documentation gaps
- Prioritize by risk
- Estimate remediation effort

### 4. Continuous Monitoring
When action is `monitor`:
- Set up automated checks
- Configure alerting:
  - Control failures
  - Compliance drift
  - Expiring certifications
- Track trends
- Generate dashboards

### 5. Remediation Planning
When action is `remediate`:
- Analyze gaps and findings
- Create remediation tasks:
  - Technical fixes
  - Process improvements
  - Documentation updates
  - Training needs
- Assign priorities and owners
- Set target dates
- Track progress

## Evidence Management

### Evidence Types
```yaml
technical_evidence:
  - Configuration files
  - Access logs
  - Security scans
  - Monitoring data
  
procedural_evidence:
  - Policies and procedures
  - Training records
  - Review documentation
  - Approval workflows
  
operational_evidence:
  - Incident reports
  - Change records
  - Risk assessments
  - Audit findings
```

### Evidence Package Structure
```
audit-package-2024/
├── framework-mapping.xlsx
├── control-evidence/
│   ├── AC-Access-Control/
│   ├── IR-Incident-Response/
│   └── SI-System-Information/
├── automated-reports/
├── attestations/
└── executive-summary.pdf
```

## Reporting Templates

### Compliance Status Report
```markdown
# Compliance Status Report - [Framework]

## Executive Summary
- Overall Compliance: 87%
- Critical Findings: 2
- High Priority Gaps: 5

## Control Family Status
| Family | Compliance | Findings |
|--------|------------|----------|
| Access Control | 92% | 3 |
| Incident Response | 85% | 2 |
| System Monitoring | 88% | 4 |

## Key Findings
1. **CRITICAL**: Multi-factor authentication not enforced for privileged accounts
2. **HIGH**: Incident response plan missing cloud-specific procedures

## Recommendations
[Prioritized recommendations]
```

### Attestation Document
```
ATTESTATION OF COMPLIANCE

Framework: SOC 2 Type II
Period: January 1 - December 31, 2024
Scope: Production Security Operations

We attest that security controls have been:
☑ Implemented as designed
☑ Operating effectively
☑ Monitored continuously

Exceptions noted: See Appendix A
```

## Example Workflows

### SOC 2 Compliance Check
```
/security:compliance check soc2 --scope organization --evidence-level detailed
```

### Multi-Framework Gap Analysis
```
/security:compliance gap soc2,iso27001 --risk-based --generate-tasks
```

### Generate Audit Package
```
/security:compliance audit pci-dss --period 1y --include-evidence --format audit-package
```

### Continuous Compliance Dashboard
```
/security:compliance monitor nist --scope project --automated-only
```

## Automation Features

### Control Mapping
- Framework crosswalk
- Control inheritance
- Shared evidence
- Gap correlation

### Evidence Collection
- Automated screenshots
- Log extraction
- Configuration backup
- Metric aggregation

### Compliance Scoring
```
Compliance Score = (Implemented Controls / Total Controls) × 100
Risk-Adjusted Score = Score × (1 - Average Risk Level)
Maturity Score = Implementation × Effectiveness × Documentation
```

## Integration Points

### Source Systems
- Security Command Center (SCC)
- Chronicle SIEM
- Cloud Asset Inventory
- Identity and Access Management
- Change Management System

### Output Destinations
- Google Drive for documents
- BigQuery for metrics
- Sheets for tracking
- GitHub for version control

## Quality Assurance

### Validation Checks
- Control mapping accuracy
- Evidence completeness
- Finding validity
- Remediation feasibility

### Audit Trail
- All checks logged
- Evidence timestamped
- Changes tracked
- Reviews documented

## Error Handling
- Missing evidence: Flag as gap with explanation
- Failed checks: Retry with diagnostics
- Access denied: Document and escalate
- Framework updates: Version tracking

## Related Commands
- `/security:metrics` - Compliance KPIs
- `/security:report` - Detailed reporting
- `/security:vulnerability` - Security findings
- `/security:detect` - Control monitoring