# GitHub Profile — Terminal/Hacker-Scientist Restyle

**Date:** 2026-04-20
**Status:** Design approved, pending implementation plan
**Scope:** Restyle `README.md` (and regenerate `assets/tech-stack-animated.svg` if needed) for the `EstrellaXD/EstrellaXD` profile repo.

---

## Goal

Polish the existing profile and establish a distinctive, coherent terminal/hacker-scientist visual identity — without cutting content. The profile serves two audiences (academic collaborators lead, OSS community follows) and must stay credible for the former while keeping the personality of the latter.

## Non-goals

- No new sections or structural reordering (e.g., publications stay above stats, projects stay above publications).
- No removal of third-party widgets (typing SVG, GitHub stats, streak, activity graph, snake) — all are restyled, not deleted.
- No bilingual rewrite. The current mix (English prose, occasional Chinese in project one-liners) stays.

---

## Design

### 1. Visual identity

Single palette applied to every styled element. Using GitHub-native dark-dimmed values so the profile renders consistently in both the viewer's light and dark mode.

| Role | Value | Notes |
|---|---|---|
| Card / background | `#0D1117` | GitHub dark bg |
| Block background | `#161B22` | slightly lighter for cards |
| Accent (primary) | `#39D353` | GitHub's "max contribution" green |
| Accent (secondary) | `#58A6FF` | GitHub link blue, used sparingly |
| Muted text | `#8B949E` | GitHub muted-fg |
| Typeface | `JetBrains Mono` | everywhere typing SVG + neofetch block |

**Widget theme (unifies all decorative blocks):** `github_dark_dimmed`. No custom theme JSON needed — this theme is already supported by every widget currently in use.

### 2. Header — typing SVG as shell prompt

Keep `readme-typing-svg` widget, restyle the call:

- `font=JetBrains+Mono`
- `color=39D353`
- Each rotating line prefixed with `$`, so the typing effect reads as a shell executing commands:
  - `$ whoami → Cancer Metabolism Researcher`
  - `$ role   → Scientific Tool Builder`
  - `$ maintains → Open Source`

### 3. Neofetch-style bio block (signature element)

Replace the current prose paragraph with a fenced monospace block. This is the single most distinctive element:

```
╭─ estrella@zurich ──────────────────────────────╮
│  role      Postdoctoral Researcher             │
│  focus     Cancer & Single-cell Metabolism     │
│  lab       University Children's Hospital, CH  │
│  alma      PhD & BSc Chemistry, Tsinghua       │
│  stack     Python · Rust · TypeScript/Vue      │
│  known for Auto_Bangumi (7.9k★), SCMeTA        │
╰────────────────────────────────────────────────╯
```

**Constraints:**
- Every content line ≤ 52 visual columns so the box doesn't wrap on narrow viewports.
- Rendered inside a GitHub fenced code block (```` ``` ````) for guaranteed monospacing.
- Box characters use standard Unicode box-drawing (╭ ╮ ╰ ╯ ─ │) — confirmed to render correctly in GitHub's README renderer.

### 4. Tech stack & topic badges

- Keep `assets/tech-stack-animated.svg` as-is unless the color audit (see Risks / validation below) finds a mismatch against the palette.
- Research-topic badges (`Cancer_Metabolism`, `Single-cell_Metabolism`, `Mass_Spectrometry`, `Metabolomics`) change from `color=4C566A&style=flat` to `color=0D1117&labelColor=39D353&style=flat` — reads as a terminal tag.

### 5. Featured projects — swap rsmzml → oxion, normalize structure

Three-project list with identical structure:

```
### [<name>](<url>) &nbsp; ![Stars](<stars-badge>)

<one-line description>

`<tag>` `<tag>` `<tag>`
```

Projects:
1. **Auto_Bangumi** — unchanged copy.
2. **SCMeTA** — unchanged copy.
3. **oxion** *(new, replaces rsmzml)*
   - URL: `https://github.com/EstrellaXD/oxion`
   - Description: `Universal mass spectrometry file reader — fast, cross-platform, no .NET required`
   - Tags: `Rust` `Python` `Mass Spectrometry`
   - Stars badge included (same `shields.io/github/stars` pattern as Auto_Bangumi).

### 6. Publications — minimal polish

No structural change. Verify italic venue formatting is consistent across all four entries. Confirm the Google Scholar link still points to the correct profile.

### 7. GitHub stats / streak / activity graph / snake — retheme only

Every widget URL's theme parameter is updated:

| Widget | Current | New |
|---|---|---|
| `github-readme-stats` | `theme=default` | `theme=github_dark_dimmed` |
| `top-langs` | `theme=default` | `theme=github_dark_dimmed` |
| `streak-stats` | `theme=default` | `theme=github_dark_dimmed` |
| `github-readme-activity-graph` | `theme=minimal` | `theme=github-dark-dimmed` *(note hyphen — activity-graph uses different naming)* |
| snake `<picture>` block | no change | no change (already dark-mode-aware) |

All other URL parameters (`hide_border=true`, `count_private=true`, dimensions) stay as-is.

### 8. Copy polish

- **Affiliation correction:** "University of Children's Hospital Zurich" → "University Children's Hospital Zurich" (canonical English name of Universitäts-Kinderspital Zürich). Apply; trivial to revert if the user prefers their current wording.
- Neofetch block lines kept ≤ 52 columns as noted in §3.
- Existing bio prose is fully replaced by the neofetch block. The three-bullet list beneath (`Research`, `Engineering`, `Languages`) is removed — its content is absorbed into the neofetch block's `focus` / `stack` fields to avoid duplication.

---

## Out of scope (deferred)

- Custom themes authored from scratch (only pre-built `github_dark_dimmed` is used).
- New widgets (wakatime, medium, etc.).
- Bilingual expansion.
- A separate personal site / landing page.

---

## Files touched

- `README.md` — section rewrites per §§ 2, 3, 4, 5, 7, 8.
- `assets/tech-stack-animated.svg` — only if color audit in the tech-stack SVG audit (Risks / validation) finds a palette mismatch.
- `scripts/generate_tech_stack.py` — only if SVG is regenerated and the generator hard-codes colors that need updating.

## Risks / validation

- **Neofetch box rendering:** GitHub's markdown renderer has previously had issues with certain box-drawing characters inside code fences on mobile. Validate by previewing the rendered README on github.com (both desktop + mobile viewports) before merging.
- **Theme name drift:** Different widgets use slightly different theme-name conventions (`github_dark_dimmed` vs `github-dark-dimmed`). Validate each rendered widget URL returns a non-error image before committing.
- **Tech-stack SVG audit (the tech-stack SVG audit (Risks / validation)):** Open the existing SVG, check its stroke/fill colors against the new palette. Either (a) confirm it's close enough and leave it, or (b) note which hex values need to change in the generator script.
- **Typing SVG `$` prefix:** The `readme-typing-svg` `lines=` query parameter URL-encodes `$` safely, but validate the rendered widget actually displays the `$` (no over-escaping).

---

## Success criteria

1. Every visual widget uses the unified palette.
2. The neofetch block renders correctly on github.com desktop + mobile.
3. `oxion` replaces `rsmzml` in featured projects; stars badge present.
4. No content loss — every fact from the current README is preserved (either in the neofetch block or its original section).
5. Visual diff (before/after screenshot) demonstrably more distinctive — a reviewer can identify this as "a terminal-themed profile" at a glance.
