# AI Tailor Landing Page

This repository contains a simple Flask application that serves a landing page for **AI Tailor**, a free personalized AI service. Visitors can join the waitlist by submitting their email address, which is stored in a local SQLite database.

## Features

- Modern responsive design using Bootstrap
- Sign-up form to collect emails
- Emails stored in `emails.db` using SQLite

## Requirements

- Python 3.9+
- `flask` package

Install dependencies:

```bash
pip install Flask
```

## Running the app

```bash
python app.py
```

The application will run on <http://localhost:5000>. When a user submits their email, it will be saved in the `emails.db` database.
