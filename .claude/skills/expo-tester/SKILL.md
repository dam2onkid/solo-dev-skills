---
name: expo-tester
description: Test Expo/React Native apps with Jest, React Native Testing Library (RNTL), and Maestro. Use when setting up test configuration, writing unit/component tests, creating E2E flows, mocking native modules, testing navigation/async operations, or debugging flaky tests. Covers jest-expo preset, RNTL queries/events, Maestro YAML flows, and CI integration.
---

# Expo Tester

Comprehensive testing for Expo apps: unit, component, and E2E tests.

## Quick Setup

```bash
# Install testing dependencies
npx expo install jest-expo jest @testing-library/react-native @types/jest

# For user events (recommended)
npm install --save-dev @testing-library/user-event
```

### package.json Configuration

```json
{
  "scripts": {
    "test": "jest --watchAll",
    "test:ci": "jest --ci --coverage"
  },
  "jest": {
    "preset": "jest-expo",
    "transformIgnorePatterns": [
      "node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|react-navigation|@react-navigation/.*)"
    ],
    "setupFilesAfterEnv": ["@testing-library/react-native/extend-expect"]
  }
}
```

## Test Structure

```
__tests__/
├── components/        # Component tests
├── screens/           # Screen tests
├── hooks/             # Custom hook tests
├── utils/             # Utility function tests
└── setup.ts           # Test setup file
maestro/
├── flows/             # E2E test flows
│   ├── auth.yaml
│   └── onboarding.yaml
└── config.yaml        # Maestro configuration
```

## Component Testing (RNTL)

```typescript
import { render, screen, userEvent } from '@testing-library/react-native';
import { MyButton } from '@/components/MyButton';

describe('<MyButton />', () => {
  it('calls onPress when tapped', async () => {
    const onPress = jest.fn();
    const user = userEvent.setup();
    
    render(<MyButton onPress={onPress} label="Submit" />);
    
    await user.press(screen.getByRole('button', { name: 'Submit' }));
    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

## E2E Testing (Maestro)

```bash
# Install Maestro
curl -fsSL "https://get.maestro.mobile.dev" | bash

# Run E2E test
maestro test maestro/flows/login.yaml

# Continuous mode (auto-rerun)
maestro test -c maestro/flows/login.yaml
```

### Basic Flow

```yaml
# maestro/flows/login.yaml
appId: com.myapp
---
- launchApp
- tapOn: "Email"
- inputText: "test@example.com"
- tapOn: "Password"
- inputText: "password123"
- tapOn: "Sign In"
- assertVisible: "Welcome"
```

## Resources

| Reference                      | Description                               |
| ------------------------------ | ----------------------------------------- |
| `references/jest-setup.md`     | Jest config, mocks, coverage, CI setup    |
| `references/rntl-guide.md`     | RNTL queries, events, async patterns      |
| `references/maestro-guide.md`  | Maestro commands, selectors, CI           |
