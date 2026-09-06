# class EmailProvider:

#     def send(
#         self,
#         to: str,
#         subject: str,
#         message: str,
#     ) -> bool:

#         print(f"[EMAIL] Sending email to {to}")
#         print(f"[EMAIL] Subject: {subject}")
#         print(f"[EMAIL] Message: {message}")

#         # Temporary mock implementation.
#         # Later this will connect to a real email service.

#         return True


from backend.app.tools.gmail_tool import send_email


class EmailProvider:

    def send(
        self,
        to: str,
        subject: str,
        message: str,
    ) -> bool:

        print(f"[EMAIL] Sending email to {to}")
        print(f"[EMAIL] Subject: {subject}")
        print(f"[EMAIL] Message: {message}")

        try:
            result = send_email(
                to=to,
                subject=subject,
                body=message,
            )

            print(
                f"[EMAIL] Gmail API sent message: "
                f"{result.get('id')}"
            )

            return result.get("id")

        except Exception as e:
            print(
                f"[EMAIL] Gmail API error: {e}"
            )
            return None