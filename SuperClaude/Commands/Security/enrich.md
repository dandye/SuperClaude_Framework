---
allowed_tools:
  - gti_mcp
  - chronicle_mcp
  - google_cloud_security
  - bigquery_mcp
description: Enrich indicators of compromise (IOCs) with threat intelligence and context
---

# /security:enrich Command

## Purpose
Enrich security indicators (IOCs) with comprehensive threat intelligence, historical context, and risk assessments. This command provides deep context for IPs, domains, hashes, URLs, and other indicators to support investigation and response decisions.

## Usage
```
/security:enrich <indicator> [options]
# or
/security:enrich --file <ioc_file> [options]
```

## Arguments
- `indicator`: Single indicator to enrich
  - IP addresses: `192.168.1.1`, `2001:db8::1`
  - Domains: `malicious.com`, `subdomain.example.org`
  - Hashes: MD5, SHA1, SHA256
  - URLs: `http://malicious.com/payload.exe`
  - Email addresses: `threat@actor.com`
  - File paths: `C:\Windows\Temp\evil.exe`

## Options
- `--file <path>`: Bulk enrich IOCs from file
  - Formats: `txt` (one per line), `csv`, `json`
  
- `--type <ioc_type>`: Specify indicator type
  - Values: `ip`, `domain`, `hash`, `url`, `email`, `filepath`
  - Default: Auto-detected
  
- `--depth <level>`: Enrichment depth
  - Values: `basic`, `standard`, `deep`, `maximum`
  - Default: `standard`
  
- `--sources <source_list>`: Specific intel sources
  - Values: `gti`, `chronicle`, `osint`, `internal`, `all`
  - Default: `all`
  
- `--historical <period>`: Historical lookback
  - Format: `7d`, `30d`, `90d`, `1y`, `all`
  - Default: `90d`
  
- `--context <type>`: Additional context
  - Values: `related`, `campaign`, `actor`, `malware`
  - Default: All available
  
- `--risk-score`: Calculate composite risk score
- `--pivot`: Find related indicators
- `--export <format>`: Export results (`json`, `csv`, `stix`)

## Enrichment Categories

### 1. Threat Intelligence
Source: Google Threat Intelligence (GTI)
- **Reputation**: Malicious, suspicious, benign
- **Categories**: Malware, phishing, C2, exploit kit
- **Confidence**: High, medium, low
- **First/Last Seen**: Temporal context
- **Prevalence**: Global observation frequency

### 2. Historical Context
Source: Chronicle SIEM
- **Previous Observations**: When/where seen
- **Associated Incidents**: Related cases
- **Affected Assets**: Impacted systems
- **User Associations**: Connected identities
- **Frequency Analysis**: Occurrence patterns

### 3. Infrastructure Analysis
- **Hosting Provider**: ASN, geolocation
- **Domain Registration**: WHOIS data
- **SSL Certificates**: Certificate details
- **DNS History**: Resolution changes
- **Network Neighbors**: Co-hosted sites

### 4. Behavioral Analysis
- **Communication Patterns**: Beaconing, protocols
- **File Characteristics**: Type, size, entropy
- **Execution Context**: Process trees, behaviors
- **Persistence Methods**: Installation tactics
- **Evasion Techniques**: Anti-analysis methods

### 5. Attribution & Campaigns
- **Threat Actor**: Known group associations
- **Campaign**: Linked attack campaigns
- **TTPs**: MITRE ATT&CK mapping
- **Target Industries**: Victimology
- **Related Incidents**: Global correlations

## Enrichment Workflows

