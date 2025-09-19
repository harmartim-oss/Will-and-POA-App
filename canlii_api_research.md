# CanLII API Research Findings

## Overview
CanLII (Canadian Legal Information Institute) provides a comprehensive REST API that allows authorized developers to programmatically access metadata about the CanLII collection. This is perfect for integrating legal case research functionality into the Ontario Wills application.

## Key API Features

### 1. API Access
- **Type**: Read-only REST HTTP API
- **Authentication**: API key required (must apply via feedback form)
- **Data Format**: JSON structures
- **Languages**: English (en) and French (fr) supported

### 2. Core Endpoints

#### A. Case Browse API
**Get list of courts and tribunals:**
```
https://api.canlii.org/v1/caseBrowse/{language}/?api_key={key}
```

**Get decisions from specific database:**
```
https://api.canlii.org/v1/caseBrowse/{language}/{databaseId}/?offset={offset}&resultCount={resultCount}
```

**Get metadata for specific case:**
```
https://api.canlii.org/v1/caseBrowse/{language}/{databaseId}/{caseId}/?api_key={key}
```

#### B. Case Citator API
**Get citation information:**
```
https://api.canlii.org/v1/caseCitator/en/{databaseId}/{caseId}/metadataType?api_key={key}
```
- metadataType options: citedCases, citingCases, citedLegislations

#### C. Legislation Browse API
**Get legislation databases:**
```
https://api.canlii.org/v1/legislationBrowse/{language}/?api_key={key}
```

**Get specific legislation:**
```
https://api.canlii.org/v1/legislationBrowse/{language}/{databaseId}/?api_key={key}
```

### 3. Ontario-Specific Databases
Based on the API structure, Ontario courts would include:
- Ontario Court of Appeal (onca)
- Ontario Superior Court of Justice (onsc)
- Ontario Court of Justice (oncj)
- Various Ontario tribunals and boards

### 4. Search Parameters
The API supports filtering by:
- **Date ranges**: publishedBefore/After, modifiedBefore/After, changedBefore/After, decisionDateBefore/After
- **Pagination**: offset and resultCount (max 10,000)
- **Language**: English or French output

### 5. Response Structure
**Case metadata includes:**
- databaseId
- caseId
- title
- citation
- url (direct link to CanLII)
- language
- docketNumber
- decisionDate
- keywords

## Integration Strategy for Ontario Wills App

### 1. Legal Research Service
Create a service that:
- Searches for relevant estate planning and power of attorney cases
- Filters by Ontario jurisdiction
- Provides case summaries and citations
- Links to full case text on CanLII

### 2. Contextual Case Suggestions
- Analyze user's will/POA content using NLP
- Search for relevant cases based on extracted legal concepts
- Suggest precedents and legal authorities
- Provide warnings about potential issues based on case law

### 3. Citation and Authority Integration
- Automatically cite relevant Ontario legislation (Succession Law Reform Act, Substitute Decisions Act)
- Reference supporting case law for specific clauses
- Provide legal authority for document provisions

### 4. Implementation Approach
1. **API Key Application**: Apply for CanLII API access
2. **Service Layer**: Create legal research service with CanLII integration
3. **Search Interface**: Build user-friendly search interface
4. **NLP Integration**: Connect with existing NLP service for intelligent case matching
5. **Caching**: Implement caching for frequently accessed cases
6. **Rate Limiting**: Respect API limitations and implement proper rate limiting

### 5. User Experience Features
- **Smart Search**: Natural language search for legal concepts
- **Case Summaries**: AI-generated summaries of relevant cases
- **Citation Management**: Automatic citation formatting
- **Bookmark System**: Save important cases for reference
- **Recent Cases**: Track recently viewed cases
- **Related Cases**: Suggest similar or related cases

### 6. Legal Compliance Benefits
- **Authority**: Provide legal authority for document provisions
- **Precedent**: Reference established legal precedents
- **Updates**: Stay current with recent legal developments
- **Validation**: Cross-reference document provisions with case law

## Technical Implementation Notes

### API Limitations
- Read-only access (no write operations)
- Rate limiting likely applies (not specified in documentation)
- Requires API key approval process
- English-only support for citator functionality

### Data Structure
- Consistent JSON response format
- Standardized case identifiers
- Direct URLs to full case text
- Comprehensive metadata

### Integration Points
1. **Document Analysis**: Use NLP to extract legal concepts, then search for relevant cases
2. **Clause Validation**: Check specific will/POA clauses against case law
3. **Risk Assessment**: Identify potential legal issues based on case precedents
4. **Educational Content**: Provide explanations of legal concepts with case examples

This API integration will significantly enhance the legal research capabilities of the Ontario Wills application, providing users with access to authoritative legal sources and helping ensure their documents are grounded in established legal precedent.

