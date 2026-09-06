from backend.app.tools.gmail_tool import send_email


send_email(
    to="kotlasumanth569@gmail.com",
    subject="Client Follow-Up AI Test",
    body="This is a test email from the Client Follow-Up AI Gmail tool.",
)

print("Email sent successfully")