# Design System V2 (Modernization Roadmap)

This document captures the new visual language prior to implementation. It introduces an updated palette, typography, spacing refinements, elevation model, motion guidelines, and semantic token architecture. Backwards compatibility is preserved via alias mapping to existing `--color-primary-*` etc.

## 1. Goals
- Improve readability & hierarchy
- Increase accessible color contrast (WCAG AA+ targets)
- Introduce fluid & responsive typography
- Normalize spacing rhythm (4px base with selective 2px micro spacing)
- Unify surface layering & elevation
- Provide motion tokens tuned for intent (micro vs expressive)
- Prepare for theming / white‑label capability

## 2. Core Primitives

### 2.1 Color Ramps (Base / Light Theme)
Brand (Blue)
```
--color-brand-50:  #f2f7ff
--color-brand-100: #e4efff
--color-brand-200: #c2dcff
--color-brand-300: #9cc6ff
--color-brand-400: #6aa9ff
--color-brand-500: #3a8bff
--color-brand-600: #186fe6
--color-brand-700: #0d57b3
--color-brand-800: #0b478f
--color-brand-900: #09376b
--color-brand-950: #052245
```
Accent (Teal)
```
--color-accent-50:  #f0fdfa
--color-accent-100: #ccfbf1
--color-accent-200: #99f6e4
--color-accent-300: #5eead4
--color-accent-400: #2dd4bf
--color-accent-500: #14b8a6
--color-accent-600: #0d9488
--color-accent-700: #0f766e
--color-accent-800: #115e59
--color-accent-900: #134e4a
--color-accent-950: #042f2e
```
Neutral (Refined grayscale emphasizing mid-tone legibility)
```
--color-gray-0:  #ffffff
--color-gray-50: #f8fafc
--color-gray-100:#f1f5f9
--color-gray-150:#e9edf3
--color-gray-200:#e2e8f0
--color-gray-300:#cbd5e1
--color-gray-400:#94a3b8
--color-gray-500:#64748b
--color-gray-600:#475569
--color-gray-700:#334155
--color-gray-800:#1e293b
--color-gray-900:#0f172a
--color-gray-950:#020617
```
Semantic ramps reuse existing success / warning / danger to avoid churn.

### 2.2 Alias & Backwards Compatibility
```
--color-primary-*  => --color-brand-*
--text-accent      => brand / accent usage depends on context
```
Existing components using `--color-primary-*` continue to function.

### 2.3 Semantic Layer Tokens
```
--surface-1: base background
--surface-2: subtle elevated block
--surface-3: card default
--surface-4: popover / dropdown
--surface-5: modal / dialog
--border-subtle: low-contrast separators
--border-strong: key delineation
--focus-ring-color: accent/brand mix for contrast
```
Dark mode derives via algorithmic inversion + manual tuning (maintain >= 4.5:1 for text on surfaces).

### 2.4 Typography
Font stack upgrade: `Inter` (variable) for UI, `Source Serif 4` (optional) for long-form content.
```
--font-sans: 'InterVariable', 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif;
--font-serif: 'Source Serif 4', ui-serif, Georgia, serif;
--font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
```
Fluid scale (clamped):
```
--fs-xs: clamp(0.72rem, 0.70rem + 0.1vw, 0.76rem)
--fs-sm: clamp(0.84rem, 0.80rem + 0.2vw, 0.9rem)
--fs-base: clamp(1rem, 0.95rem + 0.25vw, 1.075rem)
--fs-lg: clamp(1.125rem, 1.05rem + 0.35vw, 1.25rem)
--fs-xl: clamp(1.35rem, 1.2rem + 0.6vw, 1.6rem)
--fs-2xl: clamp(1.75rem, 1.5rem + 1vw, 2.15rem)
--fs-3xl: clamp(2.25rem, 1.9rem + 1.6vw, 2.9rem)
--fs-4xl: clamp(2.75rem, 2.2rem + 2.4vw, 3.5rem)
```
Line-height system:
```
--lh-tight: 1.2
--lh-snug: 1.3
--lh-normal: 1.5
--lh-relaxed: 1.65
```

