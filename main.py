import csv
import os
from datetime import datetime

def display_leads():
    if not os.path.isfile("leads.csv"):
        print("No leads found.")
        return

    with open("leads.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for lead in reader:
            print(
                f"Lead ID: {lead['lead_id']} |"
                f"Name: {lead['name']} |"
                f" Email: {lead['email']} |"
                f" Phone: {lead['phone']} |"
                f" Service: {lead['service']} |"
                f" Status: {lead['status']} |"
                f" Created At: {lead['created_at']} |"
                f" Last Contacted At: {lead['last_contacted_at']} |"
                f" Follow-up Count: {lead['follow_up_count']} |"
                f" Appointment Date: {lead['appointment_date']}"
            )

print("==Lead Automation System==")
def add_lead():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    service = input("Enter the service you are interested in: ")
    lead_id = get_next_lead_id()
    created_at = get_current_timestamp()
    last_contacted_at = ""
    follow_up_count = 0
    appointment_date = ""

    info = {
        "lead_id": lead_id,
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "status": "NEW",
        "created_at": created_at,
        "last_contacted_at": last_contacted_at,
        "follow_up_count": follow_up_count,
        "appointment_date": appointment_date
    }

    file_exists = os.path.isfile("leads.csv")
    with open("leads.csv", "a", newline="") as file:
        fieldnames = ["lead_id", "name", "email", "phone", "service", "status", "created_at", "last_contacted_at", "follow_up_count", "appointment_date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(info)

    print("\nLead created successfully!")

def get_next_lead_id():

    if not os.path.isfile("leads.csv"):
        return 1

    with open("leads.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        ids = []
        for lead in reader:
            ids.append(int(lead["lead_id"]))

        if len(ids) == 0:
            return 1

        return max(ids) + 1

def update_lead_status():
    if not os.path.isfile("leads.csv"):
        print("No leads found.")
        return

    lead_id = input("Enter the lead ID you want to update: ")
    valid_statuses = ["NEW", "CONTACTED", "FOLLOW-UP", "BOOKED", "COMPLETED", "LOST"]

    new_status = input(f"Enter the new status (valid options: {', '.join(valid_statuses)}): ").upper()

    if new_status not in valid_statuses:
        print("Invalid status. Please try again.")
        return

    leads = []
    lead_found = False

    with open("leads.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for lead in reader:
            if lead["lead_id"] == lead_id:
                lead["status"] = new_status

                if new_status in ["CONTACTED", "FOLLOW-UP"]:
                    lead["last_contacted_at"] = get_current_timestamp()

                lead_found = True

            leads.append(lead)

    if not lead_found:
        print(f"No lead found with ID {lead_id}.")
        return

    with open("leads.csv", "w", newline="") as file:
        fieldnames = ["lead_id", "name", "email", "phone", "service", "status", "created_at", "last_contacted_at", "follow_up_count", "appointment_date"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(leads)
    # Implementation for updating lead status would go here

def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_followups():

    if not os.path.isfile("leads.csv"):
        print("No leads found.")
        return

    leads = []
    with open("leads.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for lead in reader:

            if lead["status"] in ["CONTACTED", "FOLLOW-UP"]:

                if lead["last_contacted_at"] != "":

                    if has_time_passed(lead["last_contacted_at"], 30):
                        follow_up_count = int(lead["follow_up_count"])

                        if follow_up_count < 3:

                            follow_up_count += 1
                            lead["follow_up_count"] = str(follow_up_count)
                            lead["status"] = "FOLLOW-UP"
                            lead["last_contacted_at"] = get_current_timestamp()

                            if follow_up_count == 1:
                                message = (f"Hi {lead['name']}, this is a follow-up regarding your"
                                           f"{lead['service']} request. :et us know if you'd like"
                                           f" to book an appointment."
                                        )
                                print(message)

                            elif follow_up_count == 2:
                                    message = (
                                        f"Hi {lead['name']}, we wanted to follow up again about "
                                        f"your {lead['service']} request. We're still available "
                                        f"if you'd like to schedule a time."
                                    )
                                    print(message)

                            elif follow_up_count == 3:
                                message = (
                                    f"Hi {lead['name']}, this is our final follow-up regarding "
                                    f"your {lead['service']} request. If you still need help, "
                                    f"feel free to contact us anytime."
                                )
                                print(message)
                        else:
                            print(
                                f"No more follow-ups will be sent to {lead['name']}."
                            )

            leads.append(lead)
    with open("leads.csv", "w", newline="") as file:
        fieldnames = [
            "lead_id",
            "name", 
            "email", 
            "phone", 
            "service", 
            "status", 
            "created_at", 
            "last_contacted_at", 
            "follow_up_count",
            "appointment_date"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(leads)

        print("\n=== Follow-up Leads ===")

        for lead in leads:
            if lead["status"] in ["CONTACTED", "FOLLOW-UP"]:
                print(
                    f"Name: {lead['name']} |"
                    f"Status: {lead['status']} |"
                    f"Follow-up Count: {lead['follow_up_count']} |"
                )
def book_appointment():

    if not os.path.isfile("leads.csv"):
        print("No leads found.")
        return

    lead_id = input("Enter the lead ID you want to book an appointment for: ")

    appointment_date = input("Enter the appointment date (YYYY-MM-DD HH:MM): ")

    leads = []
    lead_found = False

    with open("leads.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for lead in reader:
            if lead["lead_id"] == lead_id:
                lead["appointment_date"] = appointment_date
                lead["status"] = "BOOKED"
                lead_found = True

            leads.append(lead)

    if not lead_found:
        print(f"No lead found with ID {lead_id}.")
        return

    with open("leads.csv", "w", newline="") as file:
        fieldnames = [
            "lead_id",
            "name", 
            "email", 
            "phone", 
            "service", 
            "status", 
            "created_at", 
            "last_contacted_at", 
            "follow_up_count",
            "appointment_date"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(leads)
    print("Appointment booked successfully!")

    print(f"Appointment booked for lead ID {lead_id} on {appointment_date}.")
def has_time_passed(timestamp, seconds):
    time_created = datetime.strptime(
        timestamp, 
        "%Y-%m-%d %H:%M:%S"
        )

    current_time = datetime.now()
    time_difference = current_time - time_created

    return time_difference.total_seconds() >= seconds

while True:
    print("\n1. Add Lead")
    print("2. Display Leads")
    print("3. Exit")
    print("4. Update Lead Status")
    print("5. Check Follow-ups")
    print("6. Book Appointment")

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
    else:
        print("Invalid choice. Please try again.")
