import csv
import os

print("==Lead Automation System==")

name = input("Enter your name: ")
email = input("Enter your email: ")
phone_number = input("Enter your phone number: ")
service = input("Enter the service you are interested in: ")

info = {
    "name": name,
    "email": email,
    "phone Number": phone_number,
    "service": service,
    "status": "NEW"
}

file_exitsts = os.path.isfile("leads.csv")
with open("leads.csv", "a", newline="") as file:
    fieldnames = ["name", "email", "phone Number", "service", "status"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if not file_exitsts:
        writer.writeheader()

    writer.writerow(info)

print("\nLead created successfully!")
print(info)