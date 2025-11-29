# Smart Task Analyzer

This project is a minimal Django backend + static frontend to analyze and prioritize tasks.

## Features added in this enhanced package
- Robust scoring algorithm with 3 strategies: balanced, deadline, quickwins.
- Frontend with Bootstrap UI, JSON input, Analyze & Suggest endpoints.
- Edge-case handling for missing fields and bad date formats.
- Example input included in UI.

## How to run locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize Django project (this package contains minimal skeleton files; to fully run, create a proper Django project):
   ```bash
   django-admin startproject backend .
   python manage.py migrate
   python manage.py runserver
   ```

4. Open `frontend/index.html` in your browser for the static UI, or integrate it into Django templates.

## Notes & Next steps
- I included a helper shell script `prepare_git.sh` that initializes a Git repo and makes the first commit.
- If you want, I can convert the frontend into Django templates and produce a runnable `manage.py` and `settings.py` so the whole app runs out-of-the-box.

