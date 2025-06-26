# MindEval.ai Landing Page

This repository contains a simple Flask application that serves a landing page for **MindEval.ai**, an AI-driven chess coach offering natural-language analysis of positions, moves, and games along with move-based Elo estimates. Visitors can join the waitlist by submitting their email address, which is stored in a Supabase table.

## Built Using
- Flask (for the landing page)
- Supabase Database (to save emails)
- Render (to host the website)

## Features

- Modern responsive design using Bootstrap
- Sign-up form to collect emails
- Emails stored in Supabase
- Admin routes to view and download collected addresses

## Requirements

- Python 3.9+
- `flask` package
- `supabase` package

Install dependencies:

```bash
pip install Flask supabase
```

## Configuration

Set the following environment variables with your Supabase credentials before running the app:

- `SUPABASE_URL` – your project URL
- `SUPABASE_KEY` – service role or anon key with insert/select permissions

## Running the app

```bash
python app.py
```

The application will run on <http://localhost:5000>. Submitted emails are saved to your Supabase project and can be viewed at `/emails` or downloaded from `/download`.
