# Example `sqlmigrate` problem

This repo demonstrates a problem with Django's `sqlmigrate` command when
changing `UNIQUE` indexes with multiple fields.

## Setup

Clone this repo and install Django:

```console
python -m pip install -r requirements.txt
```

## Demonstration

We can apply the first migration (to set up the database) and happily show the
SQL for the third migration:

```console
$ python -m manage migrate core 0001
Operations to perform:
  Target specific migration: 0001_initial, from core
Running migrations:
  Applying core.0001_initial... OK

$ python -m manage sqlmigrate core 0003
BEGIN;
--
-- Alter unique_together for testmodel (1 constraint(s))
--
DROP INDEX "core_testmodel_name_age_530d7841_uniq";
CREATE UNIQUE INDEX "core_testmodel_name_colour_5002f5dd_uniq" ON "core_testmodel" ("name", "colour");
COMMIT;
```

However, after applying the third migration, it can no longer be shown as SQL:

```console
$ python -m manage migrate core 0003
Operations to perform:
  Target specific migration: 0003_alter_testmodel_unique_together, from core
Running migrations:
  Applying core.0002_testmodel_colour... OK
  Applying core.0003_alter_testmodel_unique_together... OK

$ python -m manage sqlmigrate core 0003
Traceback (most recent call last):
  File "/usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/lib/python3.8/runpy.py", line 194, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/lib/python3.8/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/private/tmp/sqlmigrate-failures/testproject/manage.py", line 22, in <module>
    main()
  File "/private/tmp/sqlmigrate-failures/testproject/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/core/management/__init__.py", line 425, in execute_from_command_line
    utility.execute()
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/core/management/__init__.py", line 419, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/core/management/base.py", line 373, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/core/management/commands/sqlmigrate.py", line 29, in execute
    return super().execute(*args, **options)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/core/management/base.py", line 417, in execute
    output = self.handle(*args, **options)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/core/management/commands/sqlmigrate.py", line 65, in handle
    sql_statements = loader.collect_sql(plan)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/db/migrations/loader.py", line 352, in collect_sql
    state = migration.apply(state, schema_editor, collect_sql=True)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/db/migrations/migration.py", line 125, in apply
    operation.database_forwards(self.app_label, schema_editor, old_state, project_state)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/db/migrations/operations/models.py", line 505, in database_forwards
    alter_together(
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/db/backends/base/schema.py", line 425, in alter_unique_together
    self._delete_composed_index(model, fields, {'unique': True}, self.sql_delete_unique)
  File "/private/tmp/sqlmigrate-failures/venv/lib/python3.8/site-packages/django/db/backends/base/schema.py", line 461, in _delete_composed_index
    raise ValueError("Found wrong number (%s) of constraints for %s(%s)" % (
ValueError: Found wrong number (0) of constraints for core_testmodel(name, age)
```