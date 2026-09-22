# Mid-lifecycle churn is our retention problem, not onboarding

Onboarding works. Early-stage engagement is up since we rebuilt it. The problem sits later in the lifecycle: customers who get through their first week still leave before renewal, and that number has not moved.

The clearest signal we have is the 30-day mark. Accounts that don't reach activation inside their first 30 days churn at a much higher rate than accounts that do. That makes the first month the highest-leverage window we have, and today we watch it rather than act on it.

## What looks like it's driving churn

Five candidates. We haven't sized any of them, which is the first thing to fix.

- **Configuration.** New users face too many setup options and stall.
- **Time to first value.** We take longer than competitors to show a customer something useful.
- **Support.** Ticket resolution times are getting worse.
- **Discoverability.** Important features sit behind navigation people don't find.
- **Mid-tier pricing.** Some segments don't see what the middle tier buys them over the entry tier.

## What I'm proposing

Three workstreams, run together rather than as separate fixes. Run separately they compete for the same engineering time and none of them finishes.

1. **Instrument the activation path.** Use behavioral data to find the exact steps where users drop off, then intervene at those steps instead of sending generic nudges. This is the prerequisite for the other two.
2. **Move retention ownership beyond Customer Success.** CS can't fix configuration friction or navigation. Product and Support own most of the five causes above, so they should carry retention targets too.
3. **Build churn prediction after the instrumentation lands.** A model that flags at-risk accounts only helps if we already know which behaviors matter and have a play to run when it fires. That's why it's third, not first.

## What I need from this group

Agreement on the sequencing above, and agreement that Product and Support take retention targets alongside CS. Scoped timelines and named owners follow next week.

One caveat worth setting now: this won't move in a quarter. Mid-lifecycle churn is the compound result of decisions made by five different teams, so we should tell the board to expect a few quarters rather than explain a flat first quarter after the fact.
