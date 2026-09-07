from langchain_core.tools import tool


@tool
def test_send_follow_up_email(to: str, subject: str, body: str) -> str:
    """Test email tool that does not actually send an email."""

    print("\n[TEST EMAIL]")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")

    return "test-email-reference-123"