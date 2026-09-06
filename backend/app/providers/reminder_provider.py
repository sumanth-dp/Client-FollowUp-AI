class ReminderProvider:

    def remind(
        self,
        message: str,
    ) -> bool:

        print(f"[REMINDER] {message}")

        # Temporary mock implementation.

        return True