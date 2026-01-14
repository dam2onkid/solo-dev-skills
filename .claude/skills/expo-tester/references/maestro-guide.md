# Maestro E2E Testing Guide

## Installation

```bash
# macOS/Linux
curl -fsSL "https://get.maestro.mobile.dev" | bash

# Verify installation
maestro --version
```

## Flow Structure

```yaml
# maestro/flows/example.yaml
appId: com.myapp.dev          # Bundle ID (iOS) or package name (Android)
tags:
  - smoke
  - auth
env:
  BASE_URL: https://api.example.com
---
- launchApp
- tapOn: "Get Started"
```

## Core Commands

### Navigation & Tapping

```yaml
- launchApp                       # Launch app
- launchApp:
    clearState: true              # Clear app data before launch

- tapOn: "Login"                  # Tap by text
- tapOn:
    id: "submit-button"           # Tap by testID
- tapOn:
    id: ".*button.*"              # Regex pattern
- tapOn:
    text: "Continue"
    index: 1                      # Second match (0-indexed)

- doubleTapOn: "Like"
- longPressOn: "Delete"
```

### Text Input

```yaml
- tapOn: "Email"
- inputText: "test@example.com"

- tapOn:
    id: "password-input"
- inputText: "secret123"

- eraseText                       # Clear focused input
- eraseText: 10                   # Erase 10 characters
```

### Assertions

```yaml
- assertVisible: "Welcome back"
- assertVisible:
    id: "home-screen"
    
- assertNotVisible: "Error"

- assertTrue: ${isLoggedIn}       # Variable assertion
```

### Scrolling

```yaml
- scroll                          # Scroll down
- scroll:
    direction: UP                 # UP, DOWN, LEFT, RIGHT

- scrollUntilVisible:
    element: "Load More"
    direction: DOWN
    timeout: 10000
```

### Waiting

```yaml
- extendedWaitUntil:
    visible: "Dashboard"
    timeout: 30000                # 30 seconds

- waitForAnimationToEnd
```

## Selectors

```yaml
# By text (exact)
- tapOn: "Submit"

# By testID
- tapOn:
    id: "submit-btn"

# By regex
- tapOn:
    text: "Item \\d+"             # Matches "Item 1", "Item 2", etc

# Combined
- tapOn:
    text: "Delete"
    enabled: true
    index: 0
```

## Variables & Environment

```yaml
# Define in flow
env:
  USERNAME: test@example.com
  PASSWORD: password123
---
- inputText: ${USERNAME}

# Pass via CLI
# maestro test -e USERNAME=prod@example.com flow.yaml

# Output variables
- copyTextFrom:
    id: "otp-code"
- inputText: ${maestro.copiedText}
```

## Conditional Logic

```yaml
- runFlow:
    when:
      visible: "Accept Cookies"
    file: dismiss-cookies.yaml

- tapOn:
    text: "Skip"
    optional: true               # Won't fail if not found
```

## Subflows

```yaml
# maestro/flows/shared/login.yaml
- tapOn: "Email"
- inputText: ${EMAIL}
- tapOn: "Password"
- inputText: ${PASSWORD}
- tapOn: "Sign In"

# maestro/flows/checkout.yaml
appId: com.myapp
env:
  EMAIL: test@example.com
  PASSWORD: secret123
---
- launchApp
- runFlow: shared/login.yaml
- tapOn: "Checkout"
```

## Running Tests

```bash
# Single flow
maestro test maestro/flows/login.yaml

# All flows in directory
maestro test maestro/flows/

# With tags
maestro test --include-tags=smoke maestro/flows/
maestro test --exclude-tags=slow maestro/flows/

# Environment variables
maestro test -e EMAIL=test@example.com -e PASSWORD=secret flow.yaml

# Continuous mode (watch)
maestro test -c flow.yaml

# Generate reports
maestro test --format junit --output results.xml flows/
maestro test --format html --output report.html flows/
```

## Expo-specific Setup

```yaml
# For Expo development builds
appId: com.myapp.dev

# For Expo Go (not recommended)
appId: host.exp.Exponent
---
- launchApp:
    arguments:
      EXDevMenuDisableAutoLaunch: true
```

## CI Configuration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push]
jobs:
  e2e:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: |
          curl -fsSL "https://get.maestro.mobile.dev" | bash
          export PATH="$PATH:$HOME/.maestro/bin"
      - run: npx expo prebuild --platform ios
      - run: npx expo run:ios --configuration Release
      - run: maestro test maestro/flows/
```

## Debugging

```bash
# Record flow interactively
maestro studio

# View hierarchy
maestro hierarchy

# Take screenshot
maestro screenshot output.png
```
