# Jest Setup for Expo

## Full Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'jest-expo',
  setupFilesAfterEnv: [
    '@testing-library/react-native/extend-expect',
    '<rootDir>/jest.setup.ts'
  ],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|native-base|react-native-svg)'
  ],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1'
  },
  collectCoverageFrom: [
    '**/*.{ts,tsx}',
    '!**/node_modules/**',
    '!**/coverage/**',
    '!**/*.d.ts'
  ],
  testMatch: ['**/__tests__/**/*.test.{ts,tsx}']
};
```

## Setup File

```typescript
// jest.setup.ts
import '@testing-library/react-native/extend-expect';

// Silence warnings
jest.spyOn(console, 'warn').mockImplementation(() => {});

// Mock expo modules
jest.mock('expo-font');
jest.mock('expo-asset');

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);

// Mock expo-router
jest.mock('expo-router', () => ({
  useRouter: () => ({ push: jest.fn(), replace: jest.fn(), back: jest.fn() }),
  useLocalSearchParams: () => ({}),
  useSegments: () => [],
  Link: 'Link'
}));
```

## Mocking Native Modules

```typescript
// __mocks__/expo-camera.ts
export const Camera = {
  requestCameraPermissionsAsync: jest.fn(() => 
    Promise.resolve({ status: 'granted' })
  )
};

// __mocks__/expo-location.ts  
export const requestForegroundPermissionsAsync = jest.fn(() =>
  Promise.resolve({ status: 'granted' })
);
export const getCurrentPositionAsync = jest.fn(() =>
  Promise.resolve({ coords: { latitude: 0, longitude: 0 } })
);
```

## Test Scripts

```json
{
  "scripts": {
    "test": "jest --watch --coverage=false --changedSince=origin/main",
    "test:debug": "jest -o --watch --coverage=false",
    "test:ci": "jest --ci --coverage --reporters=default --reporters=jest-junit",
    "test:update": "jest -u --coverage=false"
  }
}
```

## CI Configuration (GitHub Actions)

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run test:ci
      - uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
```

## Coverage Thresholds

```javascript
// jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```
