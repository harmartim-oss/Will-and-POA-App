# Ontario Wills & POA App – Design System Proposal (v1)

## Goals
Modernize the interface with a consistent, accessible, and scalable design system that:
- Enhances trust and professionalism (legal domain credibility)
- Improves readability & reduces cognitive load
- Ensures WCAG 2.1 AA accessibility
- Supports dark mode & future theming (white label / localization)
- Provides a cohesive visual + interaction language across all components
- Enables rapid feature development via reusable primitives

## Core Principles
1. Clarity over decoration
2. Semantic, token-driven styling
3. Inclusive & accessible by default
4. Progressive enhancement & graceful degradation
5. Performance-aware (minimal layout shift, efficient animations)
6. Consistent motion & feedback

## Design Tokens (Foundation)
Tokens are the single source of truth, exposed via CSS variables. Categories:
- Color (primitive + semantic)
- Typography (families, scale, weights, line heights)
- Spacing (4-based scale)
- Sizing (containers, breakpoints)
- Border (radius, width)
- Elevation (shadows, overlays)
- Opacity (disabled, overlays)
- Motion (durations, easings, key transitions)
- Z-Indices (layers)

### Additions / Adjustments Needed
| Category | Action | Notes |
|----------|--------|-------|
| Color | Introduce neutral blue-gray background ramps for subtle surfaces | Improve contrast vs pure gray in dark mode |
| Color | Add semantic layer tokens (surface-1..4) | For progressive elevation & nested cards |
| Color | Add accent gradients collection | For hero, CTA, highlight states |
| Typography | Define semantic roles (heading-1..6, body, caption, code, legal-footnote) | Map to existing scale, ensure line-height clarity |
| Typography | Introduce font-size clamp utilities for responsive headings | Reduce media queries |
| Spacing | Add micro spacing (space-1.5) and large (space-36, space-48) | For fine control & large sections |
| Radius | Add `--radius-interactive` & `--radius-surface` | Harmonize buttons vs cards |
| Shadows | Add focus-ring shadow token | Replace ad‑hoc rings |
| Motion | Introduce `--duration-micro (75ms)` & `--duration-expressive (700ms)` | Micro for tap feedback, expressive for hero transitions |
| Motion | Define standard easing aliases (in, out, in-out, spring, bounce-soft) | Standardized transitions |
| Z-index | Create scale: dropdown, sticky, overlay, modal, toast, tooltip, skip-link | Avoid collisions |

## Semantic Color Model (Proposed)
```
Surface / Background Layers
--surface-bg          (page background)
--surface-alt         (alternate section background)
--surface-muted       (secondary container)
--surface-elevated    (card / panel)
--surface-overlay     (popover / menu)
--surface-inverted    (inverse foreground usage)

Borders
--border-subtle
--border-default
--border-strong
--border-focus

Text
--text-strong
--text-default
--text-muted
--text-faint
--text-inverse
--text-accent

Interactive (Primary)
--btn-primary-bg
--btn-primary-bg-hover
--btn-primary-bg-active
--btn-primary-text
--btn-primary-ring

Interactive (Neutral / Secondary)
--btn-secondary-bg
--btn-secondary-bg-hover
--btn-secondary-bg-active
--btn-secondary-text

Status
--status-success-bg / text / border
--status-info-bg / text / border
--status-warning-bg / text / border
--status-danger-bg / text / border
```

## Component Guidelines
### Buttons
- Variants: primary, secondary, outline, subtle, ghost, destructive, link
- States: default, hover, active, focus-visible, disabled, loading
- Accessibility: min 44x44px target (touch); visible focus ring separate from box-shadow; ARIA `aria-busy` when loading

### Inputs / Form Controls
- Unified height scale: sm (36px), md (40px), lg (48px)
- Error + success states with text + color + icon (non-color indicator: border style change)
- Inline help & character count pattern

### Cards / Surfaces
- Elevation tiers mapped: surface-muted (0), surface-elevated (sm shadow), surface-high (md shadow)
- Hover-lift pattern optional (`translateY(-2px)` + stronger shadow) at medium duration
- Avoid glass unless meaningful (reduce visual noise)

### Navigation
- Add top-level AppShell layout: header (branding, mode switch, user), left nav (creation steps / documents) when authenticated
- Mobile: collapsible drawer with trap focus & ESC close

### Feedback & System Status
- Toasts: role="status" + aria-live="polite"; color-coded backgrounds; accessible dismiss button
- Loading: skeleton patterns + progress indicators; limit spinners

### Motion Guidelines
| Use Case | Duration | Easing | Notes |
|----------|----------|--------|-------|
| Button hover | 150ms | ease-out | Subtle color/bg shift |
| Dialog open | 250ms | ease-out | Fade + scale 0.96 -> 1 |
| Toast slide-in | 300ms | ease-out | Slide from bottom / right |
| Skeleton fade | 700ms | linear | Pulse opacity 0.6 ↔ 1 |
| Hero decorative | 500–3000ms | ease-in-out | Low contrast, not essential |

### Accessibility Checklist
- Color contrast: ≥ 4.5:1 normal text, 3:1 large text, 3:1 UI components
- Focus visible everywhere (no removal)
- Skip to main content link (already present; ensure anchored id="main")
- ARIA labels only when natural semantics insufficient
- Keyboard navigation: tab sequence logical; ESC closes overlays
- Reduce motion preference respected: disable large hero animation & parallax if `(prefers-reduced-motion: reduce)`

## Implementation Phases
1. Foundation: Add new tokens + semantic layer (non-breaking) & doc
2. Component Refactor: Buttons, inputs, card, tabs, badge, modal (if added)
3. Layout & Navigation: AppShell & responsive improvements
4. Landing & Marketing Sections: Hero, features, trust, footer
5. Accessibility & QA: Audits + automated checks (axe / Lighthouse)
6. Polishing: Micro-interactions, animation tuning, performance

## Incremental Strategy
- Introduce tokens with fallback to existing (dual-run)
- Gate refactored components behind feature flag if needed
- Provide migration table in docs (old utility → new semantic class)

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Token naming collision | Visual regressions | Prefix new semantic tokens with `--semantic-` initially |
| Inconsistent adoption | Fragmented UI | Provide checklist & lint rule suggestions |
| Performance regression (extra layers) | Slower load | Purge unused styles; avoid deep nesting |
| Accessibility regressions | Legal risk | Automated contrast + keyboard test before merge |

## Success Metrics
- 0 critical contrast failures (axe scan)
- Reduction in custom per-component CSS overrides (>30%)
- Faster perceived task completion (qualitative feedback)
- Improved Lighthouse Performance > 90, Accessibility > 95 (desktop)

## Next Steps
- Approve token expansion list
- Implement new tokens & semantic layers
- Refactor button & input as reference implementation
- Roll out remaining components

---
Draft v1 – open for feedback.
