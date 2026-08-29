#!/usr/bin/env python3
"""Generate docs/schedule.md from the raw schedule.txt data (this script's
sibling, scripts/schedule.txt). Encodes the spreadsheet rows as structured
data, then renders a week-by-week set of small tables with links to
existing module/lab/HW pages (and plain text where no page exists yet).

To regenerate the live page after editing `rows` below (new week, moved
date, or a newly-built module/lab/HW that should now get linked — add
it to the relevant *_LINKS dict), run from the repo root:

    python3 scripts/build_schedule.py > docs/schedule.md

See MEMORY.md's "Schedule page" entry for the data decisions baked into
`rows` (resolved ambiguities, dropped columns, etc.) before changing it.
"""

import datetime

MODULE_LINKS = {
    "1.1 Intro / what is CS131?": "modules/01.1-welcome-to-programming-languages.md",
    "2.1 Intro to Haskell": "modules/02.1-introduction-to-haskell-and-functional-programming.md",
    "2.2 Functional Programming and HOF": "modules/02.2-functions-as-values.md",
    "3.1 FP, HOF, Lists": "modules/03.1-lists-tuples-pattern-matching-and-parameterized-types.md",
    "3.2 Data Types": "modules/03.2-haskell-data-types-pattern-matching-and-type-classes.md",
    "4.1 Syntax / Semantics": "modules/04.1-code-as-data-evaluating-expressions.md",
    "4.2 Eval / Interpretation": "modules/04.2-representing-functions.md",
}

LAB_LINKS = {
    "Lab 02: Haskell and ghci": "labs/lab02.md",
    "Lab 03: FP": "labs/lab03.md",
    "Lab 04: Eval ASTs": "labs/lab04.md",
}

HW_LINKS = {
    "HW 01 peoPLe": ("HW 01: peoPLe", "assignments/hw01.md"),
    "HW 02 FUNctional Programming": ("HW 02: FUNctional Programming", "assignments/hw02.md"),
    "HW 03 Lists, Data Types, Stack Machines": ("HW 03: Lists, Data Types, Stack Machines", "assignments/hw03.md"),
    "HW 04 Little Languages (RegEx, Art)": ("HW 04: Little Languages (RegEx, Art)", "assignments/hw04.md"),
}

HW_DUE_LINKS = {
    "HW 01: peoPLe": ("HW 01: peoPLe", "assignments/hw01.md"),
    "HW 02: FUNctional Programming": ("HW 02: FUNctional Programming", "assignments/hw02.md"),
    "HW 03 Lists, Data Types, Stack Machines": ("HW 03: Lists, Data Types, Stack Machines", "assignments/hw03.md"),
    "HW 04 Little Languages (RegEx, Art)": ("HW 04: Little Languages (RegEx, Art)", "assignments/hw04.md"),
}

BADGE = {"Together": "🟧", "Flexible": "🟪"}

