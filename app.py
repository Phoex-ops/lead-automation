from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        service = request.form["service"]

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connection = sqlite3.connect("leads.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO leads (
                name,
                email,
                phone,
                service,
                status,
                created_at,
                last_contacted_at,
                follow_up_count,
                appointment_date,
                reminder_sent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                phone,
                service,
                "NEW",
                created_at,
                None,
                0,
                None,
                "NO"
            )
        )

        connection.commit()
        connection.close()

        return "Thank you! Your request has been submitted."

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            lead_id,
            name,
            email,
            phone,
            service,
            status,
            created_at,
            follow_up_count,
            appointment_date,
            reminder_sent
        FROM leads
        ORDER BY lead_id DESC
    """)

    leads = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        leads=leads
    )

@app.route("/update_status/<int:lead_id>", methods=["POST"])
def update_status(lead_id):
    new_status = request.form["status"]

    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    if new_status in ["CONTACTED", "FOLLOW-UP"]:
        cursor.execute(
            """
            UPDATE leads
            SET status = ?, last_contacted_at = ?
            WHERE lead_id = ?
            """,
            (
                new_status,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                lead_id
            )
        )
    else:
        cursor.execute(
            """
            UPDATE leads
            SET status = ?
            WHERE lead_id = ?
            """,
            (
                new_status,
                lead_id
            )
        )

    connection.commit()
    connection.close()

    return redirect("/dashboard")
@app.route("/book_appointment/<int:lead_id>", methods=["POST"])
def book_appointment_web(lead_id):
    appointment_date = request.form["appointment_date"]

    try:
        appointment_datetime = datetime.strptime(
            appointment_date,
            "%Y-%m-%dT%H:%M"
        )
    except ValueError:
        return "Invalid appointment date."

    if appointment_datetime <= datetime.now():
        return "Appointment must be in the future."

    formatted_date = appointment_datetime.strftime(
        "%Y-%m-%d %H:%M"
    )

    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT lead_id
        FROM leads
        WHERE appointment_date = ?
        """,
        (formatted_date,)
    )

    existing_appointment = cursor.fetchone()

    if existing_appointment is not None:
        connection.close()
        return "That appointment time is already booked."

    cursor.execute(
        """
        UPDATE leads
        SET appointment_date = ?,
            status = 'BOOKED',
            reminder_sent = 'NO'
        WHERE lead_id = ?
        """,
        (
            formatted_date,
            lead_id
        )
    )

    connection.commit()
    connection.close()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)