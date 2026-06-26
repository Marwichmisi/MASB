---
name: prompt-quality-canon
description: The governing standard for every capability prompt
---

# Outcome-Driven Prompt Quality

Every line you write competes with the version that was never written. State the destination, then make every remaining line survive the tests.

## Write the destination, not the route

A goal-stated prompt holds five things: the **stance** (who the model is), the **outcome** (the artifact that must exist), the **consumer** (who must act on that outcome), the **bar** (what the consumer needs), and the **non-inferables** (persona, wiring, rules with real consequences). The consumer is the highest-leverage line — completeness, rigor, and tone all derive from it.

## The tests

1. **Core test.** Would a capable model do this correctly without being told? If yes, cut.
2. **Truncate before you delete.** Keep the instruction and one clause of why; drop the rest.
3. **Keep the why behind a non-obvious goal.** A goal without its reason cannot apply to the case you did not foresee.
4. **Write what survives as a goal.** State intent and let the model find the path.
5. **Number only true sequences.** Where steps genuinely feed each other, number them.
6. **Carve by relevance, not size.** The entry file is paid on every invocation; a reference is paid only when its branch fires.

## The two-version comparison

Write the smallest version (~5 lines: role, outcome, consumer, scarred rule). Run both. If the small version wins or ties, cut the structure. If it is materially worse, the structure earned its keep.
