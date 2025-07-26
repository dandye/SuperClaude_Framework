
---
title: "Semantic Markdown: Machine-Understandable Documentation"
description: "Approaches for embedding semantic web concepts and linked data into Markdown documents"
author: "Technical Documentation Team"
date: "2024-03-15"
type: "TechnicalArticle"
tags:
  - semantic-web
  - markdown
  - linked-data
  - rdf
  - json-ld
  - documentation
categories:
  - information-architecture
  - technical-writing
keywords:
  - "semantic markdown"
  - "RDFa"
  - "JSON-LD"
  - "microdata"
  - "knowledge graphs"
  - "linked data"
version: "1.0"
license: "CC-BY-4.0"
---

# Semantic Markdown

Bringing Semantic Web concepts into Markdown. Here are several approaches to make documents machine-understandable with rich, linked data:

## 1. **RDFa-style Annotations in HTML within Markdown**

```markdown
---
@context: https://schema.org/
@type: TechnicalArticle
author:
  @type: Person
  name: Jane Smith
  url: https://example.com/people/jane
about:
  @type: SoftwareApplication
  name: MyAPI
  url: https://api.example.com
---

# API Authentication Guide

This guide covers <span property="teaches">OAuth 2.0 authentication</span> for
<span property="about" resource="https://api.example.com">MyAPI</span>.

Written by <span property="author" typeof="Person">
<span property="name">Jane Smith</span></span> on
<time property="datePublished" datetime="2024-03-15">March 15, 2024</time>.
```

## 2. **JSON-LD in YAML Frontmatter**

```markdown
---
"@context":
  "@vocab": "https://schema.org/"
  ex: "https://example.com/vocab/"
  api: "https://example.com/api/vocab#"

"@type": "TechArticle"
"@id": "https://docs.example.com/auth-guide"

name: "API Authentication Guide"
teaches:
  - "@type": "DefinedTerm"
    "@id": "https://example.com/concepts/oauth2"
    name: "OAuth 2.0"
    inDefinedTermSet: "https://example.com/vocab/auth-methods"

hasPart:
  - "@type": "HowTo"
    "@id": "#oauth-setup"
    name: "OAuth Setup"
    step:
      - "@type": "HowToStep"
        name: "Register Application"
        url: "#register-app"

mentions:
  - "@id": "https://tools.ietf.org/html/rfc6749"
    "@type": "TechArticle"
    name: "RFC 6749"

isPartOf:
  "@id": "https://docs.example.com/api-documentation"
  "@type": "CreativeWork"
  name: "API Documentation"
---

# API Authentication Guide

## <span id="oauth-setup">OAuth Setup</span>

### <span id="register-app">Register Application</span>
```

## 3. **Microdata-style Inline Semantic Markup**

```markdown
# <span itemscope itemtype="https://schema.org/TechArticle">
  <span itemprop="name">API Authentication Guide</span>
</span>

By <span itemprop="author" itemscope itemtype="https://schema.org/Person">
  <span itemprop="name">Jane Smith</span>
  (<link itemprop="sameAs" href="https://orcid.org/0000-0000-0000-0000">ORCID</link>)
</span>

This guide explains <span itemprop="about" itemscope itemtype="https://schema.org/Thing">
  <span itemprop="name">OAuth 2.0</span>
  <link itemprop="sameAs" href="https://en.wikipedia.org/wiki/OAuth#OAuth_2.0">
</span>
```

## 4. **Custom Wiki-style Link Relationships**

```markdown
---
prefixes:
  concept: "https://example.com/concepts/"
  doc: "https://example.com/docs/"
  implements: "https://example.com/vocab#implements"
  extends: "https://example.com/vocab#extends"
---

# OAuth Implementation Guide

This guide [[implements:concept:rfc6749|implements RFC 6749]] and
[[extends:doc:basic-auth|extends the Basic Auth guide]].

Prerequisites:
- [[requires:doc:api-setup|API Setup Guide]]
- [[requires:concept:http-basics|Understanding of HTTP]]

See also:
- [[relatedTo:doc:jwt-guide|JWT Authentication]] - alternative approach
- [[sameAs:https://oauth.net/2/|OAuth 2.0 Specification]] - official spec
```

## 5. **Semantic Triple Tables**

