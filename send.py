import yagmail

def send_email(image_path, recipient_email):
    yagmail.register('evandamron14@gmail.com', 'REDACTED')    # Replace with your email and password
    # Initialize Yagmail client
    yag = yagmail.SMTP('evandamron14@gmail.com')  # Replace with your email

    # Email details
    subject = "Unknown Person Detected"
    body = "An unknown person has been detected, see the attached image."

    # Send the email
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=body,
        attachments=image_path  # Attach the image
    )
    print("Email sent successfully!")

if __name__ == "__main__":
    # Example usage
    send_email("captures/image_20241205_124650.jpg", "evandamron14@gmail.com")