### Single IOC Enrichment
```
Input: 192.168.1.100
Output:
{
  "indicator": "192.168.1.100",
  "type": "ip",
  "reputation": {
    "score": 85,
    "category": "malicious",
    "confidence": "high"
  },
  "threat_intel": {
    "source": "GTI",
    "tags": ["c2", "cobalt_strike"],
    "first_seen": "2024-01-15",
    "last_seen": "2024-01-18",
    "prevalence": "medium"
  },
  "historical": {
    "observations": 47,
    "incidents": ["INC-2024-001", "INC-2024-003"],
    "affected_hosts": 12
  },
  "infrastructure": {
    "asn": "AS12345",
    "country": "RU",
    "hosting": "BadHost LLC"
  },
  "attribution": {
    "actor": "APT29",
    "confidence": "medium",
    "campaign": "SOLARWINDS"
  }
}
```

### Bulk IOC Processing
```bash
# Input file format
cat iocs.txt
192.168.1.100
malicious.com
5d41402abc4b2a76b9719d911017c592

# Enrichment command
/security:enrich --file iocs.txt --depth deep --export results.json
```

### Risk Scoring Algorithm
```yaml
risk_factors:
  reputation_score: 40%  # GTI reputation
  prevalence: 20%       # How common/rare
  infrastructure: 15%   # Hosting/registration
  historical: 15%       # Previous incidents
  attribution: 10%      # Known actors

risk_levels:
  critical: 90-100     # Immediate action
  high: 70-89         # Rapid response
  medium: 40-69       # Investigation needed
  low: 0-39           # Monitor
```

## Advanced Features

### 1. Pivoting
Discover related indicators:
```
/security:enrich malicious.com --pivot
```
Finds:
- Other domains on same IP
- Subdomains
- Similar domain names
- Related hashes
- Connected infrastructure

### 2. Campaign Correlation
Link to known campaigns:
```
/security:enrich <hash> --context campaign
```
Returns:
- Campaign name
- Attack timeline
- Other indicators
- Victim profiles
- Actor TTPs

### 3. Predictive Analysis
- **Next Actions**: Likely adversary steps
- **Target Prediction**: Potential victims
- **Evolution**: How threats may change
- **Defensive Priorities**: Key mitigations

## Integration Examples

### With Triage
```
/security:triage CHR-2024-001
# Alert contains suspicious IP

/security:enrich 192.168.1.100 --depth deep
# Enrichment reveals known C2 server
```

### With Investigation
```
/security:investigate CASE-2024-001
# Investigation finds unknown hash

/security:enrich 5d41402abc4b2a76b9719d911017c592
# Enrichment links to APT campaign
```

### With Hunting
```
/security:hunt --ttp T1071
# Hunt discovers suspicious domains

/security:enrich --file suspicious_domains.txt --pivot
# Enrichment reveals infrastructure cluster
```

## Output Formats

### Standard Output
Human-readable format with:
- Summary section
- Detailed findings
- Recommendations
- Related indicators

### JSON Export
```json
{
  "enrichment_results": [...],
  "metadata": {
    "timestamp": "2024-01-19T10:00:00Z",
    "sources": ["gti", "chronicle"],
    "version": "1.0"
  }
}
```

### STIX Bundle
Threat intelligence in STIX 2.1 format for sharing

### CSV Export
Tabular format for analysis:
| Indicator | Type | Risk | Category | First Seen | Actor |
|-----------|------|------|----------|------------|-------|

## Performance Optimization

### Caching
- Recent enrichments cached for 24h
- Reduces API calls
- Improves response time
- Cache invalidation on new intel

### Batch Processing
- Bulk operations optimized
- Parallel enrichment
- Rate limiting respected
- Progress reporting

## Use Cases

### 1. Alert Triage
Quickly assess indicator risk during alert triage

### 2. Incident Response
Deep context for incident indicators

### 3. Threat Hunting
Enrich discovered anomalies

### 4. Intelligence Analysis
Build threat actor profiles

### 5. Preventive Defense
Proactive blocking decisions

## Related Commands
- `/security:triage` - Enrichment during triage
- `/security:investigate` - Deep investigation
- `/security:hunt` - Hunting support
- `/security:report` - Include in reports