```markdown
## Document Relationships

| Subject | Predicate | Object |
|---------|-----------|---------|
| this:guide | rdf:type | schema:HowToGuide |
| this:guide | schema:about | concept:oauth2 |
| this:guide | schema:isPartOf | collection:security-guides |
| this:guide | dc:requires | doc:api-basics |
| concept:oauth2 | skos:broader | concept:authentication |
| concept:oauth2 | owl:sameAs | <https://www.wikidata.org/wiki/Q616885> |
```

## 6. **Semantic Frontmatter with Namespaces**

```markdown
---
"@namespaces":
  rdf: "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  rdfs: "http://www.w3.org/2000/01/rdf-schema#"
  schema: "https://schema.org/"
  dc: "http://purl.org/dc/terms/"
  skos: "http://www.w3.org/2004/02/skos/core#"
  ex: "https://example.com/ontology#"

"@id": "https://docs.example.com/guides/oauth"
"@type": ["schema:TechArticle", "ex:SecurityGuide"]

"dc:title": "OAuth 2.0 Implementation Guide"
"dc:creator":
  "@id": "https://example.com/people/jane"
  "schema:name": "Jane Smith"

"ex:covers":
  - "@id": "ex:OAuth2"
    "skos:prefLabel": "OAuth 2.0"
    "skos:altLabel": ["OAuth2", "OAuth 2"]
    "skos:related": ["ex:JWT", "ex:SAML"]

"ex:documentRelations":
  - predicate: "ex:requires"
    object: "https://docs.example.com/guides/api-basics"
    strength: "mandatory"
  - predicate: "ex:recommends"
    object: "https://docs.example.com/guides/security-best-practices"
    strength: "optional"
---
```

## 7. **Typed Links Pattern**

```markdown
# Authentication Guide

This guide covers [OAuth 2.0](https://example.com/concepts/oauth2){.concept rel="teaches"}
authentication for our [API](https://api.example.com){.software rel="about"}.

Prerequisites:
- [API Basics Guide](./api-basics.md){.document rel="requires"}
- [Understanding HTTP](https://example.com/concepts/http){.concept rel="requires"}

Related specs:
- [RFC 6749](https://tools.ietf.org/html/rfc6749){.specification rel="implements"}
- [OpenID Connect](https://openid.net/connect/){.specification rel="extends"}
```

## 8. **Knowledge Graph Extraction Instructions**

```markdown
---
semantic_extraction:
  entities:
    - type: Concept
      id: oauth2
      labels: ["OAuth 2.0", "OAuth2"]
      definition: "An authorization framework"
      broader: authentication

    - type: Document
      id: this
      title: "OAuth Implementation Guide"
      teaches: [oauth2]
      requires: [http-basics, api-setup]

  relationships:
    - [this, implements, rfc6749]
    - [this, isPartOf, security-documentation]
    - [oauth2, enabledBy, authorization-server]
    - [jwt, alternativeTo, oauth2]

  rules:
    - "Any mention of 'token' relates to concept:access-token"
    - "Links to RFCs imply 'implements' relationship"
---
```

## Best Practices for Semantic Markdown

1. **Use Persistent URIs** - Create stable identifiers for your concepts
2. **Define Your Vocabulary** - Document what relationships mean
3. **Layer Semantics** - Start simple, add complexity as needed
4. **Tool-Friendly Formats** - Ensure extractors can parse your markup
5. **Human-Readable Fallbacks** - Semantic markup shouldn't hurt readability

## Example Extraction Script Concept

```python
# Pseudocode for extracting triples from semantic markdown
def extract_knowledge_graph(markdown_file):
    frontmatter = parse_yaml_frontmatter(markdown_file)

    # Extract JSON-LD
    if "@context" in frontmatter:
        yield from extract_jsonld_triples(frontmatter)

    # Extract custom semantic links
    for link in find_semantic_links(markdown_file):
        yield (document_uri, link.rel, link.href)

    # Extract inline RDFa
    for span in find_rdfa_spans(markdown_file):
        yield from extract_rdfa_triples(span)
```

This approach gives you:
- **Machine-readable semantics** that LLMs and other tools can process
- **Human-readable documents** that work in any Markdown viewer
- **Queryable relationships** using SPARQL-like patterns
- **Linked data** connecting your documents to the wider web
- **Flexible complexity** - use as much or as little as you need