from utils.email_alert import send_email_alert

receiver = input("Enter receiver email: ")

success = send_email_alert(
    receiver,
    "Galle",
    "Gin Ganga",
    "HIGH",
    78.50
)

if success:
    print("EMAIL SENT SUCCESSFULLY")
else:
    print("EMAIL SENDING FAILED")