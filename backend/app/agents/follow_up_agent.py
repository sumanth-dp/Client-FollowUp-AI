# from typing import TypedDict

# from langgraph.graph import StateGraph, START, END

# from backend.app.core.llm import llm


# class FollowUpState(TypedDict):
#     client_name: str
#     purpose: str
#     notes: str
#     email_subject: str
#     email_body: str


# def generate_email(state: FollowUpState):

#     prompt = f"""
# You are a professional client follow-up assistant.

# Client name: {state["client_name"]}

# Follow-up purpose:
# {state["purpose"]}

# Additional notes:
# {state["notes"]}

# Write a professional and friendly follow-up email.

# Return exactly this format:

# SUBJECT: <email subject>

# BODY:
# <email body>
# """

#     response = llm.invoke(prompt)

#     content = response.content

#     parts = content.split("BODY:", 1)

#     subject_part = parts[0].replace(
#         "SUBJECT:", ""
#     ).strip()

#     body = parts[1].strip()

#     return {
#         "email_subject": subject_part,
#         "email_body": body,
#     }


# graph_builder = StateGraph(FollowUpState)

# graph_builder.add_node(
#     "generate_email",
#     generate_email,
# )

# graph_builder.add_edge(
#     START,
#     "generate_email",
# )

# graph_builder.add_edge(
#     "generate_email",
#     END,
# )

# follow_up_agent = graph_builder.compile()



from typing import TypedDict

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from backend.app.core.llm import llm
from backend.app.tools.gmail_tool import send_follow_up_email


class FollowUpState(TypedDict):
    client_name: str
    client_email: str
    purpose: str
    notes: str
    messages: list


tools = [
    send_follow_up_email,
]

llm_with_tools = llm.bind_tools(tools)


def agent(state: FollowUpState):

    prompt = f"""
You are an AI client follow-up assistant.

Client name: {state["client_name"]}
Client email: {state["client_email"]}

Follow-up purpose:
{state["purpose"]}

Additional notes:
{state["notes"]}

Your task is to:

1. Write a professional and friendly follow-up email.
2. Create a suitable subject.
3. Send the email to the client using the send_follow_up_email tool.

Do not ask the user for permission.
The email should be concise and professional.
"""

    response = llm_with_tools.invoke(
        [HumanMessage(content=prompt)]
    )

    return {
        "messages": [response]
    }


graph_builder = StateGraph(FollowUpState)

graph_builder.add_node(
    "agent",
    agent,
)

graph_builder.add_node(
    "tools",
    ToolNode(tools),
)

graph_builder.add_edge(
    START,
    "agent",
)

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
)

graph_builder.add_edge(
    "tools",
    "agent",
)

graph_builder.add_edge(
    "agent",
    END,
)

follow_up_agent = graph_builder.compile()