from backend.app.agents.follow_up_agent import follow_up_agent


result = follow_up_agent.invoke(
    {
        "client_name": "Rahul",
        "purpose": "Follow up on the proposal sent three days ago",
        "notes": "Ask if they had a chance to review it.",
        "email_subject": "",
        "email_body": "",
    }
)

print("\nSUBJECT:")
print(result["email_subject"])

print("\nBODY:")
print(result["email_body"])