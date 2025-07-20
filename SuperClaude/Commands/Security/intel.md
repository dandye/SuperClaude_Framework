---
allowed_tools: 
  - gti_mcp
  - chronicle_mcp
  - bigquery_mcp
  - github_mcp
  - soar_mcp
description: Manage threat intelligence collections, feeds, and indicator lifecycle
---

# /security:intel Command

## Purpose
Comprehensive threat intelligence management for collecting, normalizing, enriching, and operationalizing threat data from multiple sources. This command enables SOC teams to maintain high-quality, actionable threat intelligence that enhances detection and response capabilities.

## Usage
```
/security:intel <action> [target] [options]
```

## Actions
- `import`: Import threat intelligence from various sources
- `enrich`: Enrich indicators with additional context
- `dedupe`: Deduplicate and normalize indicators
- `score`: Calculate indicator confidence scores
- `search`: Search threat intelligence database
- `export`: Export indicators to detection/blocking
- `track`: Track indicator lifecycle and usage
- `report`: Generate threat intelligence reports

## Arguments
- `action` (required): The intelligence management action
- `target` (conditional): Source, collection, or indicator
  - For import: Source name or file
  - For enrich/score: Collection ID or indicator
  - For search: Search query
  - For export: Destination system

## Options
- `--source-type <type>`: Intelligence source type
  - Values: `feed`, `report`, `collection`, `incident`, `osint`
  - Default: Auto-detected
  
- `--indicator-types <types>`: Comma-separated indicator types
  - Values: `ip`, `domain`, `hash`, `url`, `email`, `cve`
  - Default: All types
  
- `--confidence-model <model>`: Confidence scoring model
  - Values: `source-based`, `age-based`, `corroboration`, `combined`
  - Default: `combined`
  
- `--age-limit <days>`: Maximum indicator age
  - Default: `90`
  
- `--min-confidence <score>`: Minimum confidence threshold
  - Range: 0-100
  - Default: `50`
  
- `--auto-expire`: Enable automatic expiration
- `--correlate`: Correlate with existing intel
- `--operationalize`: Auto-create detections/blocks
- `--batch-size <number>`: Processing batch size

## Intelligence Sources

### External Feeds
- **Commercial Feeds**
  - Vendor threat feeds
  - Industry-specific intel
  - Geographic threats
  
- **Open Source (OSINT)**
  - Abuse databases
  - Threat lists
  - Research publications
  
- **Government Sources**
  - CISA alerts
  - Sector warnings
  - Nation-state intel

### Internal Sources
- **Incident Data**
  - IOCs from incidents
  - Attack patterns
  - Custom indicators
  
- **Hunt Findings**
  - Discovered threats
  - Behavioral patterns
  - Environmental specific

### Platform Intelligence
- **Google Threat Intelligence**
  - Collections
  - Threat actors
  - Campaigns
  - Malware families

## Intelligence Lifecycle

### 1. Collection Phase
```yaml
collection:
  sources:
    - name: "GTI Collections"
      type: platform
      api: gti_mcp
    - name: "OSINT Feeds"
      type: external
      format: STIX
    - name: "Incident IOCs"
      type: internal
      source: SOAR
  
  ingestion:
    - Parse format
    - Extract indicators
    - Capture metadata
    - Initial validation
```

### 2. Processing Phase
```yaml
processing:
  normalization:
    - Standardize formats
    - Clean data
    - Remove duplicates
    - Fix encoding
  
  enrichment:
    - Add context
    - Resolve relationships
    - GeoIP lookup
    - WHOIS data
  
  correlation:
    - Link related indicators
    - Find patterns
    - Build graphs
    - Identify campaigns
```

### 3. Analysis Phase
```yaml
analysis:
  scoring:
    source_reputation: 30%
    corroboration: 25%
    age_factor: 15%
    relevance: 20%
    accuracy_history: 10%
  
  categorization:
    - Threat type
    - Target industry
    - Attack phase
    - Actor attribution
```

### 4. Operationalization
```yaml
operationalization:
  detection:
    - Create YARA-L rules
    - Update watchlists
    - Deploy signatures
  
  blocking:
    - Firewall rules
    - EDR blocks
    - Email filters
  
  hunting:
    - Hunt queries
    - Retro-hunts
    - Pivot searches
```

## Execution Steps

### 1. Import Intelligence
When action is `import`:
- Connect to source
- Fetch new intelligence:
  - Check last import timestamp
  - Apply filters
  - Download data
- Parse indicators:
  - Extract IOCs
  - Preserve context
  - Validate format
- Store in database:
  - Assign unique IDs
  - Track source
  - Set initial confidence

### 2. Enrich Indicators
When action is `enrich`:
- Load indicators
- Query enrichment sources:
  - GTI for reputation
  - VirusTotal for samples
  - WHOIS for domains
  - GeoIP for locations
- Add context:
  - First/last seen
  - Associated campaigns
  - Malware families
  - Kill chain phase
- Update confidence scores

### 3. Deduplication
When action is `dedupe`:
- Identify duplicates:
  - Exact matches
  - Fuzzy matching
  - Relationship-based
- Merge intelligence:
  - Combine contexts
  - Preserve sources
  - Update confidence
- Remove redundancy:
  - Keep highest fidelity
  - Archive duplicates
  - Update references

