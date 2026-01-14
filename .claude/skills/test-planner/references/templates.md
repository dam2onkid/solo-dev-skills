# Test Plan Templates

## Web Application

```markdown
# Test Plan: [App Name] Web

## Scope
- **Features**: [List features in scope]
- **Browsers**: Chrome 100+, Safari 16+, Firefox 100+, Edge 100+
- **Viewports**: Mobile (375px), Tablet (768px), Desktop (1280px)

## Test Strategy

### Unit Tests (Jest/Vitest)
| Area | Coverage Target | Priority |
|------|-----------------|----------|
| Components | 80% | P1 |
| Hooks | 90% | P0 |
| Utils | 95% | P0 |
| API clients | 85% | P1 |

### E2E Tests (Playwright/Cypress)
| Flow | Browsers | Priority |
|------|----------|----------|
| Authentication | All | P0 |
| Core feature | Chrome, Safari | P0 |
| Settings | Chrome | P2 |

## Test Scenarios

### Authentication
- [ ] Login with valid credentials
- [ ] Login with invalid credentials → error message
- [ ] Logout clears session
- [ ] Password reset flow
- [ ] OAuth login (Google, GitHub)

### [Feature Name]
- [ ] Happy path scenario
- [ ] Edge case: empty state
- [ ] Edge case: max items
- [ ] Error handling: network failure

## Accessibility Checklist
- [ ] Keyboard navigation
- [ ] Screen reader labels
- [ ] Color contrast (WCAG AA)
- [ ] Focus indicators

## Performance Checklist
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
```

---

## Mobile Application

```markdown
# Test Plan: [App Name] Mobile

## Scope
- **Platforms**: iOS 15+, Android 10+
- **Devices**: iPhone 12+, Pixel 5+, Samsung Galaxy S21+
- **Build**: Development / TestFlight / Internal Testing

## Test Strategy

### Unit Tests (Jest + RNTL)
| Area | Coverage Target | Priority |
|------|-----------------|----------|
| Components | 80% | P1 |
| Hooks | 90% | P0 |
| Navigation | 75% | P1 |
| State management | 85% | P0 |

### E2E Tests (Maestro)
| Flow | Platforms | Priority |
|------|-----------|----------|
| Onboarding | iOS, Android | P0 |
| Core feature | iOS, Android | P0 |
| Settings | iOS | P2 |

## Test Scenarios

### Onboarding
- [ ] First launch → welcome screen
- [ ] Permission requests (camera, location)
- [ ] Skip onboarding
- [ ] Complete onboarding → home

### Offline Behavior
- [ ] App launches offline
- [ ] Cached data displays
- [ ] Actions queue for sync
- [ ] Reconnection syncs data

### Push Notifications
- [ ] Permission request
- [ ] Receive while foreground
- [ ] Receive while background
- [ ] Deep link from notification

## Device-Specific Checklist
- [ ] Notch/Dynamic Island handling
- [ ] Safe area insets
- [ ] Keyboard avoidance
- [ ] Orientation changes
- [ ] Dark mode support
```

---

## API/Backend

```markdown
# Test Plan: [Service Name] API

## Scope
- **Endpoints**: /api/v1/*
- **Environment**: Staging
- **Auth**: JWT Bearer tokens

## Test Strategy

### Unit Tests
| Area | Coverage | Priority |
|------|----------|----------|
| Controllers | 85% | P0 |
| Services | 90% | P0 |
| Validators | 95% | P0 |
| Middleware | 80% | P1 |

### Integration Tests
| Area | Priority |
|------|----------|
| Database operations | P0 |
| External API calls | P1 |
| Queue processing | P2 |

## Endpoint Test Matrix

| Endpoint | Method | Auth | Happy | Error | Edge |
|----------|--------|------|-------|-------|------|
| /users | GET | Yes | ✅ | ✅ | ⬜ |
| /users | POST | Yes | ✅ | ⬜ | ⬜ |
| /users/:id | PUT | Yes | ⬜ | ⬜ | ⬜ |

## Security Checklist
- [ ] Auth required endpoints reject without token
- [ ] Rate limiting enforced
- [ ] Input validation (SQL injection, XSS)
- [ ] Sensitive data not logged
- [ ] CORS configured correctly
```

---

## Feature-Specific

```markdown
# Test Plan: [Feature Name]

## Overview
- **Description**: [What the feature does]
- **PRD/Spec**: [Link to requirements]
- **Related code**: [Paths/modules affected]

## Acceptance Criteria → Test Cases

| AC | Test Case | Type | Status |
|----|-----------|------|--------|
| User can X | Verify X works | E2E | ⬜ |
| System validates Y | Invalid Y shows error | Unit | ⬜ |
| Data persists after Z | Reload shows data | Integration | ⬜ |

## Edge Cases
- [ ] Empty state
- [ ] Maximum limits
- [ ] Concurrent actions
- [ ] Interrupted flow (close app mid-action)

## Regression Risks
- [ ] [Existing feature] may be affected
- [ ] [Integration point] needs verification

## Sign-off
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Manual QA complete
- [ ] PM approval
```
