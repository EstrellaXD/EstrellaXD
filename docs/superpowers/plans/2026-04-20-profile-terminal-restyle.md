# GitHub Profile Terminal Restyle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle `README.md` (and its generated tech-stack SVG) to a unified terminal/hacker-scientist aesthetic per spec `docs/superpowers/specs/2026-04-20-profile-terminal-restyle-design.md`, and swap `rsmzml` for `oxion` in featured projects.

**Architecture:** Single-file README edit in seven logical chunks (header, neofetch block, tech-stack SVG reskin, research badges, featured projects, widget retheme, copy polish). The tech-stack SVG is regenerated from `scripts/generate_tech_stack.py` after updating two hex values. No application code is changed. Validation is manual visual inspection of the rendered README on github.com.

**Tech Stack:** Markdown, SVG, GitHub-native widget themes (`github_dark_dimmed`), Python 3 (via `uv run`) for the SVG generator.

---

## Palette reference (used throughout)

| Role | Hex |
|---|---|
| Card bg | `#0D1117` |
| Block bg | `#161B22` |
| Accent primary (green) | `#39D353` |
| Accent secondary (blue) | `#58A6FF` |
| Muted text | `#8B949E` |

---

## File Structure

| Path | Purpose | Action |
|---|---|---|
| `README.md` | Profile README rendered by GitHub | Modify throughout |
| `scripts/generate_tech_stack.py` | Generator for the animated tech-stack SVG | Modify two hex constants |
| `assets/tech-stack-animated.svg` | Output of the generator; embedded in README | Regenerate |

Each task below is self-contained with its own commit so the history is readable and revertible.

---

## Task 1: Reskin tech-stack SVG for dark palette

**Files:**
- Modify: `scripts/generate_tech_stack.py:86` (card `rect` fill) and `scripts/generate_tech_stack.py:68` (label text fill)
- Regenerate: `assets/tech-stack-animated.svg`

- [ ] **Step 1: Update card background fill**

Change `scripts/generate_tech_stack.py` line 86 from:

```python
      f'      <rect width="{ICON_BOX}" height="{ICON_BOX}" rx="12" fill="#f6f8fa"/>',
```

to:

```python
      f'      <rect width="{ICON_BOX}" height="{ICON_BOX}" rx="12" fill="#161B22"/>',
```

- [ ] **Step 2: Update label text color**

Change `scripts/generate_tech_stack.py` line 68 from:

```python
        '  .lb { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;'
        " font-size: 11px; fill: #656d76; }",
```

to:

```python
        '  .lb { font-family: "JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;'
        " font-size: 11px; fill: #8B949E; }",
```

- [ ] **Step 3: Regenerate the SVG**

Run:

```bash
uv run python scripts/generate_tech_stack.py
```

Expected output: `Generated /Users/estrella/Developer/EstrellaXD/assets/tech-stack-animated.svg (<N>,<NNN> bytes)`

- [ ] **Step 4: Sanity check the output**

Run:

```bash
head -c 200 assets/tech-stack-animated.svg
```

Expected: Contains `fill="#161B22"` at least once (the new card bg), and the `.lb` CSS rule contains `fill: #8B949E`.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_tech_stack.py assets/tech-stack-animated.svg
git commit -m "Reskin tech-stack SVG for dark terminal palette"
```

---

## Task 2: Replace header — typing SVG as shell prompt

**Files:**
- Modify: `README.md:1-3` (header anchor + typing SVG)

- [ ] **Step 1: Replace the header block**

In `README.md`, replace lines 1–3 (the current `<a>` + typing SVG) with:

```markdown
<a href="https://github.com/EstrellaXD">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&pause=1000&color=39D353&vCenter=true&width=600&lines=%24+whoami+%E2%86%92+Cancer+Metabolism+Researcher;%24+role+%E2%86%92+Scientific+Tool+Builder;%24+maintains+%E2%86%92+Open+Source" alt="Typing SVG" />
</a>
```

Encoding notes:
- `%24` = `$`, `%E2%86%92` = `→` (right-arrow). Both are safe in a query string value for this widget.
- `font=JetBrains+Mono` and `color=39D353` align with the palette.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Restyle header typing SVG as shell prompt"
```

---

## Task 3: Replace bio section with neofetch block

**Files:**
- Modify: `README.md:5-13` (bio paragraph + one-line project mention + three-bullet list)

- [ ] **Step 1: Replace the bio section**

In `README.md`, replace lines 5 through 13 (from `**Postdoctoral Researcher...**` down through the `- **Languages:**` bullet) with the following fenced block:

````markdown
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
````

