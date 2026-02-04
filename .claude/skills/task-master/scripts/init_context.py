#!/usr/bin/env python3
"""
Initialize project context documentation files.
Creates architecture overview, PRD, constraints, and other essential context docs.
"""

import sys
from pathlib import Path
from datetime import datetime

TEMPLATES = {
    "architecture": {
        "filename": "ARCHITECTURE.md",
        "content": """# Architecture Overview

## Application Overview

**What does this application do?**
- Primary purpose: [Describe the core problem this app solves]
- Target users: [Who uses this app?]
- Core use cases: [Key workflows]
- **What this is NOT**: [Explicit non-goals to prevent scope creep]

## High-Level Architecture

```mermaid
graph TD
    User[User/Client] --> Frontend
    Frontend --> API[API Layer]
    API --> Services[Business Logic]
    Services --> Data[(Data Layer)]
```

**Architectural Layers**:
- Presentation: [UI framework, patterns]
- Business Logic: [Services, domain models]
- Data: [Database, storage, caching]

**Communication Patterns**:
- [REST, GraphQL, WebSocket, etc.]

## Technology Stack

### Current Technologies
- **Frontend**: [Framework, libraries]
- **Backend**: [Language, framework]
- **Database**: [SQL, NoSQL, cache]
- **Infrastructure**: [Hosting, CI/CD]

### Technology Decisions
| Technology | Chosen | Alternative | Rationale |
|------------|--------|-------------|-----------|
| Frontend | [Choice] | [Alt] | [Why] |
| Backend | [Choice] | [Alt] | [Why] |

## Core Components

### Component 1: [Name]
- **Location**: `[path/to/component]`
- **Responsibility**: [What it does]
- **Dependencies**: [What it depends on]
- **Interfaces**: [How others interact with it]

### Component 2: [Name]
- **Location**: `[path/to/component]`
- **Responsibility**: [What it does]
- **Dependencies**: [What it depends on]
- **Interfaces**: [How others interact with it]

## Data Architecture

### Core Entities
- **[Entity1]**: [Description, key attributes]
- **[Entity2]**: [Description, key attributes]

**Relationships**: [How entities relate]

### Data Flow
1. [Step 1]: [Data enters from where]
2. [Step 2]: [How it's processed]
3. [Step 3]: [Where it's stored/output]

## Integration Points

### External Services
- **[Service Name]**: [Purpose, criticality]
  - API: [Endpoint/protocol]
  - Failure handling: [Strategy]

### Internal Boundaries
- Module boundaries and communication protocols
- API contracts between components

## Design Patterns & Principles

### Applied Patterns
- Architectural pattern: [MVC, MVVM, Clean Architecture, etc.]
- Common design patterns: [Singleton, Factory, Observer, etc.]

### Architecture Principles
- [Principle 1]: [How applied]
- [Principle 2]: [How applied]

## Constraints & Limitations

### Technical Constraints
- Platform: [OS versions, device requirements]
- Performance: [Response time, throughput targets]
- Scalability: [User/data limits]

### Business Constraints
- Compliance: [GDPR, HIPAA, accessibility]
- Budget: [Resource limitations]

## Current State & Roadmap

### Current State
- Implemented: [What's done]
- Technical debt: [Known issues]
- Areas needing improvement: [Gaps]

### Future Direction
- Planned changes: [Upcoming work]
- Features in pipeline: [Roadmap items]

---

**Last Updated**: {date}
**Maintainer**: [Team/Person]
"""
    },
    "prd": {
        "filename": "PRD.md",
        "content": """# Product Requirements Document

## Product Vision

**Mission**: [What problem are we solving?]

**Vision Statement**: [What do we want to achieve long-term?]

**Success Definition**: [How do we know we succeeded?]

## Target Users

### Primary Persona
- **Name**: [Persona name]
- **Background**: [Role, experience level]
- **Goals**: [What they want to achieve]
- **Pain Points**: [Current frustrations]

### Secondary Personas
- [Additional user types if applicable]

## Core Features (In Scope)

### Feature 1: [Name]
- **Priority**: [Critical/High/Medium]
- **Description**: [What it does]
- **User Value**: [Why it matters]
- **Success Metrics**: [How we measure it]

### Feature 2: [Name]
- **Priority**: [Critical/High/Medium]
- **Description**: [What it does]
- **User Value**: [Why it matters]
- **Success Metrics**: [How we measure it]

## Explicitly Out of Scope

**What We Are NOT Building**:
- [Feature/capability 1] - [Why not]
- [Feature/capability 2] - [Why not]
- [Feature/capability 3] - [Why not]

**Rationale**: [Explain scope boundaries]

## User Stories

See `USER_STORIES.md` for detailed user stories.

## Success Metrics

### Key Performance Indicators (KPIs)
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
- [Metric 3]: [Target value]

### User Satisfaction
- [How we measure user satisfaction]

## Competitive Analysis

| Competitor | Strengths | Weaknesses | Our Advantage |
|------------|-----------|------------|---------------|
| [Comp 1] | [Strengths] | [Weaknesses] | [Our edge] |
| [Comp 2] | [Strengths] | [Weaknesses] | [Our edge] |

## Market Opportunity

- Market size: [TAM, SAM, SOM]
- Growth potential: [Trends]
- Target market segment: [Who we focus on]

---

**Last Updated**: {date}
**Document Owner**: [Team/Person]
"""
    },
    "constraints": {
        "filename": "CONSTRAINTS.md",
        "content": """# Technical & Business Constraints

## Platform Constraints

### Device/OS Requirements
- **Minimum**: [OS version, device specs]
- **Recommended**: [Optimal specs]
- **Unsupported**: [Known incompatibilities]

### Browser/Client Support (if applicable)
- Supported browsers: [List with versions]
- Mobile web: [Responsive requirements]

## Performance Requirements

### Response Times
- API endpoints: [< Xms target]
- Page load: [< Xs target]
- Interactive: [< Xs target]

### Throughput
- Concurrent users: [Max supported]
- Requests per second: [Limit]

### Resource Limits
- Memory: [Max MB per process]
- Storage: [Max GB per user]
- Bandwidth: [Limits]

## Security Requirements

### Authentication
- Method: [OAuth, JWT, etc.]
- MFA: [Required/Optional]
- Session timeout: [Duration]

### Authorization
- Role-based access control: [Model]
- Permissions: [Structure]

### Data Protection
- Encryption at rest: [Algorithm, requirements]
- Encryption in transit: [TLS version]
- Sensitive data handling: [PII, payment info]

## Compliance Requirements

### Regulations
- **GDPR**: [Applicable provisions]
  - Right to deletion: [How handled]
  - Data portability: [Export format]
  - Consent management: [Mechanism]

- **Accessibility**: [WCAG level, standards]
  - Screen reader support
  - Keyboard navigation
  - Color contrast

- **Other**: [Industry-specific regulations]

## Infrastructure Constraints

### Hosting
- Provider: [AWS, GCP, Azure, on-prem]
- Regions: [Data residency requirements]
- Availability: [SLA targets]

### Scaling Limits
- Horizontal: [Max instances]
- Vertical: [Max resources per instance]
- Database: [Connection limits, size]

## Technology Restrictions

### Approved Technologies
- Languages: [Allowed]
- Frameworks: [Allowed]
- Libraries: [Whitelist]

### Prohibited Technologies
- [Banned tools/libraries] - [Reason]

### Versioning
- Language versions: [Minimum/recommended]
- Dependency management: [Policy]

## Budget Constraints

### Infrastructure Costs
- Monthly budget: [$Amount]
- Cost per user: [$Amount]
- Cost alerts: [Thresholds]

### Development Resources
- Team size: [Number]
- Timeline: [Deadline]
- Sprints: [Duration, count]

## Business Constraints

### Timeline
- MVP deadline: [Date]
- Feature milestones: [Key dates]
- Release schedule: [Frequency]

### Operational
- Support hours: [Availability]
- Maintenance windows: [When allowed]
- Deployment frequency: [Limits]

## Known Limitations

### Technical Debt
- [Issue 1]: [Impact, plan to address]
- [Issue 2]: [Impact, plan to address]

### Third-Party Dependencies
- [Service 1]: [Rate limits, costs, risks]
- [Service 2]: [Rate limits, costs, risks]

### Accepted Trade-offs
- [Trade-off 1]: [What sacrificed, why]
- [Trade-off 2]: [What sacrificed, why]

---

**Last Updated**: {date}
**Review Frequency**: [Monthly/Quarterly]
"""
    },
    "user-stories": {
        "filename": "USER_STORIES.md",
        "content": """# User Stories

## Story Format

**Template**:
```
As a [user type],
I want to [action],
So that [benefit].

Acceptance Criteria:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

Priority: [Critical/High/Medium/Low]
Dependencies: [Other stories]
```

## Critical Stories

### Story 1: [Title]
**ID**: US-001

As a [user type],
I want to [action],
So that [benefit].

**Acceptance Criteria**:
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

**Priority**: Critical
**Effort**: [Story points/hours]
**Dependencies**: None

**Notes**: [Additional context]

---

### Story 2: [Title]
**ID**: US-002

As a [user type],
I want to [action],
So that [benefit].

**Acceptance Criteria**:
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

**Priority**: High
**Effort**: [Story points/hours]
**Dependencies**: US-001

**Notes**: [Additional context]

---

## High Priority Stories

### Story 3: [Title]
**ID**: US-003
[Details...]

---

## Medium Priority Stories

### Story 4: [Title]
**ID**: US-004
[Details...]

---

## Low Priority / Future Stories

### Story 5: [Title]
**ID**: US-005
[Details...]

---

## Trade-offs & Decisions

### Story [ID]: [Decision]
**Options Considered**:
1. [Option A]: [Pros/Cons]
2. [Option B]: [Pros/Cons]

**Chosen**: [Option X]
**Rationale**: [Why chosen, what sacrificed]

---

**Last Updated**: {date}
**Story Count**: [Total]
**Completed**: [Count]
"""
    }
}

