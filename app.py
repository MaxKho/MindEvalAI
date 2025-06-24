from flask import Flask, render_template, request, redirect, url_for, Response
import os
import csv
import io
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def append_email(email: str) -> None:
    """Insert a new email into the Supabase table."""
    if not supabase:
        return
    supabase.table("emails").insert({"email": email}).execute()


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
