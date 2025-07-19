---
allowed_tools:
  - chronicle_mcp
  - google_cloud_security
  - bigquery_mcp
  - soar_mcp
description: Generate comprehensive security reports for various audiences and purposes
---

# /security:report Command

## Purpose
Generate standardized security reports for incidents, investigations, threat hunts, and operational metrics. Supports multiple formats and audience-specific content tailoring.

## Usage
```
/security:report <report_type> [options]
```

## Arguments
- `report_type` (required): Type of report to generate
  - Values: `incident`, `investigation`, `hunt`, `triage`, `metrics`, `executive`, `compliance`

## Options
- `--case-id <id>`: Associated case/incident ID
  - Required for: incident, investigation, triage reports
  
- `--timeframe <period>`: Report coverage period
  - Format: `24h`, `7d`, `30d`, `quarter`, `custom:YYYY-MM-DD to YYYY-MM-DD`
  - Default: Varies by report type
  
- `--format <output_format>`: Output format
  - Values: `markdown`, `pdf`, `json`, `html`, `docx`
  - Default: `markdown`
  
- `--audience <target_audience>`: Tailor content for audience
  - Values: `technical`, `executive`, `legal`, `compliance`, `customer`
  - Default: `technical`
  
- `--template <template_name>`: Use specific template
  - Values: `standard`, `detailed`, `summary`, `custom:<path>`
  - Default: `standard`
  
- `--include <sections>`: Sections to include
  - Values: `timeline`, `iocs`, `recommendations`, `metrics`, `evidence`
  - Format: Comma-separated list
  
- `--redact`: Redact sensitive information
- `--sign`: Add digital signature
- `--distribute`: Auto-distribute to stakeholders

## Report Types

### 1. Incident Report
Comprehensive documentation of security incidents following PICERL lifecycle.

#### Sections:
- **Executive Summary**: High-level overview, impact, and response
- **Incident Details**: Classification, timeline, scope
- **Technical Analysis**: Root cause, attack vectors, TTPs
- **Response Actions**: Containment, eradication, recovery steps
- **Evidence Summary**: Key findings and artifacts
- **Recommendations**: Preventive measures and improvements
- **Metrics**: MTTD, MTTC, MTTR, impact assessment
- **Appendices**: IOCs, logs, screenshots

#### Example:
```
/security:report incident --case-id INC-2024-001 --audience executive --format pdf
```

### 2. Investigation Report
Detailed findings from security investigations.

#### Sections:
- **Investigation Summary**: Objectives, scope, methodology
- **Findings**: Discovered threats, compromises, vulnerabilities
- **Evidence Analysis**: Technical details, forensic findings
- **Timeline Reconstruction**: Chronological event sequence
- **Attribution**: Threat actor analysis if applicable
- **Impact Assessment**: Business and technical impact
- **Recommendations**: Security improvements
- **Supporting Evidence**: Technical appendices

#### Example:
```
/security:report investigation --case-id INV-789 --include timeline,evidence
```

### 3. Hunt Report
Results from proactive threat hunting activities.

#### Sections:
- **Hunt Overview**: Hypothesis, scope, methodology
- **Discoveries**: New threats, gaps, anomalies
- **Detection Opportunities**: New rules and monitoring
- **Statistical Analysis**: Hunt metrics and coverage
- **Risk Assessment**: Identified vulnerabilities
- **Recommendations**: Defensive improvements
- **Hunt Artifacts**: Queries, scripts, IOCs

#### Example:
```
/security:report hunt --timeframe 30d --template detailed
```

### 4. Triage Report
Summary of alert triage activities and outcomes.

#### Sections:
- **Triage Summary**: Alerts processed, outcomes
- **True Positives**: Confirmed threats requiring action
- **False Positives**: Benign alerts and tuning needs
- **Escalations**: Cases requiring investigation
- **Metrics**: Triage efficiency, accuracy
- **Tuning Recommendations**: Alert optimization

#### Example:
```
/security:report triage --timeframe 7d --format json
```

### 5. Metrics Report
Operational metrics and KPIs for security operations.

#### Sections:
- **Operational Metrics**: Alert volumes, response times
- **Performance KPIs**: SLA compliance, efficiency
- **Threat Landscape**: Attack trends, top threats
- **Team Performance**: Analyst productivity, case metrics
- **Tool Utilization**: Platform usage, automation rates
- **Trend Analysis**: Historical comparisons
- **Recommendations**: Process improvements

#### Example:
```
/security:report metrics --timeframe quarter --audience executive
```

### 6. Executive Report
High-level security posture and incident summaries.

#### Format Features:
- Visual dashboards
- Risk heat maps
- Trend charts
- Business impact focus
- Non-technical language
- Action priorities

#### Example:
```
/security:report executive --timeframe 30d --format pdf --distribute
```

### 7. Compliance Report
Regulatory and compliance-focused reporting.

#### Sections:
- **Compliance Status**: Framework adherence
- **Incident Notifications**: Breach reporting requirements
- **Control Effectiveness**: Security control validation
- **Audit Findings**: Issues and remediation
- **Evidence Collection**: Compliance artifacts
- **Certification Status**: Current certifications

#### Example:
```
/security:report compliance --template gdpr --timeframe quarter
```

## Report Templates

### Standard Template
```yaml
structure:
  - Executive Summary (1 page)
  - Detailed Findings (5-10 pages)
  - Technical Appendices
  - Recommendations
```

### Detailed Template
```yaml
structure:
  - Comprehensive Analysis
  - Full Evidence Documentation
  - Extended Technical Details
  - Implementation Guides
```

### Summary Template
```yaml
structure:
  - 1-2 Page Overview
  - Key Findings Only
  - Critical Recommendations
  - Next Steps
```

## Automated Elements

### Data Collection
- Query relevant data sources
- Aggregate metrics
- Compile evidence
- Generate visualizations

### Content Generation
- Auto-summarize findings
- Extract key insights
- Generate recommendations
- Create executive summaries

### Quality Checks
- Completeness validation
- Accuracy verification
- Consistency checking
- Sensitive data scanning

## Distribution Options

### Email Distribution
```yaml
executive_report:
  - CISO
  - Security Leadership
  - Risk Committee

technical_report:
  - SOC Team
  - Engineering
  - Architecture
```

### Repository Storage
- SharePoint/Confluence
- Case management system
- Compliance portal
- Secure file share

## Customization

### Custom Sections
```
--include custom:risk_matrix,cost_analysis,recovery_timeline
```

### Branding
- Company logos
- Color schemes
- Font preferences
- Header/footer

### Localization
- Language support
- Regional compliance
- Time zone handling
- Currency formatting

## Related Commands
- `/security:investigate` - Generate investigation data
- `/security:triage` - Triage metrics source
- `/security:hunt` - Hunt findings source
- `/security:respond` - Incident data source