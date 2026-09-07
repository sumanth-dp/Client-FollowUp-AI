from backend.app.agents.follow_up_agent import follow_up_agent


result = follow_up_agent.invoke({
    "follow_up_id": 1,
    "client_name": "Rahul",
    "client_email": "kotlasumanth569@gmail.com",
    "purpose": "Follow up on the proposal sent three days ago",
    "notes": "Ask if they had a chance to review it.",
    "action": "",
    "email_subject": "",
    "email_body": "",
    "provider_reference": None,
    "success": False,
    "error": None,
    "messages": [],
})

print(result)