# CS 131: Programming Languages — Course Website

## Quickstart

```bash
# First time only: create and populate the virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the local dev server (re-run after the first-time setup above)
source .venv/bin/activate
make serve
```

Open <http://127.0.0.1:8000/>. The server reloads automatically when you save a file.

To build the static site (e.g. for deployment):

```bash
make build   # output goes to site/
make clean   # delete the site/ folder
```

---

## Directory structure

```
cs-131-website/
├── mkdocs.yml        # Site configuration: title, theme, nav, extensions
├── requirements.txt  # Python dependencies (mkdocs-material)
├── Makefile          # Shortcuts: make serve / build / clean
├── .venv/            # Local Python virtual environment (not committed)
├── scripts/
│   ├── build_schedule.py # Generates content/schedule.md from schedule.txt
│   └── schedule.txt      # Raw schedule data (source of truth for the generator)
└── content/          # All page content (Markdown) — set as docs_dir in mkdocs.yml
    ├── index.md              # Home page
    ├── syllabus.md           # Syllabus
    ├── schedule.md           # Weekly schedule (generated — see scripts/build_schedule.py)
    ├── modules/
    │   ├── index.md          # Modules overview / table of contents
    │   └── 01-intro.md       # Module 01: Introduction (first content page)
    ├── faq.md                # FAQ
    └── how-to/
        └── index.md          # How-to guides
```

## Adding content

### Add a new module page

1. Create `content/modules/02-foo.md` (copy `01-intro.md` as a template).
2. Add a line to the `Modules:` section of `mkdocs.yml`:
   ```yaml
   - "02: Foo": modules/02-foo.md
   ```

### Add a new how-to guide

1. Create `content/how-to/some-guide.md`.
2. Change the `How-To Guides:` entry in `mkdocs.yml` from a single file to a section:
   ```yaml
   - How-To Guides:
       - how-to/index.md
       - Some Guide: how-to/some-guide.md
   ```

### Admonition boxes

Use these anywhere in Markdown for callout boxes:

```markdown
!!! note "Title"
    Body text.

!!! warning
    Watch out.

!!! tip
    Pro tip.
```

## Configuration

All site-wide settings live in `mkdocs.yml`: site name, author, theme colors, nav structure, and Markdown extensions. The Material theme docs are at <https://squidfunk.github.io/mkdocs-material/>.
