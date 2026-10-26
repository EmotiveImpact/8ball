# 8BALL visual direction: the quiet operations room

Revision 1.0, 26 October 2026. **Design direction and recommendation. No runtime or stylesheet change is made by this document.**

This builds on [the black operator visual system](../v2/BLACK-VISUAL-SYSTEM.md) and [the relationship explorer](../v2/GRAPH-EXPLORER.md). It records what the interface looks like today, assesses it, and recommends the direction to pursue next.

## 1. Where the interface stands today

Evidence: `web/v2/style.css`, `web/v2/index.html` and a render of `scripts/design_preview.py` with fictional Northstar data.

| Area | Current state |
| --- | --- |
| Mood | Near-black graphite "situation room". Calm, sparse, professional. Reads as an operator's console rather than a consumer app. |
| Canvas and surfaces | `--bg #08090b`, `--panel #111216`, `--panel2 #1b1d22`, borders `--line #2b2e35`. |
| Text | `--ink #f2f3f5` primary, `--sub #a9adb7` secondary. |
| Accent | Off-white `#f1f2f4`. Primary buttons are white with near-black labels. |
| State colours | Desaturated pastels: red `#efb1a9`, amber `#e5c08a`, blue `#b1c6df`, plus a sage green used in the graph. Reserved for labelled evidence, approval and risk states. |
| Type | Inter is named first but never loaded, so most users see the system sans (San Francisco, Segoe UI). Monospace for codes and identifiers. Light headline weights (450) with tight negative tracking; small uppercase kickers with wide letter spacing. |
| Brand mark | A white ring holding a solid "8" ball, wordmark "8BALL", signature "POWERED BY ENDSTATE". |
| Components | Framed panels with 5 to 9px radii, pill filter chips with counts, tabbed workspaces, a right-hand inspector, a relationship graph with shape-coded nodes (diamond outcomes, squares actions, dots people and conditions), Now rail, route comparison and modal dialogs. |
| Motion | Minimal. Short background transitions and a busy pulse, both disabled under `prefers-reduced-motion`. |
| Accessibility hooks | Visible focus rings, skip link, `forced-colors` support, reduced-motion support. |

### What works

- **The mood fits the job.** A fixer handling a live, sensitive situation needs focus and gravity. The dark, low-chroma palette keeps attention on the case, and the restraint signals seriousness.
- **Colour carries meaning, not decoration.** Reserving colour for labelled states, and pairing it with shapes and words, is the right discipline for an evidence product.
- **The voice matches the visuals.** "Find a way through", "A clearer picture. A better next move." and "Recorded connections, not inferred causation" are calm and precise.

### What is holding it back

1. **The token system has drifted.** The stylesheet defines 11 colour tokens yet contains **331 distinct hard-coded hex values** (`#292929`, `#303030`, `#333`, `#141414` and dozens of near-identical greys). Panels that should match drift by one or two shades, and any future theme change is very expensive.
2. **Text is too small for sustained work.** Font sizes of 8px (25 uses), 9px (70) and 10px (68) carry labels, kickers, chip counts and metadata. At those sizes on a dark ground, `--sub` text falls short of comfortable reading and of WCAG intent, even where raw contrast passes.
3. **The type is accidental.** Inter is requested but not shipped, so the product looks different on every operating system and the light 450 headline weight renders thinly on Windows.
4. **Scales are improvised.** Seven radii (3 to 10px plus 20px), roughly twenty font sizes and seventeen separate breakpoints between 600px and 1600px. Each screen is individually tuned rather than assembled from a system.
5. **The graph gets dense quickly.** Overlapping labels and crossing edges in the Connections view make the central visual feel busier than the rest of the product.
6. **Exports have no counterpart.** Audit exports, plan reviews and client-facing summaries will be printed or shared, and a black-only identity has no light or print rendering.

## 2. Recommended direction

**Keep the black operations-room identity and turn it into a disciplined system.** The concept is right for the audience and is already reflected in the PRD amendment, so a change of mood would cost credibility for little gain. The next step is consistency, legibility and a second, light rendering for documents.

Working name: **the quiet operations room**. Three principles guide every decision:

- **Calm under pressure.** Low chroma, generous spacing, nothing that blinks or competes. Urgency comes from content and labelled state, never from decorative colour.
- **Provenance is visible.** Sources, revisions and evidence links always look the same wherever they appear, so an operator learns to trust and trace them at a glance.
- **Nothing implies more than it knows.** Neutral styling for conditional plans and unverified material; colour and weight are earned by reviewed state.

