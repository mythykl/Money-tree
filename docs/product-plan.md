# Money-tree · Wealth & Spend — Product Plan v0.1

**Status:** Draft · Sep 2026
**Design system:** [Finance Tracker · Design System v0.1 (Figma)](https://www.figma.com/design/XuoHuziR2FNT1EZoEcd3Tl/Finance-Tracker-%C2%B7-Design-System-v0.1?node-id=2-27)
**Code:** github.com/mythykl/Money-tree (Vercel: money-tree-financetracker)

---

## 1. Product frame

**User:** Indian, 25–35, early-to-mid career. Salary is growing, first big goals are coming up (house, car, travel, venture), and they hold a mix of SIPs, PPF and maybe some stocks or gold.

**Core promise:** "See where your money is heading, and feel calm about it."

**Principles for every feature**
- **Ranges over single numbers.** A 10-year forecast drawn as one line is dishonest. Show a band.
- **Calm over urgency.** The "breathe in" feature sets the tone for everything else.
- **Spend with intent.** The goal is intentional spending, not maximum saving. That's why the miser nudge exists.
- **Explain every number.** Any figure the AI or the forecast produces should be tappable to show *why*.

---

## 2. Information architecture

| Pillar | What it answers | Features |
|---|---|---|
| **Wealth** | "Where am I, and where am I heading?" | Forecast, scenarios, horizons, scrubbing, market scenarios, breathe-in |
| **Spend** | "Where is my money going, and is that okay?" | Savings range, budget, sliders, subscriptions, pattern analysis |
| **Habits** | "Am I staying consistent?" | Streaks, leaderboard, goal map, credits |
| **AI layer** (runs across all three) | "Explain this, what if, what should I change?" | Chat, insights, goal-linked suggestions |

---

## 3. Wealth pillar

### 3A. Forecast engine (the core)

These are the inputs the forecast needs. Each one should be visible and editable so users trust the output.

- **Income curve:** current CTC plus expected growth. Offer promotion presets: "steady", "fast track", "switching jobs every 2–3 years".
- **Tax:** model both the old and new regimes. Keep the slabs in a config file you update after each Budget, never hard-coded.
- **Inflation:** default around 5–6%, user-adjustable. Add an "in today's rupees" toggle, because ₹1 Cr in 2036 is not ₹1 Cr today.
- **Return assumptions per asset class:** equity, debt, PPF, gold, real estate, cash.
- **Goals as events on the timeline.** Each goal type affects the curve differently:

| Goal type | Example | Effect on net worth |
|---|---|---|
| **Appreciating asset** | House | Big dip at purchase: down payment plus stamp duty and registration (several % depending on state). Then property value minus outstanding loan starts building back. EMI replaces rent in cash flow. |
| **Depreciating liability** | Car | Permanent dent. The car loses value fast (roughly 15–20% in year one) and adds ongoing costs: fuel, insurance, service. The curve never recovers that gap. |
| **Experience** | Trip, wedding | One-time dip, no asset. Show it honestly but kindly ("₹2.4L now = ₹6.1L less at 40"). Don't shame it. |
| **Venture** | Own startup | Income drops, capital goes out, and the outcome is high-variance. The curve splits into branches: fails, breaks even, grows. |

- **Goal timeline strip** sits under the chart, with goal markers pinned to their dates. Dragging a goal later (say, house from 2029 to 2031) redraws the curve live. This is the "aha" moment.
  - *Prototyped* in the Wealth portfolio [prototype](../prototypes/wealth-portfolio/): House snaps to whole years (2028–2035), a dashed ghost marks the original date, and the caption, total and chart tooltip update as you drag ("Moving House '29 → '31 adds ₹6.4L by 2036").

### 3B. Scenario lines

- **Baseline / threshold:** current trajectory if nothing changes.
- **Current:** actual path so far.
- **Potential:** the "good habits" path, e.g. SIP step-up of 10% a year and capped expenses.
- **Floor (optional):** an emergency-fund minimum. If the forecast dips below it, warn the user.
- **Headline figure:** the gap between Baseline and Potential, e.g. "Good habits are worth ₹38L by 2036."

### 3C. Time horizons

- Offer **3M · 1Y · 5Y · 10Y**. This extends the existing 6M/1Y/5Y toggle.
- **Short range (3M–1Y):** mostly real data plus known events (bonus, EMI start). Draw a tight line.
- **Long range (5Y–10Y):** draw a widening fan chart, because uncertainty grows with time.

### 3D. Scrubbing

- Dragging across the chart shows a tooltip card with net worth, asset split, goals hit by then, and age ("age 31").
- Tapping a point opens a detail sheet with the full breakdown for that month or year.
- *Prototyped:* the tooltip carries a ↗ button that opens the detail sheet as a bottom sheet over the dimmed screen: date and age, value with range, allocation bar and legend, and "Goals hit by then".

### 3E. AI chat

- Scope it to "what if" and "explain" questions, e.g. "What if I buy the car in 2027 instead?" or "Why did my 5Y number drop?"
- The best pattern is for the AI to answer by **redrawing the chart as a scenario**, not only replying with text.
- *Prototyped:* the detail sheet ends with an editable suggested question and an **Ask** button. Asking expands the sheet to full height and answers with a one-line headline, a short reason, a scenario card (delta by 2036 and a mini chart against the current plan), **Apply to my plan** / **Show math**, follow-up suggestions and an "Ask a what-if…" input.

### 3F. Market and news impact

- Frame this as **scenarios, not predictions**, e.g. "If markets fall 20% this year, here's your curve" or "RBI cut rates; here's what that means for your FD ladder."
- ⚠️ **Regulatory:** in India, personalised investment advice ("buy this fund") generally requires SEBI registration as an Investment Adviser. Keep the AI to education, projections and scenarios unless registration is planned. Check with legal early, because this shapes the AI's copy.

### 3G. Breathe-in

- **Trigger:** more than N portfolio opens a day, or repeated opens during a market drop.
- **Response:** a calm interstitial, not a block. "Your 10-year plan hasn't changed since this morning," with a short breathing animation on the night gradient.
- **Rationale:** frequent checking makes losses feel bigger and leads to worse decisions (myopic loss aversion).
- ⚠️ **Tension:** streaks and leaderboards push people to open the app more, which works against this feature. Reward *logging and consistency*, never *checking the portfolio*.

---

## 4. Spend pillar

### 4A. Savings range (the entry point)

- Ask during onboarding: "How much do you want to save each month?"
- Take a **range**, not a single number: a minimum (e.g. ₹15k) and a stretch target (e.g. ₹25k).
- Everything else in Spend is calculated from this:
  `spendable = income − fixed costs − savings minimum`

### 4B. Budget and the "you can spend more" state

- **Budget gauge:** the Sun gauge from the DS.
- **Miser detection:** trigger only when *all* of these hold:
  - the savings range is already met
  - the emergency fund is healthy
  - spending is well under budget
- **What the user sees:** a ghost-filled area on the chart showing unused room, e.g. "₹8,200 of guilt-free money this month."
- **Category sliders:**
  - Fixed categories (rent, EMI) are locked.
  - Moving a flexible slider takes from or gives to the others, so the total stays constant.
  - The donut re-balances live as you drag.

### 4C. Subscriptions

- **Detection:** UPI autopay mandates, card statements, SMS parsing. For bank data, use RBI's **Account Aggregator** framework, which is consent-based and compliant.
- **Knowing whether a subscription is "used" is harder than it sounds**, because you can't see Netflix usage directly. Options, in order of feasibility:
  1. Ask the user every quarter.
  2. Read app usage via Android usage-access permission (not available on iOS).
  3. Read email receipts and activity.
- **Groups:** Entertainment (OTT) · AI tools · Work tools. Flag work tools that may be reimbursable or tax-deductible.
- **Insight examples:**
  - "No Spotify usage in 3 months"
  - "You pay for 2 AI tools"
  - "Switching Figma to annual saves ₹X"
  - "Price went up last cycle"

### 4D. Goal-linked AI suggestions

- Always tie a suggestion to a goal, e.g. "Cut dining out by ₹3k/month and the Goa trip moves from March to January."
- Show trade-offs in both directions. Don't only suggest cuts.

### 4E. Pattern analysis: intentional trade-offs vs. risky ones

| Pattern | Example | Response |
|---|---|---|
| **Intentional trade-off** | Walks to work, cooks at home, spends on Myntra | Celebrate it. This user knows their priorities. |
| **Risky** | Food delivery going up alongside medical and pharmacy spend going up | Flag it gently: "These two categories are rising together, want to look?" |

⚠️ **Care needed**
- Make it **opt-in**.
- Show what the AI inferred and let users correct it.
- Never moralise; avoid words like "junk food".
- India's DPDP Act 2023 applies, so consent and purpose limitation matter.

---

## 5. Habits pillar

| Feature | Recommendation |
|---|---|
| **Streaks** | Streaks for daily logging and no-spend days, shown on the heatmap. Allow streak freezes so one bad day doesn't reset months of progress. |
| **Leaderboard** | Rank **behaviour, never amounts**: % of goal reached, consistency score. Opt-in, within friend groups or as a percentile ("more consistent than 72% of people your age"). Publicly comparing rupees causes shame and envy. |
| **Goal map (priority vs time)** | Priority on one axis, time left on the other, so users see which goals are urgent and important. *(Interpretation — confirm.)* |
| **In-app credits** | Reward accurate logging, hitting savings ranges and reviewing subscriptions. Never reward spending itself. Redemption is still TBD. |

---

## 6. Mapping features to the design system

| Feature | DS component |
|---|---|
| Forecast hero | 01 Net worth hero (projection bars), extended into a fan chart |
| Horizon toggle | 04 Line/area chart segmented toggle, adding 3M and 10Y |
| Budget / savings goal | 03 Sun gauge (budget) · Moon gauge (savings) |
| Category rebalance | 05 Allocation donut plus new slider rows |
| Subscription renewal | 05 Bill due card (Pay/Later → Keep/Cancel) |
| Streaks / no-spend days | 07 Spend calendar heatmap |
| Breathe-in screen | Night gradient card |
| Scrub tooltip | 04 Inverse tooltip (pill bar chart) |
| Transactions / categories | 06 List & breakdown |

**New components needed** (the goal timeline strip and AI chat sheet are prototyped in the Wealth portfolio [prototype](../prototypes/wealth-portfolio/); still to be built as DS components)
- [ ] Fan chart (scenario bands)
- [ ] Goal timeline strip with draggable markers
- [ ] Category slider row
- [ ] AI chat sheet with inline chart
- [ ] Insight card
- [ ] Breathe-in interstitial

---

## 7. Build phases

**MVP**
- [ ] Savings range onboarding
- [ ] Expense tracking (manual entry plus SMS import)
- [ ] Budget gauge
- [ ] Subscriptions list
- [ ] Forecast with three scenario lines and horizon toggle

**v2**
- [ ] Goals on the timeline with asset/liability logic
- [ ] Scrubbing and detail sheet
- [ ] AI insights: unused subscriptions, goal-linked suggestions
- [ ] Streaks
- [ ] Breathe-in

**v3**
- [ ] AI chat with scenario redraws
- [ ] Market-scenario layer
- [ ] Pattern analysis
- [ ] Leaderboard
- [ ] Credits

**Engineering note**

Write the forecast engine as **one pure function**:

```
forecast(profile, goals, assumptions) → { monthlySeries, bands }
```

The chart, the scrubber, the AI "what if" answers and all three scenarios call this same function, so they stay consistent.

---

**Prototypes**

- [Wealth portfolio flow](../prototypes/wealth-portfolio/) (Sep 2026): goal timeline drag → scrub tooltip → detail sheet → AI what-if answer. Live at `/prototypes/wealth-portfolio` on the Vercel project. Numbers come from a placeholder curve, not the forecast engine.

---

## 8. Open decisions

- [ ] **Data source for v1:** manual entry / SMS parsing / Account Aggregator?
- [ ] **Advice boundary:** education and scenarios only, or is SEBI IA registration on the roadmap?
- [ ] **Credits:** what can users redeem them for?
- [ ] **Breathe-in trigger:** what counts as "too often"?
- [ ] **Goal map:** confirm the priority-vs-time interpretation.
- [ ] **Detail sheet entry:** keep the ↗ button in the tooltip as the only way in, or also open the sheet on tapping the chart?
- [ ] **Apply to my plan:** what exactly does it change (goal date, SIP amount), and can it be undone?
