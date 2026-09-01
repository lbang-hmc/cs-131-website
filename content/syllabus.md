# Syllabus

A syllabus describes the why, what, and how of a course, often with lots of policy details. Here is a quick summary first:

> We love studying programming languages and we hope you will, too. We also hope the course helps you think about computer science—and programming—in fundamentally new ways.
>
> We care about your learning and want you to do well. We want you to have everything you need to succeed in the course.
>
> Your ideas, contributions, creativity, and integrity are vital. You can expect to actively engage in the material, to collaborate with one another, and to bring your own interests and experiences to your learning.
>
> We want you to enjoy the class. If some aspect of the class leaves you unhappy or not feeling valued, please talk with us immediately.

The rest of this page contains details. Please skim them now, and return throughout the semester.

---

## Why Study Programming Languages?

What even is "Programming Languages"? This course is all about the ways that the design and implementation of programming languages affect how we compute: What kinds of computation are easy to express, what kinds are difficult or impossible, and why? How does language design influence which problems we can solve, how easily we can solve them, and how good the solutions are?

The field of Programming Languages covers everything from mathematical theory to social science. To give us focus, we have organized CS 131 around three ideas:

- **Functions. Are. Awesome.** We will explore functional programming — building complex programs by defining and composing just functions. No objects, no loops, just functions!
- **Programs = Data.** We can treat a program as data (passing it as input to another program) and data as a program (using a data structure to represent a program's structure). This program/data duality is Computer Science's super-power.
- **Programming Languages are all about people.** They are created by people, for people. What are the impacts of the design decisions made by programming-language creators?

This course will help you:

- Have a fundamentally different view of programming.
- Increase your ability to think abstractly.
- Choose appropriate programming languages based on the problems to be solved and logically justify your choices.
- Become a proficient Haskell programmer.
- Enjoy learning new programming languages as needed, and do so with ease.
- Treat code as data, and solve problems by writing interpreters, code analyzers, and compilers/transpilers.
- Evaluate and critique programming-language design and the way it influences the programs we write.

---

## What You Need for This Course

### Basic Needs

Before you can learn, all your basic human needs must be met. All of these things are more important than whatever is going on in class:

- Health
- Shelter
- Food

If you do not have all of these, or if you are a caretaker for someone who does not, please contact your Academic Dean. If you are a Mudd student, you can email <academicdeans@g.hmc.edu>. Typically, your Dean will contact us to arrange flexibility if necessary. If you feel comfortable, you can also contact us directly — you don't need to share any personal details.

### Your Rights as a Student

Our goal is to create a learning environment that is usable, equitable, inclusive, and welcoming. If facets of the instruction or design of this course result in barriers to inclusion, please let us know as soon as possible. If for any reason you don't feel comfortable talking to us, please feel free to contact the HMC Dean of Faculty, your own Dean of Students, or a faculty member at your home campus.

### Academic Accommodations

You have a right to accommodations for temporary or permanent disabilities. We have done our best to design this course to be accessible (videos will be closed-captioned and downloadable, and flexibility is built into due dates and assessment).

If you have a disability (including mental health and chronic or temporary medical conditions) and may need accommodation to fully participate, please contact your home college's accessibility office:

| College | Contact |
|---------|---------|
| CMC | accessibilityservices@cmc.edu |
| HMC | Amy Bibbens — abibbens@hmc.edu |
| Pitzer | Gabriella Tempestoso — gabriella_tempestoso@pitzer.edu |
| Pomona | disabilityservices@pomona.edu |
| Scripps | ars@scrippscollege.edu |

### Social Engagement

The mission of Harvey Mudd College is to prepare leaders who understand the impact of their work on society. We want to accommodate your reasonable participation in civic engagement events. It works best if you can coordinate with us in advance, ideally at least 24 hours before any affected due dates.

### Title IX

Harvey Mudd College is committed to providing an environment free of all forms of discrimination and sexual harassment, including sexual assault, domestic violence, dating violence, and stalking.

Please be aware that many HMC employees, including all faculty members, are considered Responsible Employees who are required to relay reports of sexual misconduct to the Title IX Coordinator. Although we must report the situation, you will still have options about how your case will be handled.

If you wish to speak to someone confidentially, you can contact:

- EmPOWER Center: 909.607.2689
- Monsour Counseling Center: 909.621.8202
- McAlister Chaplains: 909.621.8685

Additional information is available at <https://www.hmc.edu/tix>.

### Resources and Accounts

- **Computer / Lab Access.** You will use a computer in the McGregor Computer Science Center lab and/or your own computer. If you do not have sufficient access, a limited number of loaner laptops are available — let us know.
- **Internet.** Many materials are online. Most material will be downloadable for offline viewing.
- **Course communication.** All course communication is by email to the instructor at <bang@cs.hmc.edu>. There is no course forum this semester.
- **CS 131 Programming Server.** We recommend using the CS 131 Programming Server for assignments — it contains all necessary libraries, tools, and environments (including Haskell). See the [How-To Guides](how-to/index.md) for how to connect.
- **GitHub.** We use GitHub to distribute starter code — you will `git clone` assignment repositories. Create a free account at [github.com](https://github.com) if you don't already have one. (You do not need to send us your username.)
- **Gradescope.** Assignments, modules, and participation forms are submitted via Gradescope ([gradescope.com](https://www.gradescope.com)). You should have received a notification that you were added; Gradescope is linked to Canvas and uses the same email.
- **Books.** None required. You are free to search for additional Haskell references.

#### Optional Resources

- **Writing Center.** The Writing Center provides feedback on composition projects at any stage. Schedule appointments at <https://www.hmc.edu/writingcenter>.
- **Disability Resources.** Students with disabilities are encouraged to contact the Office of Accessible Education at <access@g.hmc.edu>. Students from other Claremont Colleges should contact their home college's officer.

---

## How This Course Works

We have designed this course as a flipped classroom, aiming to give you as much flexibility as possible while also encouraging community and emphasizing certainty.

- **Flexibility.** Much of the course material is available online to accommodate self-paced learning and unforeseen circumstances. Flexibility is also built into course deadlines.
- **Community.** Building a sense of belonging is essential to a successful learning experience. We provide opportunities during class time to engage with your peers and the instructional team.
- **Certainty.** The course has a highly scaffolded and planned structure that you have full access to via the schedule. There should be no big surprises.

### Course Format

This is a flipped class. You will spend time outside of class on theoretical learning (online content) and time in class on practical learning (working on assignments and problems on your own, with a partner, or in small groups).

### Class Meeting Times

| Section | Days | Time |
|---------|------|------|
| Section 1 | Tuesday & Thursday | 9:35am – 10:50am Pacific |

Class meets in MCSC 203 / 204.

### A Typical Week

Each week follows a pattern:

- **New materials posted** at the start of the week: two numbered submodules (videos, exercises, readings). Work through these at your own pace and submit to Gradescope by the date on the schedule.
- **Required class sessions** are typically used to kick off homework assignments and run labs.
- **Flexible class sessions** — if you have completed all currently assigned work you are not required to attend; otherwise, please spend class time making progress on CS 131.
- **Homework due** — 11:59pm on Mondays. When a Monday is a holiday, that week's homework is due the day before, on Sunday (for example, HW 1 is due Sunday because of Labor Day). Exact dates are on the [schedule](schedule.md).
- **Office hours / grutoring** — scheduled throughout the week; see the [home page](index.md#office-hours-and-grutoring).

### Course Modules

A sequence of online modules forms the backbone of theoretical learning. Each week has two numbered submodules (for example, 2.1 and 2.2), released at the start of the week and due before class on the day shown in the [schedule](schedule.md). The full, current list of modules and topics lives on the schedule.

---

## How to Have a Great CS 131

The short version: actively engage in your learning, collaborate with others, and abide by the Honor Code.

### What We Expect of You

- **Learning.** We expect you to learn lots of things.
- **Advocating for yourself.** Engage actively with materials, think carefully about exercises, and ask lots of questions — during class, at office hours, and by email.
- **Advocating for others.** Attend to the learning of your peers. Be mindful and encouraging rather than discouraging.
- **Professional ethics.** Be accountable to your collaborators and abide by Harvey Mudd's Honor Code.

### What You Can Expect from Us

- **Learning.** You can expect to learn lots of things in this course.
- **A supportive learning environment.** We will encourage academic vulnerability — it's good to say "I don't know," to ask questions, and to take risks.
- **Reasonable flexibility.** Built-in flexibility accommodates accommodations, occasional late assignments, and life events. If the built-in flexibility does not support your learning, come talk to us.
- **Professional ethics.** You can expect confidentiality regarding your grades and learning in the course.

### Getting One-on-One Help

Come to office hours and grutoring hours! We will set regularly scheduled hours, and you are also welcome to set up appointments outside of scheduled times.

### Optional Pair Programming

CS 131 allows optional pair programming on homework assignments after the first warmup assignment. You may decide weekly whether to work with a partner.

If you choose to pair program, you must use full "CS 70 pair-programming methodology": work together as a team, one person at the keyboard and the other watching and making suggestions, switching roles at regular intervals.

All submitted work must be a true joint effort. It is an Honor Code violation to divide the work, to have one person do the work while the other watches passively, or to work separately.

### Collaborating Outside of Pair Programming

You may freely discuss lecture and reading topics with classmates, from informal discussions to organized study groups.

On assignments, you may discuss ideas, general approaches, bugs in the specification, and basic issues like command-line usage or Haskell syntax. You **cannot** share solutions or code — all submitted work must be your own (or constructed equally with your pair-programming partner).

Two useful rules:

- **The "in your head" rule.** When helping each other, leave with understanding, not physical or electronic artifacts. Do not meet as a group and leave with notes; do not help fix a bug without reverting it first.
- **The "understanding, not rote learning" rule.** Do not leave with an answer you don't understand.

### The Honor Code

All students are expected to understand and abide by [Harvey Mudd College's Honor Code](https://www.hmc.edu/ashmc/honor-code/) and the [CS department's interpretation of the Honor Code](https://tinyurl.com/hmc-cs-honorcode).

In particular:

- Do not exchange literal copies of code, program output, or documentation, and do not copy from published or online sources without explicit permission and proper attribution.
- Do not subvert the clear intent of an assignment (e.g., using open-sourced code to bypass the learning goal) without permission.
- Document all sources you consult. Credit any tips from classmates or course staff incorporated into graded work.
- If assigned material is substantially similar to work you have done before, contact your professors before submitting.
- If you see something that seems like it ought to be off-limits (another student's repository, files from a previous semester), immediately contact us rather than looking further.
- If unsure whether something is allowed, document what you did and consult course staff — ideally before taking the questionable action.

### Use of AI / LLM Tools

!!! note "Policy under discussion"
    We will discuss the course policy on AI and large language model tools (ChatGPT, GitHub Copilot, Claude, and similar) during the first class, and the agreed policy will be posted here afterward. Until then, do not use these tools on any CS 131 work.

---

## Coursework and Grading

### Three Kinds of Coursework

| Category | Description |
|----------|-------------|
| **Creating knowledge** | Engaging with course materials and exercises |
| **Applying knowledge** | Working on assignments |
| **Synthesizing knowledge** | Quizzes |

### Grade Breakdown

!!! note "To be announced"
    The full points breakdown and letter-grade cutoffs for this semester are being finalized and will be posted here soon.

### Attendance

Attendance requirements for each day are specified in the [schedule](schedule.md). There are two types of days:

- 🟧 **Together** — Required attendance, with a planned in-class activity (demo, directed lab, or discussion) that benefits from everyone being present. Attending earns course credit, but will not make or break your score.
- 🟪 **Flexible** — If you have completed all currently assigned work, you are not required to attend. Otherwise, please spend class time making progress on CS 131.

### Participation and Feedback

We track attendance through participation and feedback forms. For every class session (including flexible days), there will be a corresponding form on Gradescope. Please complete this form whether or not you attended — even if you don't attend, you can receive partial credit for filling it out.

### Absences

If you need to miss a required class, please let us know via the [excused absence form](https://forms.gle/mcCiQxdoEoYgK3Z58). (No need to fill this out for flexible days.) For complex absences, email the instructor or make an appointment.

### Module Completion

You'll work through online modules outside of class. Each module includes exercises graded on a credit/no-credit basis — you get full points for a good-faith effort. Answers do not need to be correct.

### Lab / Discussion Completion

Some class sessions have required discussions or programming labs with a deliverable submitted to Gradescope. Graded for completion only, not correctness.

### Homework

Week-long homework assignments are due at **11:59pm on Mondays** (or the Sunday before, when that Monday is a holiday — see the [schedule](schedule.md) for exact dates). Each homework also has a short reflection, submitted separately on Gradescope for completion credit.

We generally will not accept homework more than 24 hours late. If you need more time, use the extension process below.

### Programming Assignments

Programming assignments are intended to develop your understanding of the design and implementation of programming languages through hands-on work. You will write and test substantial programs, but your grade will not be based primarily on whether your code passes every test.

For each programming assignment, you will submit your code together with a short Implementation Report. The report will document what you completed, provide evidence from testing or example executions, explain a small but significant piece of your code, describe something you changed or debugged during development, and identify something you understand better as a result of the assignment. You will also briefly disclose any resources or assistance you used.

The test suite tells us how well your program works. The Implementation Report is the primary evidence of how well you understand what you built and the programming-language ideas involved. A partially working implementation accompanied by a precise explanation of what works, what does not, and why can therefore demonstrate substantial learning. Conversely, passing every test is not sufficient if you cannot explain your implementation or the relevant concepts.

Programming assignments will be assessed primarily on the quality and technical accuracy of this evidence, explanation, and understanding, rather than on fine-grained correctness points.

### Quizzes

There will be **four** quizzes this semester, covering a few weeks of material each. Roughly 7 days before each deadline, the quiz will be available to take online in one sitting. You may use notes you have written yourself.

You may retake each quiz **once**. All retakes must be completed during the final week of the semester.

There is **no final exam** — the quizzes and their retakes are the only timed assessments.

### Extensions

- **One-day, no-questions-asked extensions** are available for any homework. Please notify us via the [one-day extension form](https://forms.gle/4NUAH7kHQDivRJSc6). Keeping up with deadlines still gives you the best experience in the course, so use these when you need them, not by default.
- **Longer extensions** require notifying us via the [excused absence / longer extension form](https://forms.gle/mcCiQxdoEoYgK3Z58) and speaking with your instructor and dean.

**Quizzes are the exception.** Quizzes have fixed dates and times and are not eligible for one-day or routine extensions. A quiz deadline moves only for a documented issue, emergency, or intervention by your academic dean.

---

## Fine Print

All policies in this syllabus are subject to change if there is a compelling academic justification. Such changes will be clearly announced by email and posted here.
