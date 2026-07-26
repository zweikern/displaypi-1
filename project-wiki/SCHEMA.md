---
okf_version: "0.2"
type: Schema
title: Project Wiki Schema – displaypi-1
description: Agent instructions for maintaining the displaypi-1 project wiki. Combines Karpathy's LLM Wiki pattern with the Open Knowledge Format (OKF) v0.2.
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
---

# Project Wiki Schema – displaypi-1

## Quick Start for AI Agents

When the user says **`project-wiki update`**, the agent MUST:

1. **Read this SCHEMA.md** for conventions and workflows.
2. **Read `index.md`** for the current catalog.
3. **Perform the update operation** as defined below (§ Operations → Update).
4. **Write all changes** to concept pages, index.md, and log.md.

The shell script `./pw update` provides a human-readable trigger that describes the steps, then hands over to the agent. The agent does the actual work.

## Purpose

This file is the **schema** for the `project-wiki/` directory. It tells every AI agent (Codex, Copilot, Claude, etc.) how to read, maintain, and extend the project knowledge base. The wiki is the project's persistent memory — it accrues knowledge with every session.

## Three-Layer Architecture

```
sources/          ← Immutable raw sources. Agents read but NEVER modify.
concepts/         ← LLM-maintained markdown. Agents create and update. OKF v0.2.
SCHEMA.md         ← This file. Tells agents HOW to maintain the wiki.
index.md          ← Content catalog. Updated on every change.
log.md            ← Chronological history. Append-only.
```

- **sources/**: Reference documents (like the original briefing), datasheets, pinout diagrams. Immutable.
- **concepts/**: Derived knowledge as OKF concept documents. Each file has YAML frontmatter with at least `type`.
- **schema** (SCHEMA.md + index.md + log.md): Governance files.

## OKF v0.2 Conventions

Every concept document under `concepts/` MUST follow OKF v0.2:

### Required Frontmatter
```yaml
---
type: <Type name>  # REQUIRED. e.g. "Hardware", "Architecture", "Phase", "Protocol"
---
```

### Recommended Frontmatter
```yaml
title: <Display name>
description: <One-line summary>
tags: [<tag>, ...]
status: draft | stable | deprecated   # absent ⇒ stable
stale_after: YYYY-MM-DD
generated: { by: <actor>, at: <ISO 8601> }
verified: { by: <actor>, at: <ISO 8601> }
sources:
  - id: <key>
    resource: <path or URL>
    title: <label>
```

### Actor Convention
- Agent: `codex/gpt-5`, `copilot/deepseek-v4`
- Human: `human:tom`
- Process: `process:bootstrap`, `process:ci`

### Trust Tiers
Derived from `verified`:
- No `verified` → **unverified**
- Only non-`human:` actors → **machine-confirmed**
- At least one `human:<id>` → **human-reviewed**

### Lifecycle
- `status: draft` — work in progress, may be incomplete
- `status: stable` — ready for consumption (default)
- `status: deprecated` — kept for links and history, no longer current

## Operations

### 1. Ingest (on first setup or when sources change)

When a new source is added to `sources/` or initially when building the wiki:

1. Read the source document completely.
2. Extract key concepts and cross-references.
3. Create or update concept pages under `concepts/`.
4. Update `index.md` with links and one-line descriptions.
5. Append an entry to `log.md` with the `## [YYYY-MM-DD] ingest | <description>` format.
6. Update all relevant cross-references across concept pages.

### 2. Query (when answering questions)

1. Read `index.md` first to find relevant pages.
2. Read the concept pages that match.
3. Synthesize an answer with citations (links to concept pages).
4. If the answer is valuable, file it as a new concept page or update an existing one.
5. Optionally append a query entry to `log.md`.

### 3. Update (regular maintenance)

Triggered by the command `project-wiki update` or when instructed:

1. Read `SCHEMA.md` (this file) for conventions.
2. Read `index.md` for the current catalog.
3. Check for:
   - **New sources** in `sources/` not yet ingested → ingest them.
   - **Stale concepts** (`stale_after` passed or `status: deprecated` with no replacement).
   - **Orphan concepts** (pages not linked from `index.md`).
   - **Contradictions** between concept pages.
   - **Missing cross-references** (a concept mentioned in prose but lacking a dedicated page).
   - **Gaps** (important topics from the project not yet covered).
4. Update affected pages.
5. Update `index.md`.
6. Append a lint/update entry to `log.md`.

### 4. Lint (health check)

1. Scan all concept pages for OKF conformance (valid YAML frontmatter, `type` present).
2. Flag stale concepts.
3. Flag orphan pages.
4. Flag broken cross-links.
5. Report findings in `log.md`.

## Project-Specific Type Values

Use these `type` values for concept pages. Choose the most specific one that fits.

| Type | Use for |
|------|---------|
| `Hardware` | Physical components, specs, wiring |
| `Architecture` | Software design, module structure, data flow |
| `Configuration` | Config values, TOML structure, env vars |
| `Phase` | Development phase descriptions and status |
| `Protocol` | OSC, SPI, I²C, communication protocols |
| `Workflow` | Development processes, CLI commands, build steps |
| `Constraint` | Non-negotiable rules, compatibility requirements |
| `Decision` | Architectural decisions with rationale |
| `Issue` | Known problems, bugs, troubleshooting |
| `Reference` | External links, datasheets, documentation |

## Index Format

`index.md` has no frontmatter (except the bundle-root `okf_version`). Body format:

```markdown
# Section Heading

- [Title 1](concepts/page.md) — one-line description
- [Title 2](concepts/other.md) — one-line description
```

Sections should group concepts by type or topic.

## Log Format

`log.md` uses date-grouped entries, newest first:

```markdown
## YYYY-MM-DD
- **Ingest**: Processed `<source>`. Updated 5 pages.
- **Update**: Added cross-reference from X to Y.
- **Lint**: Found 2 stale pages, 1 orphan.
```

## Cross-Linking

- Use bundle-relative paths: `/concepts/hardware-display.md`
- Link concepts to each other where relationships exist.
- Each link is an untyped directed edge in the knowledge graph.

## File Naming

- Concept files: `kebab-case.md` under `concepts/`
- Source files: descriptive names under `sources/`
- No spaces or special characters in filenames.

## Update Command

The `project-wiki update` command:
1. Sources its logic from this SCHEMA.md.
2. Runs the `scripts/update.sh` shell script which invokes the agent to perform the update operation.
3. The agent reads SCHEMA.md → reads index.md → performs lint → updates everything.
