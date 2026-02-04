# Project Context Files

Essential documentation for LLM to understand project scope and avoid over-engineering.

## Required Context Files

### 1. Architecture Overview (`docs/ARCHITECTURE.md`)

**Purpose**: High-level system understanding
**Content**:

- Application purpose and user problems solved
- Technology stack and rationale
- Core components and data flow
- Design patterns and principles
- Constraints and limitations

**When to read**: Before proposing any feature or architectural change

### 2. Product Requirements Document (`docs/PRD.md`)

**Purpose**: Define product scope and priorities
**Content**:

- Product vision and goals
- Target users and personas
- Core features (in scope)
- Explicitly out-of-scope features
- Success metrics

**Why needed**: Prevents suggesting features that don't align with product vision

### 3. User Stories Collection (`docs/USER_STORIES.md`)

**Purpose**: Define specific user needs
**Content**:

- As [user type], I want [action] so that [benefit]
- Acceptance criteria per story
- Priority ranking
- Dependencies between stories

**Why needed**: Ensures features serve real user needs

### 4. Technical Constraints (`docs/CONSTRAINTS.md`)

**Purpose**: Define boundaries and limitations
**Content**:

- Platform/device requirements
- Performance benchmarks
- Security requirements
- Compliance needs (GDPR, accessibility, etc.)
- Budget/timeline constraints
- Technology restrictions

**Why needed**: Prevents suggesting infeasible or non-compliant solutions

### 5. API Documentation (`docs/API.md`)

**Purpose**: Define system interfaces
**Content**:

- External API endpoints
- Internal module interfaces
- Request/response formats
- Authentication/authorization
- Rate limits and quotas

**Why needed**: Prevents inventing non-existent APIs or misusing existing ones

## Avoiding AI Slop

**AI Slop Signs**:

- Generic boilerplate suggestions ("Let's add a dashboard!")
- Over-engineered solutions (microservices for simple CRUD)
- Hallucinated features not in requirements
- Ignoring existing architecture patterns
- Copy-paste code without understanding context

**Prevention Strategy**:

1. **Always read context first**: Before suggesting anything, read relevant docs
2. **Ask clarifying questions**: If context unclear, ask rather than assume
3. **Reference existing patterns**: Use established architecture/code patterns
4. **Justify with trade-offs**: Explain pros/cons of suggestions
5. **Stay in scope**: Only suggest features aligned with PRD

## Template: Context Check

Before proposing feature/change, answer:

```
[ ] Read docs/ARCHITECTURE.md - understand system structure?
[ ] Read docs/PRD.md - feature aligns with product vision?
[ ] Read docs/USER_STORIES.md - addresses real user need?
[ ] Read docs/CONSTRAINTS.md - respects technical limits?
[ ] Read existing similar features - follows established patterns?
[ ] Identified trade-offs - what are pros/cons?
[ ] Minimalist approach - simplest solution that works?
```

## Creating Context Files

If project lacks these files, create them:

```bash
# Create architecture overview
python .cursor/skills/task-master/scripts/init_context.py architecture

# Create PRD
python .cursor/skills/task-master/scripts/init_context.py prd

# Create constraints doc
python .cursor/skills/task-master/scripts/init_context.py constraints
```

## Example: Good vs Bad Suggestions

**Bad (AI Slop)**:

> "Let's add a user dashboard with real-time analytics, social features, and gamification!"

- No PRD reference
- Over-engineered
- Unrelated to core use case

**Good**:

> "Per USER_STORIES.md #23, users need to view scan history. Propose: Simple list view in existing ScanListScreen (follows MVVM pattern per ARCHITECTURE.md), Room query for metadata. Trade-off: Basic UI now, can add filters later if usage data shows need."

- References requirements
- Uses existing architecture
- Simple solution
- Clear trade-offs

## Integration with Task-Master

**Feature initialization** should:

1. Check context files exist
2. Reference relevant sections in requirements doc
3. Validate against constraints
4. Document trade-offs in design doc

**Feature requirements** must include:

- Which user story addressed
- How it fits architecture
- What constraints respected
- What explicitly NOT included (non-goals)
