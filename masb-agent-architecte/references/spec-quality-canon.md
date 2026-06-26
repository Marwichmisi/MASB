# Spec Quality Canon

## Write the destination, not the route

Every line you write competes with the version of itself that was never written. A spec is not a script — it is a contract. State what must be true when the work is done, then let the implementer find the path.

A good spec holds five things:
- **The outcome** — what artifact or change must exist
- **The consumer** — who must act on this spec without the conversation in the room
- **The bar** — what the consumer needs to be true of the result
- **The context** — what was decided before, why this phase exists
- **The non-inferables** — constraints, rules, and decisions with real consequences

Then stop. The consumer implies the level of detail: if a developer who was never in the room must implement from this spec, chase every ambiguity. If this is a quickplan for an expert, a line per phase is enough.

## The tests

1. **Would a capable implementer do this correctly without being told?** If yes, cut. A section earns its place only by preventing a failure.
2. **Does every requirement have a clear "done" test?** If the implementer cannot tell when the work is complete, the spec is not finished.
3. **Is each section self-contained?** The reader should not need to cross-reference other sections to understand one.
4. **Are scope edges explicit?** What is NOT being done is as important as what is.

## The habit

For each section: What single outcome do you want? What does the implementer already know how to do? What do they genuinely need from you that they cannot infer? Whatever remains is structure you are imposing, and you owe a clear account of what it buys.
