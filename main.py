import csv
import os

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
                f" Status: {lead['status']}"
            )

print("==Lead Automation System==")
def add_lead():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    service = input("Enter the service you are interested in: ")
    lead_id = get_next_lead_id()

    info = {
        "lead_id": lead_id,
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "status": "NEW"
    }

    file_exists = os.path.isfile("leads.csv")
    with open("leads.csv", "a", newline="") as file:
        fieldnames = ["lead_id", "name", "email", "phone", "service", "status"]
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

    new_status = input(f"Enter the new status (valid options: {', '.join(valid_statuses)}): ")

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
                lead_found = True

            leads.append(lead)

    if not lead_found:
        print(f"No lead found with ID {lead_id}.")
        return

    with open("leads.csv", "w", newline="") as file:
        fieldnames = ["lead_id", "name", "email", "phone", "service", "status"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(leads)
    # Implementation for updating lead status would go here

while True:
    print("\n1. Add Lead")
    print("2. Display Leads")
    print("3. Exit")
    print("4. Update Lead Status")

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
    else:
        print("Invalid choice. Please try again.")
