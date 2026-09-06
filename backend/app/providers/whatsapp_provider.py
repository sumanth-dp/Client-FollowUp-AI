class WhatsAppProvider:

    def send(
        self,
        phone: str,
        message: str,
    ) -> bool:

        print(f"[WHATSAPP] Sending message to {phone}")
        print(f"[WHATSAPP] Message: {message}")

        # Temporary mock implementation.

        return True