### 2.1 Palette

Collapse the 331 values into one ramp and a small set of semantic tokens.

| Token | Value | Use |
| --- | --- | --- |
| `--grey-0` | `#08090b` | Canvas |
| `--grey-1` | `#111216` | Panels |
| `--grey-2` | `#1b1d22` | Raised controls, hovered rows |
| `--grey-3` | `#2b2e35` | Borders and dividers |
| `--grey-4` | `#3c4250` | Strong borders, disabled outlines |
| `--grey-6` | `#8d94a2` | Tertiary text, icons |
| `--grey-7` | `#b4b8c2` | Secondary text (lifted slightly from `#a9adb7`) |
| `--grey-9` | `#f2f3f5` | Primary text, primary buttons |
| `--state-risk` | `#efb1a9` | Risks, refusals, blockers |
| `--state-caution` | `#e5c08a` | Pending review, approaching deadlines |
| `--state-evidence` | `#a9d4bb` | Reviewed and supported evidence |
| `--state-info` | `#b1c6df` | Neutral information, selection |

Rules: every colour in the stylesheet resolves to a token; state colours appear only beside a text label or shape; no state colour fills an area larger than a badge, edge or thin rule; the accent stays white. A single restrained signature colour may be considered later for the brand mark only, never for state.

### 2.2 Typography

- **Ship a typeface.** Self-host Inter (variable) for interface text and pair it with a monospace such as JetBrains Mono or IBM Plex Mono for identifiers, revisions and source excerpts. This fixes cross-platform drift and gives provenance its own recognisable voice.
- **Set a floor of 12px** for any text a user must read, with 11px kept for uppercase kickers only. Remove 8px and 9px sizes.
- **Adopt a fixed scale:** 11, 12, 13, 14, 16, 20, 24, 32 and 40px. Headlines at 500 weight with modest negative tracking; body at 400 with 1.6 line height.
- **Reduce kicker tracking** from 1.8px to about 1px so small capitals stay legible.

### 2.3 Shape, space and layout

- **Radii:** three steps only. 4px for chips and inputs, 8px for panels and cards, full round for status dots and avatars.
- **Spacing:** a 4px base with steps of 4, 8, 12, 16, 24, 32 and 48px.
- **Breakpoints:** consolidate to four (600, 900, 1200, 1600px) and let components flex inside them.
- **Elevation:** keep borders and shade steps rather than drop shadows; dialogs may use one soft shadow to separate from the canvas.

### 2.4 Components to standardise first

1. **Evidence chip:** source name, revision and review state in one consistent element, used in the inspector, plans and timeline.
2. **State badge:** shape plus label plus colour, one component for risk, caution, evidence and info.
3. **Panel and inspector:** one header pattern (kicker, title, action) shared by every panel.
4. **Filter chip with count:** already close; move to tokens and the 12px floor.
5. **Graph node and edge:** keep the shape language, add label collision avoidance, fade non-neighbour edges on focus, and show historical links as dashed at lower opacity.

### 2.5 Light rendering for documents

Add a light "paper" theme used for print, PDF and shared exports, built from the same tokens inverted (warm off-white ground, graphite ink, the same state hues darkened for contrast). The interactive workspace stays dark by default; documents that leave the situation room should feel like formal case papers.

### 2.6 Motion

Keep it minimal. Allow short fades (120 to 160ms) for panel changes and a gentle focus transition in the graph. No looping or ambient animation, and continue to honour `prefers-reduced-motion`.

## 3. Suggested sequence

| Step | Work | Outcome |
| --- | --- | --- |
| 1 | Introduce the token set and replace hard-coded colours, without visual change beyond near-duplicate greys merging. | One source of truth; theming becomes cheap. |
| 2 | Self-host the typefaces and apply the type scale and 12px floor. | Consistent, more legible interface on every platform. |
| 3 | Standardise radii, spacing and breakpoints. | Screens assembled from a system rather than tuned individually. |
| 4 | Build the evidence chip and state badge, then refit the inspector and plans. | Provenance reads identically everywhere. |
| 5 | Improve graph legibility (labels, focus fading). | The central view matches the calm of the rest of the product. |
| 6 | Add the light paper theme for exports and print. | Client-ready documents from the same system. |

Each step should be checked against the existing native browser suites and the accessibility notes in [ACCESSIBILITY.md](../v2/ACCESSIBILITY.md). This direction does not change any acceptance requirement, and adopting it is a design decision for the owner to record in the delivery ledger.
