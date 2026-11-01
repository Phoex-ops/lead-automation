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
                f"Name: {lead['name']} |"
                f" Email: {lead['email']} |"
                f" Phone: {lead['phone']} |"
                f" Service: {lead['service']} |"
                f" Status: {lead['status']}"
            )

print("==Lead Automation System==")

name = input("Enter your name: ")
email = input("Enter your email: ")
phone = input("Enter your phone number: ")
service = input("Enter the service you are interested in: ")

info = {
    "name": name,
    "email": email,
    "phone": phone,
    "service": service,
    "status": "NEW"
}

file_exists = os.path.isfile("leads.csv")
with open("leads.csv", "a", newline="") as file:
    fieldnames = ["name", "email", "phone", "service", "status"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    writer.writerow(info)

print("\nLead created successfully!")
print(info)
display_leads()