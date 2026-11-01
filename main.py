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
print("\nLead created successfully!")
print(info)