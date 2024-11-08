import smtplib 
from email.message import EmailMessage
import ssl

def send_email(image_path, recipient_email):
    sender_email = "fasteenchet23@gmail.com"
    sendgrid_password = "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"
    subject = "Person Detected"
    body = "A person has been detected, see the attached image."

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(body)

    with open(image_path, 'rb') as img:
        msg.add_attachment(img.read(), maintype='image', subtype='jpeg', filename='person.jpg')

    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.sendgrid.net', 587) as server:
        server.starttls(context=context)
        server.login("apikey", sendgrid_password)
        server.send_message(msg)

# Example usage
# detect_and_notify("recipient_email@example.com")
image_path = "IMG_3782.jpg"
send_email(image_path, "rcgoodman18@gmail.com")