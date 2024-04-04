run this to activate the variables

$env:READ_DOT_ENV_FILE = "True"

RUN this command to collect the static files and directories
python manage.py collectstatic

in the installed apps i set "whitenoise.runserver_nostatic",
to disable the static files and directories If you wan't to disable it, just relove it in your settings apps

---

---
