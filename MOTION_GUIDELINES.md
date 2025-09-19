# Motion & Interaction Guidelines

## Philosophy
Motion supports comprehension, hierarchy, and feedback. It should not distract or induce motion sickness. Prefer micro-interactions that reinforce causality.

## Core Timing Tokens
| Token | Value | Use |
|-------|-------|-----|
| --duration-micro | 75ms | Tap feedback, color flashes |
| --duration-fast | 150ms | Simple hover transitions |
| --duration-normal | 250ms | Component entry/exit (menus, dialogs) |
| --duration-slow | 350ms | Complex layout shifts, multi-step transitions |
| --duration-expressive | 700ms | Hero / decorative loops |

## Easing Tokens
| Token | Curve | Use |
|-------|-------|-----|
| --ease-out | cubic-bezier(0,0,0.2,1) | Standard appear / hover |
| --ease-in | cubic-bezier(0.4,0,1,1) | Disappear / fade out |
| --ease-in-out | cubic-bezier(0.4,0,0.2,1) | Scale & transform combos |
| --ease-spring | cubic-bezier(0.34,1.56,0.64,1) | Button press release, pop gestures |
| --ease-soft-bounce | cubic-bezier(.33,.07,.19,.97) | Subtle panel/card hover lift |

## Patterns
### Button
State transitions (bg, color, shadow) use `--duration-fast` and `--ease-out`.
Active press adds temporary scale `0.985`.

### Dialog / Modal
Entry: fade + scale from 0.96 to 1 over `--duration-normal`, `--ease-out`.
Backdrop: fade in (opacity 0 -> 1) with same duration.
Exit: reverse using `--ease-in`.

### Dropdown / Menu
Slide + fade: translateY(4px) -> 0; opacity 0 -> 1. Duration `--duration-fast`.

### Toast
Slide from bottom-right (12px) & fade over `--duration-normal`.

### Card Hover (interactive)
Elevation increase + subtle translateY(-2px) using `--ease-soft-bounce` `--duration-normal`.

### Skeleton Loading
Pulse opacity (0.6 -> 1) using 700ms linear infinite.

## Reduced Motion
Respect `(prefers-reduced-motion: reduce)`:
- Disable large hero background movement
- Remove non-essential parallax
- Keep fades (minimal cognitive load)

Example CSS snippet:
```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 1ms !important; animation-iteration-count: 1 !important; transition-duration: 1ms !important; }
  .hero-animated-element { display: none; }
}
```

## Accessibility Considerations
- Duration > 500ms should allow early interruption (e.g., skip / reduce motion setting)
- Avoid simultaneous unrelated animations
- Do not animate opacity + color on text simultaneously (readability)

## Do & Don't
| Do | Don't |
|----|-------|
| Use motion to connect trigger to result | Animate every element on page load |
| Favor subtle scaling (<4%) | Use large bouncy overshoot for legal doc UI |
| Provide focus-visible without relying on motion | Use motion as only focus indicator |
| Batch related entrance animations | Stagger unrelated content excessively |

---
Version 1.0 – evolves as new components are introduced.