# Each row: week, date(YYYY-MM-DD) or None, kind, ...fields
# kind: "class", "due", "holiday"
rows = [
 (1, "2026-09-01", "class", "Class 1", "Together", "Intro", None, None, "HW 01 peoPLe"),
 (1, "2026-09-03", "class", "Class 2", "Together", "Haskell Live Interactive Demo", "1.1 Intro / what is CS131?", "Lab 01: logging into server, getting starter HW files, editing files, submitting files, workflows", None),
 (1, "2026-09-06", "due", None, None, None, None, None, "HW 01: peoPLe"),
 (2, "2026-09-07", "holiday", "Labor Day", None, None, None, None, None),
 (2, "2026-09-08", "class", "Class 3", "Together", "Haskell and Functional Programming", "2.1 Intro to Haskell", "Lab 02: Haskell and ghci", "HW 02 FUNctional Programming"),
 (2, "2026-09-10", "class", "Class 4", "Flexible", "Haskell and Functional Programming", "2.2 Functional Programming and HOF", None, None),
 (3, "2026-09-14", "due", None, None, None, None, None, "HW 02: FUNctional Programming"),
 (3, "2026-09-15", "class", "Class 5", "Together", "Lists & Pattern Matching", "3.1 FP, HOF, Lists", "Lab 03: FP", "HW 03 Lists, Data Types, Stack Machines"),
 (3, "2026-09-17", "class", "Class 6", "Together", "Data Types & Pattern Matching", "3.2 Data Types", "Quiz 1", None),
 (4, "2026-09-21", "due", None, None, None, None, None, "HW 03 Lists, Data Types, Stack Machines"),
 (4, "2026-09-22", "class", "Class 7", "Together", "Syntax / Semantics", "4.1 Syntax / Semantics", "Lab 04: Eval ASTs", "HW 04 Little Languages (RegEx, Art)"),
 (4, "2026-09-24", "class", "Class 8", "Flexible", "Eval", "4.2 Eval / Interpretation", None, None),
 (5, "2026-09-28", "due", None, None, None, None, None, "HW 04 Little Languages (RegEx, Art)"),
 (5, "2026-09-29", "class", "Class 9", "Together", "Eval / Compiling", "5.1 Scope", "Lab 05: PicPlot", "HW 05 Simple PicPlot Compiling"),
 (5, "2026-10-01", "class", "Class 10", "Flexible", "Eval / Closures", "5.2 Environments? Closures?", None, None),
 (6, "2026-10-05", "due", None, None, None, None, None, "HW 05 Simple PicPlot Part 1: Compiling"),
 (6, "2026-10-06", "class", "Class 11", "Together", "Parsing", "6.1 Parsing", "Lab 06: Parsing", "HW 06 PicPlot Parsing"),
 (6, "2026-10-08", "class", "Class 12", "Flexible", "Parsing", "6.2 Parser Combinators", None, None),
 (7, "2026-10-12", "due", None, None, None, None, None, "HW 06 PicPlot Part 2: Parsing"),
 (7, "2026-10-13", "class", "Class 13", "Together", "Functors / Monads", "7.1 Functors", "Lab 07: Monads", "HW 07 Monadic Eval"),
 (7, "2026-10-15", "class", "Class 14", "Together", "Functors / Monads", "7.2 Monads", "Quiz 2", None),
 (8, "2026-10-20", "holiday", "Fall Break", None, None, None, None, None),
 (8, "2026-10-22", "class", "Class 15", None, "Lambda Calc", "8.1 Lambda Calc", None, None),
 (9, "2026-10-26", "due", None, None, None, None, None, "HW 07 Monadic Eval"),
 (9, "2026-10-27", "class", "Class 16", "Together", "Lambda Calc", "9.1 Lambda Calc", "Lab 08: LC", "HW 08 Lambda Calc"),
 (9, "2026-10-29", "class", "Class 17", "Flexible", "Lambda Calc", "9.2 Lambda Calc", None, None),
 (10, "2026-11-02", "due", None, None, None, None, None, "HW 08 Lambda Calc"),
 (10, "2026-11-03", "class", "Class 18", "Together", "Lambda Calc → Raskell", "10.1 LC → Raskell", "Lab 09: S-Exps (Raskell)", "HW 09 Raskell Eval"),
 (10, "2026-11-05", "class", "Class 19", "Flexible", "Lambda Calc → Raskell", "10.2 LC → Raskell", None, None),
 (11, "2026-11-09", "due", None, None, None, None, None, "HW 09 Raskell Eval"),
 (11, "2026-11-10", "class", "Class 20", "Together", None, None, "Lab 10: Parsing S-Exps", "HW 10 Raskell Parser"),
 (11, "2026-11-12", "class", "Class 21", "Flexible", "Types", "11.1 Types", None, None),
 (12, "2026-11-16", "due", None, None, None, None, None, "HW 10 Raskell Parser"),
 (12, "2026-11-17", "class", "Class 22", "Together", "Types", "12.1 Types", "Lab 11: Types", "HW 11: Types"),
 (12, "2026-11-19", "class", "Class 23", "Together", "Types", "12.2 Types", "Quiz 3", None),
 (13, "2026-11-23", "due", None, None, None, None, None, "HW 11: Types"),
 (13, "2026-11-24", "holiday", "Thanksgiving Break", None, None, None, None, None),
 (13, "2026-11-26", "holiday", "Thanksgiving Break", None, None, None, None, None),
 (14, "2026-12-01", "class", "Class 24", "Together", "peoPLe", "14.1 peoPLe", "Lab 12: peoPLe", "HW 12: peoPLe"),
 (14, "2026-12-03", "class", "Class 25", "Together", "peoPLe", None, "peoPLe Workshop", None),
 (15, "2026-12-07", "due", None, None, None, None, None, "HW 12: peoPLe"),
 (15, "2026-12-08", "class", "Class 26", None, None, None, None, None),
 (15, "2026-12-10", "class", "Class 27", None, None, None, "Quiz 4", None),
]

