# Wireframes v0.1

Editable SVG wireframes built on Finance Tracker DS v0.1 (440 frame, 36 margins, 368 / 177 widths).

**Import into Figma:** drag `all-screens.svg` (or a single screen) onto the canvas. Shapes and text come in as editable layers, named by component.

| File | Screen |
|---|---|
| 01-onboarding-savings-range.svg | Savings range onboarding |
| 02-wealth-home.svg | Net worth, 5Y forecast with scenario band, goal timeline |
| 03-spend-home.svg | Budget gauge, room to spend, category rebalance |
| 04-subscriptions.svg | Subscriptions with unused-subscription insight |
| 05-breathe-in.svg | Breathe-in interstitial |

For the interactive version of the wealth home (goal drag, detail sheet, AI what-if), see the [Wealth portfolio prototype](../../prototypes/wealth-portfolio/).

To change copy or layout, edit `build.py` and run `python3 build.py`.
Fonts: Inter (text) and Space Mono (numbers) — install both so Figma keeps text editable.
