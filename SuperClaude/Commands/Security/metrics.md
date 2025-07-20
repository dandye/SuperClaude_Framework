---
allowed_tools: 
  - bigquery_mcp
  - chronicle_mcp
  - soar_mcp
  - scc_mcp
  - google_sheets_mcp
description: Generate security operations metrics, KPIs, and performance dashboards
---

# /security:metrics Command

## Purpose
Comprehensive security metrics collection, analysis, and reporting to measure SOC performance, track operational efficiency, and support data-driven decision making. This command provides visibility into security operations effectiveness through standardized KPIs and custom metrics.

## Usage
```
/security:metrics <metric_type> [options]
```

## Metric Types
- `operational`: SOC operational metrics (MTTD, MTTR, etc.)
- `detection`: Detection effectiveness and coverage
- `incident`: Incident response metrics
- `vulnerability`: Vulnerability management KPIs
- `compliance`: Compliance and audit metrics
- `threat`: Threat landscape metrics
- `dashboard`: Generate comprehensive dashboard
- `custom`: Custom metric calculation

## Options
- `--period <timeframe>`: Reporting period
  - Values: `daily`, `weekly`, `monthly`, `quarterly`, `yearly`, `custom`
  - Default: `monthly`
  
- `--start-date <date>`: Custom period start
  - Format: `YYYY-MM-DD`
  
- `--end-date <date>`: Custom period end
  - Format: `YYYY-MM-DD`
  
- `--comparison`: Include period-over-period comparison
- `--breakdown <dimension>`: Breakdown metrics by dimension
  - Values: `severity`, `source`, `analyst`, `team`, `category`
  
- `--format <format>`: Output format
  - Values: `report`, `csv`, `json`, `dashboard`, `sheets`
  - Default: `report`
  
- `--targets`: Include SLA/target comparisons
- `--trends`: Calculate trend analysis
- `--forecast`: Include metric forecasting
- `--export <destination>`: Export location

## Core Metrics

### 1. Operational Metrics
- **Mean Time to Detect (MTTD)**
  - Time from incident start to detection
  - Breakdown by detection source
  - Trend analysis
  
- **Mean Time to Respond (MTTR)**
  - Time from detection to containment
  - By severity level
  - By incident type
  
- **Mean Time to Contain (MTTC)**
  - Time to stop incident spread
  - Effectiveness measurement
  
- **Mean Time to Recover**
  - Full recovery duration
  - Business impact duration

### 2. Alert Metrics
- **Alert Volume**
  - Total alerts generated
  - By source/category
  - Peak times analysis
  
- **False Positive Rate**
  - FP percentage by rule
  - Trend over time
  - Cost impact
  
- **Alert Fidelity**
  - True positive rate
  - Alert quality score
  - Tuning effectiveness

### 3. Case Metrics
- **Case Volume**
  - Open/closed cases
  - By priority/severity
  - Assignment distribution
  
- **Case Resolution Time**
  - Average resolution
  - By case type
  - SLA compliance
  
- **Escalation Rate**
  - Tier 1 to Tier 2/3
  - By category
  - Accuracy metrics

### 4. Detection Coverage
- **MITRE ATT&CK Coverage**
  - Techniques covered
  - Coverage gaps
  - Detection confidence
  
- **Rule Performance**
  - Detection success rate
  - Rule effectiveness
  - Maintenance needs
  
- **Threat Detection Rate**
  - Known threats caught
  - Novel threat detection
  - Miss rate analysis

### 5. Team Performance
- **Analyst Productivity**
  - Cases per analyst
  - Resolution times
  - Quality scores
  
- **Skill Utilization**
  - Tier distribution
  - Training needs
  - Specialization metrics
  
- **Workload Balance**
  - Case distribution
  - Shift coverage
  - Burnout indicators

## Calculation Methods

### Time-Based Metrics
```python
MTTD = (Detection_Time - Incident_Start_Time).average()
MTTR = (Response_Complete_Time - Detection_Time).average()
MTTC = (Containment_Time - Detection_Time).average()
```

### Rate Calculations
```python
False_Positive_Rate = (False_Positives / Total_Alerts) × 100
Detection_Rate = (Detected_Incidents / Total_Incidents) × 100
SLA_Compliance = (Met_SLA / Total_Cases) × 100
```

