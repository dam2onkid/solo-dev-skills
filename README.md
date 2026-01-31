# Solo Dev Skills

A collection of Agent Skills for Cursor and Claude Code, extending AI agent capabilities in specialized domains.

## Installation

```bash
# Using npx (no installation needed)
npx solo-dev-skills init

# Or install globally
npm install -g solo-dev-skills
solo-dev-skills init
```

## Commands

```bash
# Initialize all skills
solo-dev-skills init                      # → both .cursor/skills/ and .claude/skills/
solo-dev-skills init -e cursor            # → .cursor/skills/ only
solo-dev-skills init -e claude            # → .claude/skills/ only

# Add specific skills
solo-dev-skills add expo-dev supabase-dev
solo-dev-skills add sui-move -e cursor

# List available skills
solo-dev-skills list
```

## Skills

### 📱 expo-dev

Build universal native apps (Android, iOS, web) with Expo + React Native:

- Expo Router navigation (tabs, stacks, drawers)
- SDK packages (camera, notifications, storage, location)
- EAS Build & deploy to app stores
- TypeScript standards & performance patterns

### 🧪 expo-tester

Test Expo/React Native apps with Jest, RNTL, and Maestro:

- Jest setup with jest-expo preset
- React Native Testing Library queries/events
- Maestro E2E YAML flows
- CI integration

### 🎨 mobile-design

Apple-quality mobile interface design:

- Apple Human Interface Guidelines
- Touch interactions & gesture navigation
- Anti-AI-slop guidelines - avoid generic aesthetics
- Text-to-image/video/audio prompt templates

### ⚡ supabase-dev

Backend-as-a-service with Supabase:

- Authentication (email/password, OAuth, magic links, OTP)
- Database with Row Level Security (RLS)
- File storage & realtime subscriptions
- Edge Functions & CLI

### 🔗 sui-move

Smart contract development on Sui blockchain:

- Move language basics & object model
- Ownership patterns & capabilities
- Testing with sui-move-analyzer
- CLI scripts for build/test/deploy

### 🌐 sui-ts-dev

TypeScript SDK for Sui blockchain:

- Client setup & transaction building
- dApp Kit for React/Next.js integration
- zkLogin, Passkey, SuiNS, Walrus, DeepBook
- Best practices & patterns

### 📋 test-planner

Plan and strategize testing for web and mobile apps:

- Test strategy documents from requirements
- Coverage gap analysis
- Critical path identification
- QA approach documentation

### 🛠️ skill-creator

Guide for creating effective Agent Skills:

- Skill structure: SKILL.md + scripts/ + references/ + assets/
- Progressive disclosure design principle
- Full workflow from planning to packaging

### 🔍 code-review

_Source: [mrgoonie/claudekit-skills](https://github.com/mrgoonie/claudekit-skills)_

Code review practices with 3 core principles:

- **Receiving feedback** - Technical evaluation over performative agreement
- **Requesting reviews** - Systematic review via code-reviewer subagent
- **Verification gates** - Evidence required before completion claims

### 🧠 problem-solving

_Source: [mrgoonie/claudekit-skills](https://github.com/mrgoonie/claudekit-skills)_ (derived from [microsoft/amplifier](https://github.com/microsoft/amplifier))

Problem-solving techniques:

- **collision-zone-thinking** - Force unrelated concepts together for breakthroughs
- **inversion-exercise** - Flip assumptions to reveal alternative approaches
- **meta-pattern-recognition** - Spot patterns appearing in 3+ domains
- **scale-game** - Test at extremes (1000x bigger/smaller)
- **simplification-cascades** - Find insights that eliminate multiple components
- **when-stuck** - Dispatch to appropriate technique based on symptoms

## License

MIT
