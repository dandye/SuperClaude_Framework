---
allowed_tools: 
  - chronicle_mcp
  - soar_mcp
  - gti_mcp
  - github_mcp
  - google_docs_mcp
description: Conduct structured post-incident reviews to capture lessons learned and improve security posture
---

# /security:review Command

## Purpose
Facilitate comprehensive post-incident reviews (PIR) to analyze incident response effectiveness, identify improvements, capture lessons learned, and update security processes. This command ensures continuous improvement of security operations through systematic review and documentation.

## Usage
```
/security:review <incident_id> [options]
```

## Arguments
- `incident_id` (required): The incident identifier to review
  - Examples: `INC-2024-001`, `CASE-789`, `SEC-INCIDENT-456`

## Options
- `--review-type <type>`: Type of review to conduct
  - Values: `quick`, `standard`, `comprehensive`, `executive`
  - Default: `standard`
  
- `--timeline-start <datetime>`: Override incident start time
  - Format: `YYYY-MM-DD HH:MM:SS`
  - Default: Incident creation time
  
- `--timeline-end <datetime>`: Override incident end time
  - Format: `YYYY-MM-DD HH:MM:SS`
  - Default: Incident closure time
  
- `--participants <list>`: Comma-separated list of review participants
  - Default: Auto-detected from incident responders
  
- `--focus-areas <list>`: Specific areas to focus review on
  - Values: `detection`, `response`, `communication`, `tools`, `process`
  - Default: All areas
  
- `--generate-actions`: Generate actionable improvement items
- `--update-runbooks`: Propose runbook updates based on findings
- `--calculate-metrics`: Calculate and compare incident metrics
- `--executive-summary`: Generate executive-friendly summary

## Review Components

### 1. Incident Timeline Reconstruction
- Collect all events and actions
- Identify key milestones:
  - Initial detection/alert
  - Triage completion
  - Escalation points
  - Containment actions
  - Eradication steps
  - Recovery milestones
  - Closure
- Calculate time intervals
- Identify delays or gaps

### 2. Response Effectiveness Analysis
- **Detection Effectiveness**
  - How was incident detected?
  - Time to detection (TTD)
  - Detection rule performance
  - Missed indicators
  
- **Triage Quality**
  - Initial assessment accuracy
  - Severity classification
  - Escalation decisions
  - False positive analysis
  
- **Investigation Depth**
  - Scope identification
  - Root cause analysis
  - Evidence collection
  - Attribution accuracy

### 3. Process Evaluation
- **Runbook Adherence**
  - Steps followed vs skipped
  - Deviations and reasons
  - Runbook effectiveness
  - Missing procedures
  
- **Tool Performance**
  - Tool availability
  - Performance issues
  - Missing capabilities
  - Integration gaps
  
- **Communication Flow**
  - Stakeholder notifications
  - Update frequency
  - Escalation effectiveness
  - Documentation quality

### 4. Impact Assessment
- **Business Impact**
  - Services affected
  - Downtime duration
  - Data exposure
  - Financial impact
  
- **Security Impact**
  - Assets compromised
  - Data exfiltrated
  - Persistence achieved
  - Lateral movement

### 5. Lessons Learned
- **What Went Well**
  - Effective detections
  - Quick responses
  - Good decisions
  - Tool successes
  
- **What Needs Improvement**
  - Detection gaps
  - Process failures
  - Communication issues
  - Tool limitations
  
- **Near Misses**
  - Almost-problems
  - Lucky breaks
  - Close calls

## Execution Steps

### 1. Data Collection Phase
- Query incident details from SOAR
- Collect all related cases and alerts
- Gather response actions timeline
- Extract communication logs
- Compile metrics and KPIs

### 2. Analysis Phase
- Reconstruct complete timeline
- Analyze each response phase:
  - Preparation effectiveness
  - Identification accuracy
  - Containment speed
  - Eradication completeness
  - Recovery validation
  - Lessons capture
- Compare against benchmarks
- Identify improvement areas

### 3. Review Meeting Preparation
- Generate timeline visualization
- Prepare metrics dashboard
- Draft initial findings
- Create discussion topics
- Prepare question lists

### 4. Action Item Generation
- Categorize improvements:
  - Immediate fixes
  - Short-term improvements
  - Long-term projects
- Assign priorities
- Estimate effort
- Set deadlines
- Assign owners

### 5. Documentation Updates
- Update relevant runbooks
- Enhance detection rules
- Improve response procedures
- Update contact lists
- Revise escalation criteria

## Output Templates

### Standard Review Report
```markdown
# Post-Incident Review: [INCIDENT_ID]

## Executive Summary
- Incident Type: [Type]
- Severity: [Level]
- Duration: [Time]
- Business Impact: [Summary]

## Timeline Analysis
- Detection: [Time] via [Method]
- Containment: [Time] ([Duration] from detection)
- Resolution: [Time] ([Total Duration])

## Key Findings
### What Went Well
- [Success points]

### Areas for Improvement
- [Improvement areas]

## Action Items
1. [High Priority Actions]
2. [Medium Priority Actions]
3. [Low Priority Actions]

## Metrics Comparison
- MTTD: [Current] vs [Benchmark]
- MTTR: [Current] vs [Benchmark]
```

### Executive Summary Format
- One-page overview
- Key metrics only
- Major findings
- Critical actions
- Business impact focus

## Improvement Tracking

### Action Item Template
```yaml
action_id: PIR-2024-001-ACT-01
title: "Improve detection for lateral movement"
category: detection
priority: high
effort: medium
owner: detection-team
due_date: 2024-03-01
status: pending
details: |
  Enhance detection rules to catch specific 
  lateral movement techniques observed in incident
```

### Metrics Tracking
- Track implementation progress
- Measure improvement impact
- Compare future incidents
- Validate effectiveness

## Integration with Runbooks

### Primary Runbook
- `post_incident_review.md`: Core PIR process

### Update Targets
- Incident response runbooks
- Detection tuning guides
- Communication templates
- Tool configuration docs

## Example Workflows

### Quick Review (Minor Incident)
```
/security:review INC-2024-100 --review-type quick --generate-actions
```

### Standard Review
```
/security:review CASE-2024-050 --calculate-metrics --update-runbooks
```

### Comprehensive Executive Review
```
/security:review SEC-INCIDENT-001 --review-type comprehensive --executive-summary --participants "CISO,SOC-Manager,IR-Lead"
```

### Focused Process Review
```
/security:review INC-2024-200 --focus-areas detection,communication --generate-actions
```

## Quality Checkpoints

### Review Completeness
- All phases analyzed
- All participants included
- Metrics calculated
- Actions generated
- Documentation updated

### Action Item Quality
- Specific and measurable
- Assigned owners
- Realistic deadlines
- Clear success criteria
- Tracked to completion

## Automation Features

### Auto-Timeline Generation
- Query all system logs
- Correlate events
- Generate visualization
- Identify gaps

### Metric Calculation
- Pull performance data
- Calculate KPIs
- Compare benchmarks
- Trend analysis

### Runbook Updates
- Identify gaps in procedures
- Propose specific changes
- Generate update PRs
- Track approvals

## Error Handling
- Missing incident data: Use available partial data
- Incomplete timeline: Highlight gaps for discussion
- No benchmarks available: Use industry standards
- Conflicting information: Present all perspectives

## Related Commands
- `/security:investigate` - Initial incident investigation
- `/security:respond` - Incident response execution
- `/security:metrics` - Ongoing metrics tracking
- `/security:report` - Generate detailed reports