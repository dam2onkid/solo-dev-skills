# Apple Design Standards

The gold standard for mobile design. Study these principles deeply.

## Apple's Design Philosophy

### Three Core Themes

**Clarity**
- Text is legible at every size
- Icons are precise and lucid
- Adornments are subtle and appropriate
- Functionality motivates design

**Deference**
- The UI helps people understand and interact with content
- Content fills the screen
- Translucency and blur hint at more
- Minimal use of bezels, gradients, and drop shadows

**Depth**
- Distinct visual layers convey hierarchy
- Transitions provide sense of depth
- Touch and discoverability heighten delight

## Typography Excellence

### SF Pro: More Than a System Font

SF Pro isn't "generic"—it's precision-engineered. The key is using it with intention:

- **Optical sizes**: Text, Display variants for different contexts
- **Variable weight**: 100 to 900, enabling subtle hierarchy
- **Tracking adjustments**: Tighter at large sizes, looser at small

### Beyond SF Pro

Apple apps often pair SF Pro with:
- **SF Pro Rounded**: Softer, friendlier feel
- **New York**: Serif for editorial, reading experiences
- **Custom typefaces**: Apps like Notes, Books have distinct typography

### Typography Hierarchy

| Element | Weight | Tracking | Purpose |
|---------|--------|----------|---------|
| Large Title | Bold | Tight (-0.5pt) | Screen headers |
| Title | Semibold | Normal | Section headers |
| Body | Regular | Normal | Content |
| Caption | Regular | Loose (+0.5pt) | Supporting text |

**The Apple difference**: Confident size jumps between hierarchy levels. Don't be timid.

## Color Philosophy

### Restraint Over Abundance

Apple's color usage:
- **Mostly monochrome**: Black/white/gray foundation
- **Single accent**: One color carries meaning
- **Semantic colors**: System colors adapt to context
- **Dark mode native**: Colors designed for both modes

### Beyond Blue

While `systemBlue` is default, Apple apps use distinctive palettes:
- **Health**: Pink/red family
- **Fitness**: Green rings, multicolor activity
- **Music**: Dynamic, album-derived colors
- **Weather**: Atmospheric, time-based gradients
- **Notes**: Warm yellow/cream

### Color Principles

1. **Color as communication**: Not decoration
2. **Sufficient contrast**: 4.5:1 minimum, but Apple often exceeds
3. **Semantic meaning**: Red for destructive, green for positive
4. **Vibrancy in dark mode**: Colors pop against dark backgrounds

## Visual Design

### Depth & Layering

Apple creates depth through:
- **Material backgrounds**: Blur effects for context
- **Elevation**: Shadow intensity indicates hierarchy
- **Overlapping elements**: Cards, sheets, modals stack naturally

### Negative Space

Apple designs breathe:
- **Generous margins**: Content doesn't crowd edges
- **Section spacing**: Clear visual separation
- **Focus through emptiness**: Important elements stand alone

### Iconography

SF Symbols characteristics:
- **Consistent stroke weight**: Matches SF Pro text
- **Nine weights × three scales**: Precise control
- **Semantic variants**: Same concept, different meanings

## Motion & Animation

### Animation Philosophy

Apple animations feel physical:
- **Spring-based**: Natural deceleration, slight overshoot
- **Interruptible**: Can be redirected mid-animation
- **Responsive**: Begin immediately on touch
- **Meaningful**: Animation explains change

### Key Animation Patterns

**Sheet presentation**:
- Slides up with spring
- Parent scales down subtly
- Darkens background gradually

**Navigation push**:
- New screen slides in from right
- Title transitions smoothly
- Back content scales/fades

**Item deletion**:
- Swipe reveals action
- Haptic at threshold
- Item collapses smoothly

### Timing Philosophy

- **Micro-interactions**: 100-200ms (immediate feel)
- **Screen transitions**: 350ms (smooth, not sluggish)
- **Spring animations**: `response: 0.5, dampingFraction: 0.7` (typical)

## Component Patterns

### Cards Done Right

Apple cards are not all the same:
- **Music**: Album art bleeds to edge
- **App Store**: Hero images, editorial layout
- **Wallet**: Realistic card representation
- **Photos**: Borderless, grid-tight

### Lists With Character

- **Grouped inset**: Settings, preferences
- **Plain**: Content-focused, minimal chrome
- **Sidebar**: Navigation in iPad split view

### Buttons With Intention

- **Filled**: Primary actions (single per context)
- **Gray fill**: Secondary prominence
- **Tinted**: Text with color background
- **Plain**: Tertiary, embedded actions

## Signature Elements

What makes Apple apps recognizable:

1. **Large titles that collapse**: Scroll interaction delight
2. **Contextual menus**: Long-press reveals options
3. **Swipe actions**: Quick, gestural interactions
4. **Pull behaviors**: Refresh, reveal search, dismiss
5. **Haptic punctuation**: Feedback at key moments

## The Quality Bar

Ask yourself:
- Would this feel at home next to Apple's apps?
- Is every element intentional?
- Does the animation feel physical and natural?
- Is there visual rest, or is everything competing?
- What will users remember about this design?

## Inspiration Sources

### Apple Resources
- Human Interface Guidelines (developer.apple.com/design)
- Apple Design Awards winners
- Apple's own apps (best-in-class references)
- WWDC design sessions

### Analysis Approach
Don't copy—understand WHY Apple made each choice. The principles transfer; the specific implementations should be yours.