def create_context_doc(doc_type: str, output_dir: str = "docs"):
    """Create a project context documentation file."""

    if doc_type not in TEMPLATES:
        print(f"❌ Unknown document type: {doc_type}")
        print(f"Available types: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)

    template = TEMPLATES[doc_type]
    output_path = Path(output_dir) / template["filename"]

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        print(f"⚠️  File already exists: {output_path}")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)

    # Replace date placeholder
    content = template["content"].format(date=datetime.now().strftime('%Y-%m-%d'))

    output_path.write_text(content)
    print(f"✅ Created {output_path}")
    print(f"\nNext steps:")
    print(f"1. Fill in the template sections in {output_path}")
    print(f"2. Commit to version control")
    print(f"3. Keep updated as project evolves")

def list_context_types():
    """List all available context document types."""
    print("Available context document types:\n")
    for doc_type, template in TEMPLATES.items():
        print(f"  {doc_type:15} - {template['filename']}")
    print("\nUsage: python scripts/init_context.py <type> [output-dir]")
    print("Example: python scripts/init_context.py architecture docs")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/init_context.py <type> [output-dir]")
        print("       python scripts/init_context.py list")
        print("\nExample: python scripts/init_context.py architecture docs")
        sys.exit(1)

    if sys.argv[1] == "list":
        list_context_types()
        sys.exit(0)

    doc_type = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "docs"

    create_context_doc(doc_type, output_dir)