Each content line is exactly 48 characters between `│  ` and `│` (48-col interior + 2-col left pad + 1-col right pad + 2 border chars = 52 total cols), satisfying the `≤ 52 columns` constraint from the spec.

- [ ] **Step 2: Verify column widths**

Run:

```bash
awk 'NR>=1 && /│/ { print length($0), $0 }' README.md | head -20
```

Expected: every line containing `│` reports length `52` (plus possibly a trailing newline). If any line is longer, trim trailing spaces before the closing `│` so the box aligns.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Replace bio paragraph with neofetch-style info block"
```

---

## Task 4: Restyle research topic badges

**Files:**
- Modify: `README.md` — the four `img.shields.io/badge/...` lines beneath the tech-stack image (current lines 21–24).

- [ ] **Step 1: Replace the four badge lines**

In `README.md`, replace the four badge lines with:

```markdown
![Cancer Metabolism](https://img.shields.io/badge/Cancer_Metabolism-0D1117?style=flat&labelColor=39D353)
![Single-cell Metabolism](https://img.shields.io/badge/Single--cell_Metabolism-0D1117?style=flat&labelColor=39D353)
![Mass Spectrometry](https://img.shields.io/badge/Mass_Spectrometry-0D1117?style=flat&labelColor=39D353)
![Metabolomics](https://img.shields.io/badge/Metabolomics-0D1117?style=flat&labelColor=39D353)
```

Note the shields.io URL contract: `/badge/<label>-<message>-<color>` — the hex after the dash is the *message* (right-side) color. `labelColor=39D353` sets the *label* (left-side) green strip. Result reads as a terminal tag.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Restyle research topic badges to terminal palette"
```

---

## Task 5: Swap rsmzml → oxion and normalize project structure

**Files:**
- Modify: `README.md` — the `## Featured Projects` section (current lines 28–46).

- [ ] **Step 1: Replace the Featured Projects section**

Replace the entire current `## Featured Projects` section (from the `## Featured Projects` heading down to the closing `---` that precedes `## Selected Publications`) with:

```markdown
## Featured Projects

### [Auto_Bangumi](https://github.com/EstrellaXD/Auto_Bangumi) &nbsp; ![Stars](https://img.shields.io/github/stars/EstrellaXD/Auto_Bangumi?style=flat&color=39D353&labelColor=0D1117)

全自动追番工具 | Fully automated anime tracking & downloading tool

`Python` `Docker` `RSS` `qBittorrent`

### [SCMeTA](https://github.com/EstrellaXD/SCMeTA) &nbsp; ![Stars](https://img.shields.io/github/stars/EstrellaXD/SCMeTA?style=flat&color=39D353&labelColor=0D1117)

A Python library for single-cell metabolism data analysis | 单细胞代谢数据分析工具

`Python` `Single-cell` `Metabolism`

### [oxion](https://github.com/EstrellaXD/oxion) &nbsp; ![Stars](https://img.shields.io/github/stars/EstrellaXD/oxion?style=flat&color=39D353&labelColor=0D1117)

Universal mass spectrometry file reader — fast, cross-platform, no .NET required

`Rust` `Python` `Mass Spectrometry`

---
```

Changes versus current:
1. `rsmzml` removed; `oxion` added with its GitHub description.
2. All three projects now carry a stars badge styled with the palette (SCMeTA and oxion did not previously have one).
3. Identical structure per project: `### [name](url) &nbsp; ![Stars]…` → one-line description → backtick tag row.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Swap rsmzml for oxion and normalize featured projects structure"
```

---

## Task 6: Retheme stats, streak, and activity graph widgets

**Files:**
- Modify: `README.md` — the `## GitHub Stats` section (current lines 61–71) and the `## Activity Graph` section (current lines 75–77).

- [ ] **Step 1: Retheme GitHub stats + top languages**

Replace the `<p>` block under `## GitHub Stats` that contains the two `github-readme-stats-ten-tau-52.vercel.app` images with:

```markdown
<p>
  <img height="170" src="https://github-readme-stats-ten-tau-52.vercel.app/api?username=EstrellaXD&show_icons=true&theme=github_dark_dimmed&hide_border=true&count_private=true" alt="GitHub Stats" />
  &nbsp;&nbsp;
  <img height="170" src="https://github-readme-stats-ten-tau-52.vercel.app/api/top-langs/?username=EstrellaXD&layout=compact&theme=github_dark_dimmed&hide_border=true" alt="Top Languages" />
</p>
```

Only change: `theme=default` → `theme=github_dark_dimmed` in both URLs.

- [ ] **Step 2: Retheme streak stats**

Replace the `<p>` block containing the `streak-stats.demolab.com` image with:

```markdown
<p>
  <img height="170" src="https://streak-stats.demolab.com?user=EstrellaXD&theme=github-dark-blue&hide_border=true" alt="GitHub Streak" />
</p>
```

Rationale: `streak-stats.demolab.com` does not recognize `github_dark_dimmed`; its closest palette match is `github-dark-blue`. Confirm rendering in Step 4.

- [ ] **Step 3: Retheme activity graph**

Replace the `## Activity Graph` section's `img` tag with:

```markdown
<img src="https://github-readme-activity-graph.vercel.app/graph?username=EstrellaXD&theme=github-dark-dimmed&hide_border=true&area=true" alt="Activity Graph" />
```

Only change: `theme=minimal` → `theme=github-dark-dimmed` (hyphenated form — this widget uses hyphens, not underscores).

- [ ] **Step 4: Verify each widget URL returns an image**

Run (one at a time, checking each returns HTTP 200 + content-type `image/svg+xml`):

```bash
curl -sI 'https://github-readme-stats-ten-tau-52.vercel.app/api?username=EstrellaXD&theme=github_dark_dimmed&hide_border=true' | head -5
curl -sI 'https://streak-stats.demolab.com?user=EstrellaXD&theme=github-dark-blue&hide_border=true' | head -5
curl -sI 'https://github-readme-activity-graph.vercel.app/graph?username=EstrellaXD&theme=github-dark-dimmed&area=true' | head -5
```

Expected: each returns `HTTP/2 200` and an SVG/image content-type header. If any returns 4xx/5xx, the theme name is wrong — fall back to `theme=dark` for that widget.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Retheme stats, streak, and activity-graph widgets to dark palette"
```

---

## Task 7: Copy polish — affiliation correction

**Files:**
- Modify: `README.md` — the neofetch `lab` line (written in Task 3).

- [ ] **Step 1: Check whether the correction is already applied**

The neofetch block added in Task 3 already uses `University Children's Hospital, CH` (no "of"). If Task 3 was applied verbatim, this correction is already live. If the user kept `University of Children's Hospital` in their earlier prose and the neofetch line accidentally reintroduced "of", fix it now.

Run:

```bash
grep -n 'University of Children' README.md || echo "No 'University of' found — correction already applied."
```

Expected: no match; the command prints the "already applied" line.

- [ ] **Step 2: If a match is found, replace it**

Only if Step 1 printed a match, replace `University of Children's Hospital` with `University Children's Hospital` (there should be exactly one occurrence after Task 3).

- [ ] **Step 3: Commit only if a change was made**

```bash
git diff --quiet README.md || git commit -am "Fix affiliation wording: University Children's Hospital"
```

(The `git diff --quiet` guard skips an empty commit if nothing changed.)

---

## Task 8: End-to-end visual validation

**Files:** none modified in this task — it only validates.

- [ ] **Step 1: Push the branch to GitHub**

```bash
git push origin $(git branch --show-current)
```

- [ ] **Step 2: Render the README on github.com**

Open `https://github.com/EstrellaXD/EstrellaXD` (or the branch URL if not yet merged to main) in a browser. Visually confirm:
1. Typing SVG shows shell-prompt lines in green JetBrains Mono.
2. Neofetch box renders aligned with no wrapping or broken borders.
3. Tech-stack tiles have dark `#161B22` card backgrounds.
4. Research badges show green label strips with dark message bodies.
5. Featured Projects has exactly three entries: Auto_Bangumi, SCMeTA, oxion — each with a green-accented stars badge.
6. GitHub stats, top-langs, streak, and activity-graph widgets all render with dark backgrounds (no white cards).
7. Snake section still renders (light/dark `<picture>` switch preserved).

- [ ] **Step 3: Mobile viewport check**

In browser devtools, set viewport to `iPhone SE` (375px wide). Re-inspect the neofetch box. Expected: still monospaced, still aligned, no horizontal scroll created on the page.

- [ ] **Step 4: Fix and re-push if any defect appears**

If any defect is visible (box unaligned, widget returning 404, badge wrong color), isolate which Task introduced it, make a focused fix commit, and re-push. Rerun Step 2.

- [ ] **Step 5: Final sign-off**

Once all seven items in Step 2 pass and mobile (Step 3) passes, the restyle is complete. Announce done.

---

## Post-completion notes

- No new files are introduced by this plan. `docs/superpowers/specs/…design.md` and `docs/superpowers/plans/…plan.md` are the only additions outside `README.md` + `assets/` + `scripts/`.
- Running on `main` vs. a feature branch: the user is currently on `main` with a clean tree. Choice of branching strategy is the executor's call; commits are independent per task and trivially revertible either way.
- Rollback: `git revert <task-commit-sha>` per task undoes exactly that task's change without disturbing others.
