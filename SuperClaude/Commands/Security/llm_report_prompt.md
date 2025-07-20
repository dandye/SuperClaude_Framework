# Security Report Generation Prompt

You are tasked with generating a comprehensive security report based on the execution of a security runbook. Follow the guidelines from the AI Runbooks project for consistent, high-quality security documentation.

## Report Guidelines

You MUST follow these guidelines from `rules_bank/run_books/guidelines/report_writing.md`:

### Report Structure
1. **Report Metadata** - Essential details about the report
2. **Executive Summary** - High-level overview for decision makers
3. **Workflow Diagram** - Mermaid sequence diagram showing the process
4. **Detailed Findings** - Key facts, decisions, and analysis
5. **Timeline** - Chronological sequence of events
6. **Indicators of Compromise (IOCs)** - If applicable
7. **Recommendations** - Next steps and remediation
8. **Performance Metrics** - Execution statistics

### Critical Requirements
- **ALWAYS include a Mermaid sequence diagram** showing the workflow
- Use appropriate tone for the target audience
- Provide actionable recommendations
- Include all discovered IOCs in structured format
- Show execution timeline with durations
- Highlight key decisions made during investigation

### Mermaid Diagram Requirements
Create a sequence diagram that shows:
- Participants: Analyst, System, and relevant tools (Chronicle SIEM, Google Threat Intelligence, SOAR Platform)
- Each step of the workflow with tool interactions
- Decision points and their outcomes
- Final status

## Input Data

The following data represents the results of executing a security runbook:

```json
${EXECUTION_DATA}
```

## Report Generation Instructions

1. **Analyze the execution data** to understand what happened
2. **Extract key information** including facts, decisions, IOCs, and timeline
3. **Generate appropriate content** for the specified audience: ${AUDIENCE}
4. **Create a Mermaid sequence diagram** showing the workflow execution
5. **Structure the report** according to the guidelines above
6. **Ensure all sections are complete** and provide actionable insights

## Output Format

Generate a complete security report in markdown format that:
- Follows the exact structure outlined above
- Includes a properly formatted Mermaid sequence diagram
- Provides clear, actionable recommendations
- Uses professional security terminology
- Is appropriate for the ${AUDIENCE} audience
- Documents all findings comprehensively

Remember: This report may be used for compliance, incident response, or executive briefings. Ensure it meets professional security documentation standards.