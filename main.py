
import sqlite3
from datetime import datetime
from email_utils import send_email

def initialize_database():
    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            service TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_contacted_at TEXT,
            follow_up_count INTEGER DEFAULT 0,
            appointment_date TEXT,
            reminder_sent TEXT DEFAULT 'NO'
        )
    """)

    connection.commit()
    connection.close()
def display_leads():
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
            last_contacted_at,
            follow_up_count,
            appointment_date,
            reminder_sent
        FROM leads
    """)

    leads = cursor.fetchall()
    connection.close()

    if not leads:
        print("No leads found.")
        return

    for lead in leads:
        print(
            f"Lead ID: {lead[0]} | "
            f"Name: {lead[1]} | "
            f"Email: {lead[2]} | "
            f"Phone: {lead[3]} | "
            f"Service: {lead[4]} | "
            f"Status: {lead[5]} | "
            f"Created At: {lead[6]} | "
            f"Last Contacted At: {lead[7]} | "
            f"Follow-up Count: {lead[8]} | "
            f"Appointment Date: {lead[9]} | "
            f"Reminder Sent: {lead[10]}"
        )


print("==Lead Automation System==")


def add_lead():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    service = input("Enter the service you are interested in: ")

    created_at = get_current_timestamp()

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

    print("\nLead created successfully!")
