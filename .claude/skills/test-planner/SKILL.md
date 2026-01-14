---
name: test-planner
description: Plan and strategize testing for web and mobile applications. Use when creating test strategy documents, analyzing test coverage gaps, generating test plans from requirements/user stories, identifying critical paths and edge cases, prioritizing test scenarios, or documenting QA approach. Outputs structured markdown test plans.
---

# Test Planner

Create comprehensive test plans and coverage analysis for web/mobile apps.

## Workflow

### 1. Gather Context

Before planning, analyze:
- **Requirements/User stories** - What features need testing?
- **Codebase structure** - Components, screens, API endpoints
- **Existing tests** - What's already covered?
- **Risk areas** - Complex logic, integrations, user-critical flows

### 2. Generate Test Plan

```bash
# Output location
docs/
└── test-plan.md    # Or project-specific location
```

### 3. Coverage Analysis

Identify gaps by mapping:
- Features → Test cases
- User flows → E2E scenarios  
- Edge cases → Unit tests

## Test Plan Template

```markdown
# Test Plan: [Feature/Project Name]

## Overview
- **Scope**: [What's being tested]
- **Timeline**: [Testing period]
- **Environment**: [Dev/Staging/Prod]

## Test Strategy
### Unit Tests
- [ ] Component logic
- [ ] Utility functions
- [ ] Hooks/state management

### Integration Tests  
- [ ] API endpoints
- [ ] Database operations
- [ ] Third-party services

### E2E Tests
- [ ] Critical user flows
- [ ] Cross-platform scenarios

## Test Scenarios
| ID | Scenario | Type | Priority | Status |
|----|----------|------|----------|--------|
| T1 | User login with valid credentials | E2E | P0 | Pending |

## Coverage Analysis
### Covered
- [x] Authentication flow
### Gaps
- [ ] Error handling for network failures

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|
| Payment integration | High | Mock in staging, manual prod test |
```

## Resources

| Reference                        | Description                              |
| -------------------------------- | ---------------------------------------- |
| `references/strategy-guide.md`   | Test types, prioritization, risk matrix  |
| `references/coverage-analysis.md`| Gap identification, metrics, reporting   |
| `references/templates.md`        | Test plan templates by app type          |