### 2.5 Spacing (extending existing)
Add half-steps & container gutters:
```
--space-1-5: 0.375rem
--space-2-5: 0.625rem
--space-7: 1.75rem
--space-14: 3.5rem
--space-18: 4.5rem
--gutter-sm: clamp(1rem, 2vw, 2rem)
--gutter-lg: clamp(2rem, 4vw, 4rem)
```

### 2.6 Radii & Shape
```
--radius-xs: 2px
--radius-sm: 4px
--radius-md: 6px
--radius-lg: 10px
--radius-xl: 14px
--radius-2xl: 20px
--radius-round: 9999px
--radius-fluid: clamp(0.75rem, 1vw, 1.25rem)
```
(Where possible map old names to closest new size.)

### 2.7 Elevation & Shadows
Soft, layered shadows with opacity tuned for light/dark:
```
--elevation-1: 0 1px 2px -1px rgb(0 0 0 / 0.08), 0 1px 1px rgb(0 0 0 / 0.04)
--elevation-2: 0 2px 4px -1px rgb(0 0 0 / 0.10), 0 1px 2px rgb(0 0 0 / 0.06)
--elevation-3: 0 4px 8px -2px rgb(0 0 0 / 0.12), 0 2px 4px rgb(0 0 0 / 0.08)
--elevation-4: 0 8px 16px -4px rgb(0 0 0 / 0.14), 0 4px 6px rgb(0 0 0 / 0.10)
--elevation-5: 0 12px 28px -6px rgb(0 0 0 / 0.18), 0 6px 10px rgb(0 0 0 / 0.12)
```
Dark mode will reduce spread & increase transparency.

### 2.8 Motion
Intent groupings:
```
--motion-micro: 90ms
--motion-fast: 150ms
--motion-base: 220ms
--motion-slow: 340ms
--motion-expressive: 600ms
--ease-standard: cubic-bezier(.4,0,.2,1)
--ease-entrance: cubic-bezier(0,0,.2,1)
--ease-exit: cubic-bezier(.4,0,1,1)
--ease-emphatic: cubic-bezier(.68,-0.55,.265,1.55)
```
Reduced motion handling: prefer opacity / scale <= 1.02, guard with `@media (prefers-reduced-motion: reduce)`.

### 2.9 Gradients & Effects
```
--gradient-brand: linear-gradient(90deg, var(--color-brand-600), var(--color-accent-500))
--gradient-accent: linear-gradient(90deg, var(--color-accent-500), var(--color-brand-500))
--gradient-surface: linear-gradient(145deg, var(--surface-2), var(--surface-3))
--blur-backdrop: 20px
```

### 2.10 Focus & Accessibility
```
--focus-ring-width: 3px
--focus-ring-color: var(--color-accent-500)
--focus-ring: 0 0 0 var(--focus-ring-width) var(--focus-ring-color)
--focus-ring-offset-color: var(--surface-1)
--focus-ring-offset: 0 0 0 2px var(--focus-ring-offset-color)
```
Contrast objectives: Primary text >= 7:1, secondary >= 4.5:1, interactive states > 3:1 delta vs background.

## 3. Mapping Strategy
- Add new primitives alongside existing tokens.
- Alias existing `--color-primary-*` → new `--color-brand-*` so components continue working.
- Introduce semantic surfaces (`--surface-{1..5}`) then refactor components gradually.

## 4. Implementation Phases
1. Ship tokens (no breaking changes).
2. Update global typography + font imports.
3. Refactor primitives (buttons, inputs, cards, tabs, badges).
4. Update layout & spacing wrappers.
5. Apply surface/elevation layers to key screens.
6. Dark mode tuning + accessibility validation.

## 5. Validation Checklist
- A11y: Run automated axe scan + manual keyboard audit.
- Color contrast: Verify via tooling (contrast matrix for surfaces vs text roles).
- Dark mode parity: No unintended contrast inversions.
- Motion: Confirm respects reduced-motion.

## 6. Next Steps
Proceed to Phase 1 (token injection) → modify `tokens.css` with additions + aliases.

