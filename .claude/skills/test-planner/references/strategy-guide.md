# Test Strategy Guide

## Test Pyramid

```
        /\
       /E2E\        Few, slow, expensive
      /------\
     /Integration\   Medium coverage
    /--------------\
   /   Unit Tests   \  Many, fast, cheap
  /------------------\
```

## Test Types by Layer

### Unit Tests
- **What**: Individual functions, components, hooks
- **When**: Logic-heavy code, utilities, pure functions
- **Tools**: Jest, Vitest, Testing Library

### Integration Tests
- **What**: Multiple units working together
- **When**: API calls, database ops, service interactions
- **Tools**: Supertest, MSW, Playwright API testing

### E2E Tests
- **What**: Complete user flows
- **When**: Critical paths, cross-feature scenarios
- **Tools**: Maestro (mobile), Playwright/Cypress (web)

## Priority Matrix

| Priority | Definition | Examples |
|----------|------------|----------|
| P0 | Critical - blocks release | Login, payment, core feature |
| P1 | High - major functionality | User profile, settings, search |
| P2 | Medium - important features | Notifications, filters, sorting |
| P3 | Low - nice to have | Animations, tooltips, themes |

## Risk-Based Testing

### High Risk Areas
- Authentication & authorization
- Payment processing
- Data mutations (create/update/delete)
- Third-party integrations
- Cross-platform behavior

### Risk Assessment Matrix

| Probability | Impact | Risk Level | Action |
|-------------|--------|------------|--------|
| High | High | Critical | Automate + manual |
| High | Low | Medium | Automate |
| Low | High | High | Manual + monitoring |
| Low | Low | Low | Smoke test |

## Platform-Specific Considerations

### Web
- Browser compatibility (Chrome, Safari, Firefox, Edge)
- Responsive breakpoints (mobile, tablet, desktop)
- Accessibility (keyboard nav, screen readers)
- Performance (Core Web Vitals)

### Mobile
- OS versions (iOS 15+, Android 10+)
- Device sizes (phone, tablet)
- Permissions (camera, location, notifications)
- Offline behavior
- Deep linking

## Test Environment Strategy

| Environment | Purpose | Data |
|-------------|---------|------|
| Local | Development | Mocked/seeded |
| CI | Automated tests | Fixtures |
| Staging | Pre-release | Sanitized prod copy |
| Production | Smoke tests only | Real data (read-only) |