def update_lead_status():
    lead_id = input("Enter the lead ID you want to update: ")

    valid_statuses = [
        "NEW",
        "CONTACTED",
        "FOLLOW-UP",
        "BOOKED",
        "COMPLETED",
        "LOST"
    ]

    new_status = input(
        f"Enter the new status "
        f"(valid options: {', '.join(valid_statuses)}): "
    ).upper()

    if new_status not in valid_statuses:
        print("Invalid status. Please try again.")
        return

    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT lead_id FROM leads WHERE lead_id = ?",
        (lead_id,)
    )

    lead = cursor.fetchone()

    if lead is None:
        print(f"No lead found with ID {lead_id}.")
        connection.close()
        return

    if new_status in ["CONTACTED", "FOLLOW-UP"]:
        cursor.execute(
            """
            UPDATE leads
            SET status = ?, last_contacted_at = ?
            WHERE lead_id = ?
            """,
            (
                new_status,
                get_current_timestamp(),
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

    print("Lead status updated successfully!")
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_followups():
    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        lead_id,
        name,
        email,
        service,
        status,
        last_contacted_at,
        follow_up_count
    FROM leads
    WHERE status IN ('CONTACTED', 'FOLLOW-UP')
""")

    leads = cursor.fetchall()

    for lead in leads:
        lead_id = lead[0]
        name = lead[1]
        email = lead[2]
        service = lead[3]
        status = lead[4]
        last_contacted_at = lead[5]
        follow_up_count = lead[6]

        if last_contacted_at is None:
            continue

        if has_time_passed(last_contacted_at, 30):

            if follow_up_count < 3:
                follow_up_count += 1

                if follow_up_count == 1:
                    message = (
                        f"Hi {name}, this is a follow-up regarding your "
                        f"{service} request. Let us know if you'd like "
                        f"to book an appointment."
                    )

                elif follow_up_count == 2:
                    message = (
                        f"Hi {name}, we wanted to follow up again about "
                        f"your {service} request. We're still available "
                        f"if you'd like to schedule a time."
                    )

                else:
                    message = (
                        f"Hi {name}, this is our final follow-up regarding "
                        f"your {service} request. If you still need help, "
                        f"feel free to contact us anytime."
                    )

                print(message)

                try:
                    send_email(
                        email,
                        f"Following up on your {service} request",
                        message
                    )
                    print(f"Follow-up email sent to {name} ({email}).")
                    
                except Exception as error:
                    print(f"Email could not be sent: {error}")
                    continue
                cursor.execute(
                    """
                    UPDATE leads
                    SET
                        follow_up_count = ?,
                        status = 'FOLLOW-UP',
                        last_contacted_at = ?
                    WHERE lead_id = ?
                    """,
                    (
                        follow_up_count,
                        get_current_timestamp(),
                        lead_id
                    )
                )

            else:
                print(
                    f"No more follow-ups will be sent to {name}."
                )

    connection.commit()
    connection.close()
def book_appointment():
    lead_id = input(
        "Enter the lead ID you want to book an appointment for: "
    )

    while True:
        appointment_date = input(
            "Enter the appointment date and time "
            "(YYYY-MM-DD HH:MM): "
        )

        if not validate_appointment_date(appointment_date):
            print(
                "Invalid date. Please enter a future date "
                "in the format YYYY-MM-DD HH:MM."
            )
            continue

        if not is_appointment_available(appointment_date):
            print(
                f"{appointment_date} is already booked. "
                "Please choose another time."
            )
            continue

        break

    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT lead_id
        FROM leads
        WHERE lead_id = ?
        """,
        (lead_id,)
    )

    lead = cursor.fetchone()

    if lead is None:
        print(f"No lead found with ID {lead_id}.")
        connection.close()
        return

    cursor.execute(
        """
        UPDATE leads
        SET
            appointment_date = ?,
            status = 'BOOKED',
            reminder_sent = 'NO'
        WHERE lead_id = ?
        """,
        (
            appointment_date,
            lead_id
        )
    )
    print("Rows updated:", cursor.rowcount)

    connection.commit()
    connection.close()

    print(
        f"Appointment booked for lead ID {lead_id} "
        f"on {appointment_date}."
    )

def validate_appointment_date(date_text):
    try:
        appointment = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        if appointment <= datetime.now():
            return False
        return True
    except ValueError:
        return False
def is_appointment_available(appointment_date):
    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT lead_id
        FROM leads
        WHERE appointment_date = ?
        """,
        (appointment_date,)
    )

    appointment = cursor.fetchone()

    connection.close()

    return appointment is None
def check_appointment_reminders():
    connection = sqlite3.connect("leads.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            lead_id,
            name,
            appointment_date,
            reminder_sent
        FROM leads
        WHERE status = 'BOOKED'
        AND appointment_date IS NOT NULL
        AND reminder_sent = 'NO'
    """)

    leads = cursor.fetchall()

    for lead in leads:
        lead_id = lead[0]
        name = lead[1]
        appointment_date = lead[2]

        appointment_datetime = datetime.strptime(
            appointment_date,
            "%Y-%m-%d %H:%M"
        )

        time_difference = appointment_datetime - datetime.now()

        if 0 < time_difference.total_seconds() <= 120:
            print(
                f"Reminder: {name} has an appointment "
                f"scheduled for {appointment_date}."
            )

            cursor.execute(
                """
                UPDATE leads
                SET reminder_sent = 'YES'
                WHERE lead_id = ?
                """,
                (lead_id,)
            )

    connection.commit()
    connection.close()
def has_time_passed(timestamp, seconds):
    time_created = datetime.strptime(
        timestamp, 
        "%Y-%m-%d %H:%M:%S"
        )

    current_time = datetime.now()
    time_difference = current_time - time_created

    return time_difference.total_seconds() >= seconds

initialize_database()

while True:
    print("\n1. Add Lead")
    print("2. Display Leads")
    print("3. Exit")
    print("4. Update Lead Status")
    print("5. Check Follow-ups")
    print("6. Book Appointment")
    print("7. Check Appointment Reminders")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        add_lead()
    elif choice == "2":
        display_leads()
    elif choice == "3":
        print("Exiting the program.")
        break
    elif choice == "4":
        update_lead_status()
    elif choice == "5":
        check_followups()
    elif choice == "6":
        book_appointment()
    elif choice == "7":
        check_appointment_reminders()
    else:
        print("Invalid choice. Please try again.")
