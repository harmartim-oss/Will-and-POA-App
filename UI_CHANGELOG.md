# UI Changelog

## 2025-09-19
### Added
- `DESIGN_SYSTEM_PROPOSAL.md` outlining goals, principles, tokens, components, accessibility, rollout strategy.
- Extended design tokens: semantic surfaces, button tokens, status tokens, motion durations (`micro`, `expressive`), additional easings, z-index scale, overlay variables.
- Accessibility enhancements: skip link (`.skip-link`), `<main id="main">` landmark in `App.jsx`.
- `MOTION_GUIDELINES.md` detailing timing, easing, and motion patterns.

### Changed
- Refactored `button.jsx` to semantic variants (primary, secondary, outline, subtle, ghost, destructive, link), added sizes (`xl`), loading state with spinner, ARIA attributes.
- Refactored `input.jsx` to semantic tokens, added size variants, invalid + loading states.
- Refactored `card.jsx` supporting elevation + interactive focus/hover states and semantic surfaces.

### Pending / Next
- Revamped landing page to align with semantic tokens (in progress).
- Tab component refactor (if present) to semantic tokens.
- Introduce AppShell navigation for authenticated flows.
- Add reduced motion media query adjustments.

### Migration Notes
| Legacy Pattern | New Pattern |
|----------------|------------|
| `bg-blue-600 text-white hover:bg-blue-700` | Use `<Button variant="primary" />` |
| Manual inline spinner | `<Button loading>` prop |
| `border border-gray-200 bg-white` input styling | Semantic default `Input` with tokens |
| Custom card backgrounds | `<Card elevation="md" />` |

### Accessibility
- Visible focus ring consistent across buttons & inputs using token-driven ring.
- Skip link ensures keyboard users can bypass navigation.
- Loading state communicates via `aria-busy` on buttons.

---
This changelog documents incremental UI system evolution.