def fmt_date(d):
    dt = datetime.date.fromisoformat(d)
    return dt.strftime("%a %b ") + str(dt.day)

def week_header(week_rows):
    dates = [datetime.date.fromisoformat(r[1]) for r in week_rows]
    lo, hi = min(dates), max(dates)
    if lo.month == hi.month:
        return f"{lo.strftime('%B')} {lo.day}–{hi.day}"
    return f"{lo.strftime('%b')} {lo.day} – {hi.strftime('%b')} {hi.day}"

def module_cell(m):
    if not m:
        return ""
    if m in MODULE_LINKS:
        return f"[{m}]({MODULE_LINKS[m]})"
    return m

def activity_cell(a):
    if not a:
        return ""
    if a in LAB_LINKS:
        return f"[{a}]({LAB_LINKS[a]})"
    if a.startswith("Quiz"):
        return f"\U0001F4DD **{a}**"
    return a

def class_cell(topic, modality):
    badge = BADGE.get(modality, "")
    label = f"{badge} *{modality}*".strip() if modality else ""
    if label and topic:
        return f"{label} — {topic}"
    return label or topic or ""

def hw_release_cell(hw):
    if not hw:
        return ""
    if hw in HW_LINKS:
        label, link = HW_LINKS[hw]
        return f"Released: [{label}]({link})"
    return f"Released: {hw}"

def hw_due_cell(hw):
    if not hw:
        return ""
    if hw in HW_DUE_LINKS:
        label, link = HW_DUE_LINKS[hw]
        return f"**Due:** [{label}]({link}) · 11:59pm"
    return f"**Due:** {hw} · 11:59pm"

def render_week(week_num, week_rows):
    out = []
    out.append(f"## Week {week_num} — {week_header(week_rows)}\n")
    out.append("| Date | Class | Module (due 9:30am) | Lab / Activity | Homework |")
    out.append("|---|---|---|---|---|")
    for r in week_rows:
        (_, date, kind, event, modality, topic, module, activity, hw) = r
        date_s = fmt_date(date)
        if kind == "holiday":
            out.append(f"| {date_s} | \U0001F389 *{event} — no class* | | | |")
        elif kind == "due":
            out.append(f"| {date_s} | | | | {hw_due_cell(hw)} |")
        else:  # class
            cls = class_cell(topic, modality)
            hw_cell = hw_release_cell(hw)
            label = f"**{event}** — {cls}" if cls else f"**{event}**"
            out.append(f"| {date_s} | {label} | {module_cell(module)} | {activity_cell(activity)} | {hw_cell} |")
    out.append("")
    return "\n".join(out)

HEADER = """# Schedule

Fall 2026. Every row below is a real calendar date — click through to a module, lab, or homework page wherever one is linked; unlinked items aren't posted yet.

**How to read the "Class" column:**

- 🟧 **Together** — required attendance, with an in-class activity (demo, lab, or discussion) planned.
- 🟪 **Flexible** — if you're caught up on assigned work, you don't need to attend; otherwise, use the time to work on CS 131 with staff around to help.

See the syllabus's [Attendance](syllabus.md#attendance) section for the full policy. A few classes late in the semester (Oct 22, Dec 8, Dec 10) don't have a type assigned yet in the source schedule — they'll get a badge once that's decided.

**Module completions are due by 9:30am on the day listed in the "Module" column** — before class starts. Each week's table also carries any homework released or due that week, and marks holidays where there's no class.
"""

def main():
    weeks = {}
    for r in rows:
        weeks.setdefault(r[0], []).append(r)

    body = [HEADER]
    for wn in sorted(weeks):
        body.append(render_week(wn, weeks[wn]))

    print("\n".join(body))

if __name__ == "__main__":
    main()
