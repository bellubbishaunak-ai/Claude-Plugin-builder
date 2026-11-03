---
name: code-review
description: Review code for correctness bugs, security flaws, and quality issues. Use when the user asks to review, audit, or find problems in code — a file, a folder, or code just written in this session. Reports findings without fixing them.
---

Review the code the user points to and report findings. Do not fix anything unless asked.

**Workflow**
1. Read every relevant file completely — never review from partial excerpts.
2. Trace the logic by hand: inputs → transformations → outputs. Review what the code actually does, not what it claims to do.
3. Use Grep and Glob to find callers, definitions, and all usages of the functions involved — bugs often sit at the boundary, not inside the function.
4. Run the code when possible: existing tests, a quick lint, or a small repro script. Real output beats speculation.

**What to check (in priority order)**
- Correctness: off-by-one errors, wrong operator, unhandled edge case, broken invariant, race condition.
- Security: injection (SQL/command/XSS), path traversal, hardcoded secrets, unsafe deserialization.
- Resource leaks: unclosed files or connections, unbounded memory growth.
- Simplification: dead code, duplicated logic, misleading names, needless abstraction.
- Performance: only when it matters (hot loop, large input).

**Output format**
For each finding:
- `[critical | major | minor] file_path:line_number`
- One-sentence description of the defect.
- Concrete failure scenario: what input or state produces the wrong output.
- Suggested fix in one or two lines.

Order findings by severity, most severe first. If nothing is found, say so plainly — never invent issues to seem thorough.
