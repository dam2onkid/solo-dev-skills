# Solo Dev Skills

A collection of Agent Skills for Claude Code, extending AI agent capabilities in specialized domains.

## Skills

### 📱 expo-dev

Build universal native apps (Android, iOS, web) with Expo + React Native:

- Expo Router navigation (tabs, stacks, drawers)
- SDK packages (camera, notifications, storage, location)
- EAS Build & deploy to app stores
- TypeScript standards & performance patterns

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

## Installation

Copy the `.claude/skills/` folder into your project.

## License

MIT
