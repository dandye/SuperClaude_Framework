---
description: Add YAML frontmatter to markdown files for structured metadata
execute_immediately: true
metadata:
  type: info-arch
  category: documentation
  accepts_args: true
  arg_description: "File path or directory to add/update YAML frontmatter. If no argument provided, explains YAML frontmatter best practices."
---

{{#if args}}
Add YAML frontmatter to the file or files in: {{args}}

Analyze the content and add appropriate metadata fields based on:
- Document type (guide, reference, tutorial, etc.)
- Categories and tags from content analysis
- Creation/modification dates
- Author information if available
- Related documents
- Any existing metadata that should be preserved

If the file already has frontmatter, update it intelligently by:
- Preserving existing valid fields
- Adding missing recommended fields
- Standardizing field names to best practices
- Updating modification date

{{else}}

**Markdown with YAML Frontmatter** is a powerful combination that gives you structured metadata at the top of a human-readable document. It's widely supported (Jekyll, Hugo, Gatsby, Obsidian, many static site generators) and perfect for LLM consumption.

## Basic Structure

```markdown
---
title: API Authentication Guide
type: reference
category: security
tags: [api, authentication, oauth2, security]
created: 2024-01-15THH:MM:SSZ
modified: 2024-03-15THH:MM:SSZ
author: Security Team
version: 2.1
status: published
---

# API Authentication Guide

This document covers authentication methods for our API...
```

## YAML Frontmatter Benefits

**Structured Metadata** - YAML provides rich data types:
```yaml
---
# Scalars
title: Getting Started Guide
priority: high
word_count: 1234

# Lists
tags: [quickstart, tutorial, beginner]
authors:
  - Jane Smith
  - Bob Johnson

# Nested objects
metadata:
  audience: developers
  difficulty: beginner
  estimated_time: 30min

# Multi-line strings
description: |
  This guide helps new developers
  get up and running with our API
  in under 30 minutes.

# References to other docs
related_docs:
  - path: /api/reference.md
    relationship: extends
  - path: /tutorials/advanced.md
    relationship: next-step
---
```

## Document Organization Examples

**Content Map Entry:**
```markdown
---
type: content-map
scope: /documentation/api/
total_files: 23
last_generated: 2024-03-15T10:30:00Z
generator_version: 1.2.0
---

# API Documentation Structure

## /authentication/
- `oauth2.md` - OAuth 2.0 implementation guide
- `api-keys.md` - API key management
- `jwt.md` - JSON Web Token usage

## /endpoints/
- `users.md` - User management endpoints
- `projects.md` - Project endpoints
  - `/examples/` - Code examples for each endpoint
```

**Document Inventory Entry:**
```markdown
---
type: inventory-entry
path: /guides/authentication/oauth2.md
document_id: auth-oauth2-001
classification:
  type: guide
  category: security
  audience: [developers, architects]

metrics:
  word_count: 3456
  code_blocks: 12
  images: 3
  tables: 2

dependencies:
  requires:
    - /guides/getting-started.md
    - /references/api-basics.md
  required_by:
    - /tutorials/advanced-auth.md
    - /examples/oauth-flow.md

quality_checks:
  last_reviewed: 2024-02-28
  reviewer: security-team
  next_review: 2024-05-28
  completeness: 95
---

# OAuth 2.0 Implementation Guide

[Document content follows...]
```

**Taxonomy/Controlled Vocabulary:**
```markdown
---
type: taxonomy
domain: api-documentation
version: 1.0
last_updated: 2024-03-15
---

# API Documentation Taxonomy

## Authentication Terms
- **Primary Term**: authentication
  - *Synonyms*: auth, authn, login, sign-in
  - *Related*: authorization, security, access-control
  - *Narrower*: oauth, jwt, api-key, basic-auth

- **Primary Term**: oauth2
  - *Synonyms*: oauth-2.0, oauth 2.0
  - *Broader*: authentication
  - *Related*: authorization-code, client-credentials, refresh-token
```

**Cross-Reference Matrix:**
```markdown
---
type: cross-reference-matrix
generated: 2024-03-15
scope: /api/security/
format: references-matrix
---

# Security Documentation Cross-References

## Reference Matrix

| Document | References | Referenced By | Relationship Type |
|----------|------------|---------------|-------------------|
| auth-overview.md | oauth2.md, jwt.md, api-keys.md | getting-started.md, security-checklist.md | explains |
| oauth2.md | auth-overview.md, token-storage.md | mobile-auth.md, web-auth.md | implements |
| jwt.md | auth-overview.md, token-validation.md | microservices.md, api-gateway.md | uses |
```

## Advanced Patterns

**Multi-document Manifest:**
```markdown
---
type: manifest
documents:
  - id: guide-001
    path: /guides/quickstart.md
    title: Quick Start Guide
    status: published
    metadata:
      difficulty: beginner
      time: 15min

  - id: guide-002
    path: /guides/authentication.md
    title: Authentication Guide
    status: draft
    metadata:
      difficulty: intermediate
      time: 45min

index_settings:
  searchable_fields: [title, tags, description]
  facets: [type, status, metadata.difficulty]
  sort_options: [title, modified, metadata.difficulty]
---

# Documentation Manifest

This manifest tracks all documentation in the system...
```

**Computed Relationships:**
```markdown
---
type: document-analysis
path: /api/users.md
auto_generated: true
extracted:
  entities:
    - type: endpoint
      value: /api/v1/users
      methods: [GET, POST, PUT, DELETE]

  external_links:
    - url: https://tools.ietf.org/html/rfc7231
      context: HTTP status codes

  code_dependencies:
    - language: python
      packages: [requests, json]
    - language: javascript
      packages: [axios, fetch]

  cross_references:
    internal:
      - ./authentication.md#api-keys
      - ../models/user.md
    external:
      - https://example.com/api/v1/users
---
```

## Best Practices for LLM Consumption

1. **Consistent Field Names** - Always use the same field names across documents
2. **Type Indicators** - Include a `type` field to help LLMs understand the document's purpose
3. **ISO Dates** - Use ISO 8601 format for all dates: `2024-03-15T10:30:00Z`
4. **Explicit Relationships** - Don't rely on implicit connections; state them clearly
5. **Version Everything** - Include version numbers for both documents and schemas
6. **Validation Schema** - Consider creating a schema document that defines valid values:

```markdown
---
type: schema-definition
version: 1.0
fields:
  type:
    required: true
    values: [guide, reference, tutorial, api, example]
  status:
    required: true
    values: [draft, review, published, deprecated]
  difficulty:
    required: false
    values: [beginner, intermediate, advanced]
---
```

This format is ideal because:
- **LLMs can easily parse** both the YAML and Markdown sections
- **Humans can read it** without special tools
- **Tools support it** widely (GitHub renders it nicely, for example)
- **It's extensible** - you can add new fields without breaking existing parsers
- **It separates concerns** - metadata vs. content are clearly delineated

{{/if}}