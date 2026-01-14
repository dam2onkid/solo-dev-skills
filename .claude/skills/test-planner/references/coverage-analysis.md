# Coverage Analysis Guide

## Coverage Types

### Code Coverage
- **Line coverage**: % of code lines executed
- **Branch coverage**: % of if/else paths tested
- **Function coverage**: % of functions called

### Feature Coverage
- **Requirement coverage**: Features with tests
- **User flow coverage**: E2E scenarios covered
- **Edge case coverage**: Error paths tested

## Gap Identification Process

### Step 1: Map Features to Tests

```markdown
| Feature | Unit | Integration | E2E | Status |
|---------|------|-------------|-----|--------|
| Login | ✅ | ✅ | ✅ | Complete |
| Register | ✅ | ❌ | ❌ | Gaps |
| Profile | ❌ | ❌ | ❌ | Missing |
```

### Step 2: Identify Critical Paths

List user journeys by importance:
1. **Must test**: Revenue-generating, security-critical
2. **Should test**: Core features, frequent usage
3. **Could test**: Edge cases, rare scenarios

### Step 3: Analyze Risk vs Coverage

```
High Risk + Low Coverage = Priority Gap
High Risk + High Coverage = Maintain
Low Risk + Low Coverage = Acceptable
Low Risk + High Coverage = Potential over-testing
```

## Coverage Metrics

### Recommended Thresholds

| Test Type | Target | Minimum |
|-----------|--------|---------|
| Unit (critical modules) | 90% | 80% |
| Unit (overall) | 80% | 70% |
| Integration | N/A | Key flows |
| E2E | N/A | Critical paths |

### Generating Reports

```bash
# Jest coverage
npm test -- --coverage --coverageReporters=text-summary

# Output
Statements   : 85.5%
Branches     : 78.2%
Functions    : 90.1%
Lines        : 85.5%
```

## Coverage Report Template

```markdown
## Coverage Report: [Date]

### Summary
- **Code Coverage**: 82% (target: 80%)
- **Critical Flows**: 5/5 covered
- **Known Gaps**: 3 features

### By Module
| Module | Coverage | Status |
|--------|----------|--------|
| auth/ | 95% | ✅ |
| payments/ | 88% | ✅ |
| profile/ | 45% | ⚠️ |

### Gap Details
1. **Profile editing** - No integration tests
   - Risk: Medium
   - Action: Add API tests for update endpoint

2. **Offline mode** - No E2E coverage
   - Risk: High
   - Action: Add Maestro flow with network off

### Recommendations
- [ ] Add integration tests for profile module
- [ ] Create E2E flow for offline scenarios
- [ ] Increase branch coverage in utils/
```

## Continuous Coverage Tracking

### CI Integration
```yaml
# GitHub Actions example
- name: Check coverage threshold
  run: |
    npm test -- --coverage --coverageThreshold='{
      "global": {
        "branches": 75,
        "functions": 80,
        "lines": 80
      }
    }'
```

### PR Coverage Comments
- Show coverage diff (+/- from main)
- Flag decreased coverage
- Highlight uncovered new code
