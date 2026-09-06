## CODE CRAFT

How to write, not just what.

- Before implementing, ask the question that could delete the work. If bending a requirement makes the implementation 10 lines instead of 200, say so and ask — don't build the 200.
- Smallest diff that fully solves it. Every extra moving part is a future bug's home.
- Flat over nested: guard clauses and early returns. Three levels of indentation means restructure, not indent further.
- No speculative abstraction. Don't build for the second caller until the second caller exists. Duplicate once; extract on the third.
- Build what was asked, nothing more. Unrequested options, fallbacks, and "while I'm here" features are scope creep — open a flag instead.
- Match the neighborhood. Reuse the existing util and idiom; introducing a new pattern requires a stated reason.
- Handle errors where something can be done about them. Blanket try/except at every layer hides bugs; let unexpected failures fail loudly.
- When a fix needs a fix, stop — suspect the diagnosis, not the patch.
- State the trade-off you picked. If a simpler approach existed and you rejected it, say why in the PR, not silently.
- Prefer deletable over extensible. Code that's easy to remove beats code that's built to grow.
