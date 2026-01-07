---
name: mobile-design
description: Create distinctive, production-grade mobile app interfaces with Apple-quality design standards. Use when designing mobile screens, implementing touch interactions, creating gesture-based navigation, building responsive mobile layouts, generating app mockups/assets, or establishing mobile design systems. Focuses on iOS/Apple design excellence while avoiding generic AI aesthetics. Includes text-to-image/video/audio prompt templates.
---

# Mobile Design

Create aesthetically beautiful, distinctive mobile app interfaces that feel genuinely designed—not AI-generated. Focus on Apple design excellence as the gold standard.

## When to Use This Skill

- Designing mobile app screens (iOS-first, cross-platform)
- Implementing touch interactions and gesture navigation
- Building responsive layouts for various screen sizes
- Creating mobile-specific components
- Generating mobile app mockups, icons, and visual assets
- Establishing mobile design systems

## Design Thinking (Before Implementation)

Understand context and commit to a **clear aesthetic direction**:

- **Purpose**: What problem does this app solve? Who uses it?
- **Tone**: Pick a direction—refined minimal, warm organic, bold editorial, soft pastel, luxury premium, playful delightful. Commit fully.
- **Differentiation**: What makes this MEMORABLE? What's the signature element?

**CRITICAL**: Apple's design language succeeds through intentionality and restraint. Every element earns its place. Every animation has purpose. Every detail is considered.

## Core Framework

### 1. APPLE EXCELLENCE: Design Language

Study Apple's Human Interface Guidelines deeply. Understand the "why" behind their choices—clarity, deference, depth.

**Reference**: [`references/apple-design-standards.md`](references/apple-design-standards.md)

### 2. EXPERIENCE: UI/UX Principles

Apply fundamental UX laws adapted for mobile—Fitts's Law, Hick's Law, cognitive load.

**Reference**: [`references/ui-ux-principles.md`](references/ui-ux-principles.md)

### 3. TOUCH: Designing for Fingers

Mobile is touch-first. Design for thumbs, consider reachability, ensure comfortable touch targets.

**Reference**: [`references/mobile-interactions.md`](references/mobile-interactions.md)

### 4. FLOW: Navigation & Patterns

Master mobile navigation patterns—tab bars, stacks, sheets, gestures.

**Reference**: [`references/mobile-patterns.md`](references/mobile-patterns.md)

### 5. STORYTELLING: Peak Experiences

Elevate with narrative elements—meaningful animations, progressive disclosure, emotional moments.

**Reference**: [`references/storytelling-design.md`](references/storytelling-design.md)

### 6. GENERATE: Creating Visual Assets

Generate mockups, icons, splash screens using text-to-image/video/audio prompts.

**Reference**: [`references/media-prompts.md`](references/media-prompts.md)

## Anti-AI-Slop Guidelines

**NEVER use generic AI aesthetics**:

- ❌ Default SF Pro everywhere without typographic intention
- ❌ Blue (#007AFF) as the only accent color
- ❌ Identical card components with rounded corners
- ❌ Generic gradient backgrounds (especially purple-blue)
- ❌ Stock illustration style (flat, geometric people)
- ❌ Predictable tab bar with Home/Search/Profile
- ❌ Same spacing, same shadows, same everything

**INSTEAD, make intentional choices**:

- ✅ Typography with character—pair SF Pro with a distinctive display font, or use custom fonts entirely
- ✅ Color palettes that evoke specific emotions—not just "blue for trust"
- ✅ Component variations that fit the context—cards aren't always rectangular
- ✅ Unexpected but delightful micro-interactions
- ✅ Visual metaphors that reinforce the app's purpose
- ✅ Signature elements users will remember

## Workflows

### Workflow 1: Analyze & Extract Inspiration

1. Browse App Store featured apps, Mobbin, Apple Design Awards winners
2. Analyze screenshots for:
   - What makes this feel "Apple-quality"?
   - Typography choices and hierarchy
   - Color restraint and accent usage
   - Animation and transition philosophy
   - Unique signature elements
3. Document insights—not to copy, but to understand the standard

### Workflow 2: Generate Design Assets

1. Define asset type and aesthetic direction
2. Use prompt templates from [`references/media-prompts.md`](references/media-prompts.md)
3. Generate with **ai-multimodal** skill
4. Evaluate against Apple quality bar:
   - Does it feel premium and intentional?
   - Would this look out of place in the App Store featured section?
   - Is there a signature element?
5. Iterate until distinctive and polished

### Workflow 3: Implement Mobile UI

1. Establish design guidelines first
2. Use **expo-dev** for React Native implementation
3. Use **ui-styling** for component styling
4. Focus on:
   - Gesture feel (spring animations, momentum)
   - Transition quality (shared element, contextual)
   - Touch response (immediate, satisfying)
5. Test obsessively—details matter

## Documentation

- Design guidelines: [`assets/mobile-guideline-template.md`](assets/mobile-guideline-template.md)
- Design story/narrative: [`assets/design-story-template.md`](assets/design-story-template.md)

## Guiding Principles

1. **Intentional**: Every element earns its place
2. **Distinctive**: Memorable, not generic
3. **Apple-Quality**: The gold standard for mobile
4. **Touch-Native**: Designed for fingers, not adapted from web
5. **Emotionally Resonant**: Creates feeling, not just function
6. **Accessible**: Beautiful AND usable by everyone

## Related Skills

- **expo-dev**: Build cross-platform apps
- **ui-styling**: Implement with Tailwind/NativeWind
- **ai-multimodal**: Generate and analyze design assets
- **aesthetic**: Core design principles
