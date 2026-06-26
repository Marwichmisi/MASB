---
name: perf-analyze
description: Analyse les performances Android via Perfetto
added: 2026-06-26
type: capability
inputs: trace_file
outputs: test-report.md (performance section)
---

# Perf Analyze

Analyze performance using Perfetto trace files. Load companion skills by invoking the Skill tool directly: load `perfetto-sql` for SQL queries against trace files, `perfetto-trace-analysis` for deeper root-cause analysis.

Focus on: startup latency, UI jank, memory usage, thread contention.

Produce a performance section in `phases/N/test-report.md` with findings, severity, and recommendations.

If no trace file is provided: explain how to capture one (`adb shell perfetto ... -o /data/misc/perfetto-traces/trace.perfetto`), offer to guide the user, or note the gap as `blocked: perf` with an unblock action.