### Efficiency Scores
```python
Alert_Efficiency = True_Positives / (True_Positives + False_Positives)
Automation_Rate = Automated_Actions / Total_Actions
Cost_Per_Incident = Total_Cost / Number_of_Incidents
```

## Execution Steps

### 1. Data Collection
- Query relevant time period
- Gather from sources:
  - Chronicle SIEM logs
  - SOAR case data
  - SCC findings
  - Incident tickets
  - Team timesheets
- Validate data quality
- Handle missing data

### 2. Metric Calculation
- Apply calculation formulas
- Aggregate by dimensions
- Calculate:
  - Averages
  - Percentiles (P50, P90, P99)
  - Standard deviations
  - Trends
- Identify outliers
- Apply business rules

### 3. Comparison Analysis
- Compare to:
  - Previous periods
  - Targets/SLAs
  - Industry benchmarks
  - Team baselines
- Calculate deltas
- Identify improvements/degradations

### 4. Visualization
- Generate charts:
  - Time series
  - Distributions
  - Heatmaps
  - Comparisons
- Create dashboards
- Build reports

### 5. Insights Generation
- Identify patterns
- Highlight anomalies
- Suggest improvements
- Predict future trends
- Generate recommendations

## Dashboard Components

### Executive Dashboard
- High-level KPIs
- Trend indicators
- Risk posture
- Cost metrics
- Compliance status

### Operational Dashboard
- Real-time metrics
- Queue status
- SLA tracking
- Team utilization
- System health

### Analytical Dashboard
- Deep-dive metrics
- Correlation analysis
- Pattern detection
- Predictive analytics
- Benchmarking

## Example Workflows

### Monthly SOC Report
```
/security:metrics operational --period monthly --comparison --targets --format report
```

### Detection Effectiveness Analysis
```
/security:metrics detection --period quarterly --breakdown category --trends
```

### Team Performance Dashboard
```
/security:metrics dashboard --breakdown analyst --period custom --start-date 2024-01-01 --end-date 2024-01-31
```

### Executive Metrics Summary
```
/security:metrics operational --period quarterly --format dashboard --export executive-brief
```

### Custom KPI Tracking
```
/security:metrics custom --query "phishing_response_time" --period weekly --forecast
```

## Output Examples

### Operational Report
```markdown
# SOC Operational Metrics - January 2024

## Key Performance Indicators
- MTTD: 12 minutes ↓ 15% (Target: 15 min) ✓
- MTTR: 45 minutes ↑ 5% (Target: 60 min) ✓
- False Positive Rate: 18% ↓ 3% (Target: < 20%) ✓
- Case Resolution: 87% ↑ 2% (Target: 85%) ✓

## Trends
- Alert volume decreased 10% MoM
- Detection coverage improved to 78%
- Automation rate increased to 45%
```

### Performance Matrix
| Metric | Current | Previous | Target | Status |
|--------|---------|----------|--------|--------|
| MTTD | 12 min | 14 min | 15 min | ✓ |
| MTTR | 45 min | 43 min | 60 min | ✓ |
| FP Rate | 18% | 21% | <20% | ✓ |

## Automated Insights

### Anomaly Detection
- Identify metric anomalies
- Correlate with events
- Suggest root causes
- Recommend actions

### Predictive Analytics
- Forecast alert volumes
- Predict resource needs
- Estimate risk trends
- Plan capacity

## Integration Features

### Data Sources
- Chronicle SIEM analytics
- SOAR metrics API
- BigQuery custom queries
- External benchmarks

### Export Options
- Google Sheets integration
- PDF report generation
- API endpoints
- Dashboard embedding

## Quality Assurance

### Data Validation
- Completeness checks
- Outlier detection
- Consistency validation
- Source reconciliation

### Metric Accuracy
- Calculation verification
- Peer review process
- Historical validation
- Benchmark comparison

## Error Handling
- Missing data: Use interpolation or exclusion
- Calculation errors: Fallback to raw data
- API failures: Cache previous results
- Invalid periods: Suggest valid alternatives

## Related Commands
- `/security:report` - Generate detailed reports
- `/security:review` - Post-incident metrics
- `/security:detect` - Detection effectiveness
- `/security:operational` - Real-time operations