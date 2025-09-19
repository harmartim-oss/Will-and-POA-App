# Design System Rollout Plan

## Phase Overview
| Phase | Scope | Success Criteria |
|-------|------|------------------|
| 1. Foundations | Tokens + semantic utilities | No visual regressions, tokens loaded everywhere |
| 2. Primitives | Button, Input, Card, Badge, Tabs | Components consume tokens, pass a11y checks |
| 3. Layout | AppShell, Navigation, Footer | Consistent responsive layout, skip link works |
| 4. Workflow Screens | Document Creation & Editing flows | Uniform spacing & headings, improved clarity |
| 5. Marketing | Landing page sections updated | Lighthouse A11y >95, CLS <0.02 |
| 6. QA & Hardening | Contrast, keyboard, reduced motion | Zero critical axe issues |
| 7. Optimization | Dead CSS purge, bundle diff | <5% CSS growth vs legacy baseline |

## Migration Checklist
For each component:
- [ ] Uses only design tokens (no raw hex/rgb except in tokens)
- [ ] Focus-visible state present & visible
- [ ] Keyboard navigation logical
- [ ] Variants documented
- [ ] Loading & disabled states tested
- [ ] Dark mode parity verified
- [ ] Reduced motion respected

## Adoption Strategy
1. Dual Run: Keep old utility-based styling in non-refactored areas until replaced.
2. Component Gate: Optional feature flag (`ENABLE_NEW_UI`) via env if needed.
3. Documentation First: Merge proposal & guidelines before mass refactors.
4. Iterative PRs: One or two component refactors per PR to ease review.
5. Visual Regression: Manual screenshot diff (future: integrate playwright + percy/alternatives).

## Risk Mitigation
| Risk | Mitigation |
|------|------------|
| Partial adoption fragmentation | Track progress with migration checklist |
| Performance regression | Purge unused Tailwind utilities post-migration |
| Accessibility drift | Run axe + Lighthouse in CI stage |
| Theming inconsistencies | Centralize overrides in tokens only |

## Tooling Enhancements (Future)
- Lint rule scanning for disallowed raw color values
- Storybook / Component catalog for isolated testing
- Visual regression tests

## Communication
- Add section in README for Using the Design System
- Update CHANGELOG with each phase completion

## Rollback Plan
If severe regression: revert component PR (tokens remain harmless). Maintain atomic commits for each component to reduce blast radius.

## Status Dashboard (Initial)
| Component | Status |
|-----------|--------|
| Button | ✅ Refactored |
| Input | ✅ Refactored |
| Card | ✅ Refactored |
| Tabs | ⏳ Pending |
| Badge | Pending |
| Toast | Pending a11y improvement |
| Landing Page | Pending alignment |

---
Version 1.0 – evolves with adoption.
