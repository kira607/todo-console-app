# Tasks

A simple teminal app for managing tasks.

## Features

- [x] Multiple tasks lists.
- [x] Autocreated default list (on first use).
- [ ] Different task statuses (tasks list specific).
- [ ] Tasks grouping.
- [ ] Due dates.
- [ ] Tasks scheduling.
- [ ] Task description (markdown).

## Tasks

- [x] Make basic cli with CRUDable tasks in a pre-made json file as a storage.
- [x] Add a simple TUI.
- [x] Make the app create a file for tasks at startup.
- [x] Add debug module.
- [x] Fix logging leveling: ERROR and CRITICAL are printed all times; WARNING, INFO, DEBUG are printed with each -v option.
- [x] Make logging rich
- [x] Make able to manage multiple tasks files with a separate `lists` module.
- [ ] Tasks list should come in a pretty `rich` table.
- [ ] Emoji or colorful task status.

- [ ] Created at
  - [ ] Add `created_at` attribute to a task.
  - [ ] The attribute is filled when a task is created.
  - [ ] Option to view `created_at` in CLI.
  - [ ] Add visual for `created_at` in TUI.
  - [ ] Tasks are sorted by `created_at` by default.

- [ ] Due date

- [ ] Tasks should have `due_date` attribute.
- [ ] `due_date` in CLI.
  - [ ] Visual representation
- [ ] Editable `due_date` via TUI (including both adding and editing).
- [ ] Different visual of tasks, that are overdue in TUI.

## Development

1. Create venv

```bash
python -m venv .venv
```

2. Source to venv

```bash
source .venv/bin/activate
```

3. Install the module locally with all dependencies

```bash
pip install -e .[all]
```
