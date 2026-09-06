from backend.app.agents.follow_up_agent import follow_up_agent


result = follow_up_agent.invoke(
    {
        "client_name": "Rahul",
        "client_email": "your-test-email@gmail.com",
        "purpose": "Follow up on the proposal sent three days ago",
        "notes": "Ask whether they reviewed the proposal.",
        "messages": [],
    }
)

print("\nAgent execution completed.")

print("\nMessages:")
for message in result["messages"]:
    print(message)