### 4. Confidence Scoring
```python
def calculate_confidence(indicator):
    scores = []
    
    # Source reputation (0-100)
    source_score = get_source_reputation(indicator.source)
    scores.append(source_score * 0.3)
    
    # Corroboration (0-100)
    corroboration = count_confirming_sources(indicator)
    scores.append(min(corroboration * 20, 100) * 0.25)
    
    # Age factor (0-100)
    age_days = (now() - indicator.first_seen).days
    age_score = max(0, 100 - (age_days * 0.5))
    scores.append(age_score * 0.15)
    
    # Relevance (0-100)
    relevance = calculate_environmental_relevance(indicator)
    scores.append(relevance * 0.2)
    
    # Historical accuracy (0-100)
    accuracy = get_source_accuracy_rate(indicator.source)
    scores.append(accuracy * 0.1)
    
    return sum(scores)
```

### 5. Search and Query
When action is `search`:
- Parse search query
- Search across:
  - Indicator values
  - Metadata
  - Relationships
  - Context
- Apply filters:
  - Time range
  - Confidence level
  - Source
  - Type
- Return ranked results

### 6. Export and Deploy
When action is `export`:
- Select indicators:
  - Apply confidence threshold
  - Check age limits
  - Validate relevance
- Format for destination:
  - STIX for sharing
  - YARA-L for Chronicle
  - CSV for analysis
  - API for automation
- Deploy to systems:
  - Detection rules
  - Blocklists
  - Watchlists
- Track deployment

## Intelligence Formats

### STIX 2.1 Format
```json
{
  "type": "indicator",
  "id": "indicator--12345",
  "pattern": "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
  "pattern_type": "stix",
  "valid_from": "2024-01-20T00:00:00.000Z",
  "confidence": 85,
  "labels": ["malicious-activity"],
  "external_references": [{
    "source_name": "GTI",
    "external_id": "GTI-MAL-12345"
  }]
}
```

### Internal Format
```yaml
indicator:
  value: "malicious.example.com"
  type: "domain"
  confidence: 78
  sources:
    - name: "GTI"
      collection: "APT-X-Infrastructure"
      first_seen: "2024-01-15"
  context:
    malware_families: ["Emotet", "TrickBot"]
    campaigns: ["CAMP-2024-001"]
    ttps: ["T1071", "T1566"]
  metadata:
    import_date: "2024-01-20"
    last_enriched: "2024-01-20"
    expiration: "2024-04-20"
```

## Example Workflows

### Import Threat Feed
```
/security:intel import threat-feed-xyz --source-type feed --auto-expire --correlate
```

### Enrich Campaign IOCs
```
/security:intel enrich GTI-COLLECTION-123 --confidence-model combined --min-confidence 70
```

### Deduplicate Database
```
/security:intel dedupe --indicator-types ip,domain --age-limit 180
```

### Search for APT Infrastructure
```
/security:intel search "APT28 infrastructure" --indicator-types ip,domain --min-confidence 80
```

### Export High-Confidence IOCs
```
/security:intel export chronicle-watchlist --min-confidence 85 --operationalize
```

### Generate Intel Report
```
/security:intel report --period monthly --source-type all --format pdf
```

## Quality Management

### Source Reliability Tracking
```yaml
source_metrics:
  name: "ThreatFeed-ABC"
  total_indicators: 10000
  true_positives: 8500
  false_positives: 500
  unverified: 1000
  reliability_score: 94.4%
  last_updated: "2024-01-20"
```

### Indicator Lifecycle
- **Active**: Currently operational
- **Expired**: Past useful life
- **Deprecated**: Replaced by better intel
- **False Positive**: Verified benign
- **Archived**: Historical reference

### Feedback Loop
1. Track indicator usage
2. Monitor detection rates
3. Collect analyst feedback
4. Update confidence scores
5. Improve source ratings

## Integration Features

### Platform Integration
- Chronicle watchlists
- Detection rule updates
- SOAR enrichment
- Hunting queries

### Sharing Mechanisms
- STIX/TAXII feeds
- API endpoints
- Email reports
- Slack notifications

## Output Examples

### Intelligence Summary Report
```markdown
# Threat Intelligence Summary - January 2024

## Key Metrics
- New Indicators: 1,234
- Active Indicators: 45,678
- High Confidence: 12,345 (27%)
- Detections Generated: 89

## Top Threats
1. **APT-X Campaign**
   - Indicators: 234
   - Confidence: 92%
   - Target: Financial sector

2. **Ransomware Infrastructure**
   - Indicators: 456
   - Confidence: 87%
   - Active campaigns: 3

## Source Performance
| Source | Indicators | TP Rate | Reliability |
|--------|-----------|---------|-------------|
| GTI | 5,000 | 95% | Excellent |
| OSINT-1 | 2,000 | 78% | Good |
| Internal | 500 | 99% | Excellent |
```

## Error Handling
- Import failures: Queue for retry
- Enrichment errors: Use cached data
- Scoring conflicts: Apply conservative score
- Export failures: Generate error report

## Related Commands
- `/security:enrich` - IOC enrichment workflows
- `/security:hunt` - Use intel for hunting
- `/security:detect` - Create detections from intel
- `/security:report` - Intelligence reporting