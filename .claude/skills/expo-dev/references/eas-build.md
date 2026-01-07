# EAS Build & Submit Reference

Expo Application Services (EAS) for building and deploying apps.

## Setup

```bash
npm install -g eas-cli
eas login
eas build:configure    # Creates eas.json
```

## eas.json Configuration

```json
{
  "cli": { "version": ">= 5.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true },
      "android": { "buildType": "apk" }
    },
    "preview": {
      "distribution": "internal",
      "android": { "buildType": "apk" }
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "you@example.com", "ascAppId": "1234567890" },
      "android": { "serviceAccountKeyPath": "./play-store-key.json" }
    }
  }
}
```

## Build Commands

```bash
# Development build (with dev client)
eas build --profile development --platform ios
eas build --profile development --platform android

# Preview build (internal testing)
eas build --profile preview --platform all

# Production build (store release)
eas build --profile production --platform ios
eas build --profile production --platform android

# Local build (no EAS servers)
eas build --local --platform android
```

## Build Options

| Option              | Description                           |
| ------------------- | ------------------------------------- |
| `--profile`         | Build profile from eas.json           |
| `--platform`        | `ios`, `android`, or `all`            |
| `--local`           | Build locally (requires native tools) |
| `--auto-submit`     | Submit after build completes          |
| `--non-interactive` | Skip prompts (CI/CD)                  |

## Submit to Stores

```bash
# Submit latest build
eas submit --platform ios
eas submit --platform android

# Submit specific build
eas submit --platform ios --id BUILD_ID
```

### iOS Setup

1. Create App Store Connect API key
2. Configure in eas.json or environment:

```json
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCD1234"
      }
    }
  }
}
```

### Android Setup

1. Create Google Play service account
2. Download JSON key file
3. Configure in eas.json:

```json
{
  "submit": {
    "production": {
      "android": {
        "serviceAccountKeyPath": "./google-play-key.json",
        "track": "internal"
      }
    }
  }
}
```

**Tracks**: `internal`, `alpha`, `beta`, `production`

## Environment Variables

```bash
# Set secrets (encrypted)
eas secret:create --name API_KEY --value "your-secret"
eas secret:list
eas secret:delete API_KEY

# Use in app.config.js
export default {
  extra: {
    apiKey: process.env.API_KEY,
  },
};
```

Access in code:

```typescript
import Constants from "expo-constants";
const apiKey = Constants.expoConfig?.extra?.apiKey;
```

## EAS Update (OTA Updates)

```bash
# Configure
eas update:configure

# Publish update
eas update --branch production --message "Bug fixes"

# List updates
eas update:list
```

**app.json config**:

```json
{
  "expo": {
    "updates": {
      "url": "https://u.expo.dev/PROJECT_ID"
    },
    "runtimeVersion": { "policy": "appVersion" }
  }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: EAS Build
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --platform all --non-interactive
```

### Environment Setup

```bash
# Generate token for CI
eas credentials
# or
npx expo login

# Set EXPO_TOKEN in CI secrets
```

## Common Build Profiles

### Development (Debug)

- Dev client enabled
- Internal distribution
- Simulator/emulator builds

### Preview (Testing)

- Release mode
- Internal distribution (TestFlight/Firebase)
- APK for Android

### Production (Release)

- Store-ready builds
- Auto version increment
- Optimized & signed
