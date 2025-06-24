from flask import Flask, render_template, request, redirect, url_for, Response
import os
import csv
import io
from supabase import create_client, Client
from dotenv import load_dotenv
from postgrest.exceptions import APIError

app = Flask(__name__)

load_dotenv(".env")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def append_email(email: str) -> None:
    if not supabase:
        app.logger.error("Supabase client not configured")
        return

    try:
        res = supabase.table("emails") \
                       .insert({"email": email}) \
                       .execute()
        # res.data always exists on success
        app.logger.info(f"Inserted {email!r}, response data={res.data}")
    except APIError as e:
        # catches constraint, RLS, key-errors, etc.
        app.logger.error(f"Supabase insert failed: {e}")
    except Exception as e:
        # anything else unexpected
        app.logger.error(f"Unexpected error on insert: {e}")



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    if email:
        append_email(email)
    return redirect(url_for("thanks"))


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


@app.route("/emails")
def list_emails():
    if not supabase:
        return "Supabase not configured", 500
    res = supabase.table("emails").select("email,created_at").execute()
    emails = res.data or []
    return render_template("emails.html", emails=emails)


@app.route("/download")
def download_emails():
    if not supabase:
        return "Supabase not configured", 500
    res = supabase.table("emails").select("email,created_at").execute()
    rows = res.data or []
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["email", "created_at"])
    for row in rows:
        writer.writerow([row.get("email"), row.get("created_at")])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=emails.csv"},
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
