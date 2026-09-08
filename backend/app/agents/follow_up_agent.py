# # from typing import TypedDict

# # from langgraph.graph import StateGraph, START, END

# # from backend.app.core.llm import llm


# # class FollowUpState(TypedDict):
# #     client_name: str
# #     purpose: str
# #     notes: str
# #     email_subject: str
# #     email_body: str


# # def generate_email(state: FollowUpState):

# #     prompt = f"""
# # You are a professional client follow-up assistant.

# # Client name: {state["client_name"]}

# # Follow-up purpose:
# # {state["purpose"]}

# # Additional notes:
# # {state["notes"]}

# # Write a professional and friendly follow-up email.

# # Return exactly this format:

# # SUBJECT: <email subject>

# # BODY:
# # <email body>
# # """

# #     response = llm.invoke(prompt)

# #     content = response.content

# #     parts = content.split("BODY:", 1)

# #     subject_part = parts[0].replace(
# #         "SUBJECT:", ""
# #     ).strip()

# #     body = parts[1].strip()

# #     return {
# #         "email_subject": subject_part,
# #         "email_body": body,
# #     }


# # graph_builder = StateGraph(FollowUpState)

# # graph_builder.add_node(
# #     "generate_email",
# #     generate_email,
# # )

# # graph_builder.add_edge(
# #     START,
# #     "generate_email",
# # )

# # graph_builder.add_edge(
# #     "generate_email",
# #     END,
# # )

# # follow_up_agent = graph_builder.compile()



# from typing import TypedDict

# from langchain_core.messages import HumanMessage
# from langgraph.graph import StateGraph, START, END
# from langgraph.prebuilt import ToolNode, tools_condition

# from backend.app.core.llm import llm
# from backend.app.tools.gmail_tool import send_follow_up_email
# from backend.app.tools.test_email_tool import test_send_follow_up_email

# from typing import Annotated
# from langgraph.graph.message import add_messages

# from typing import Annotated, TypedDict

# from langchain_core.messages import BaseMessage
# from langgraph.graph.message import add_messages


# class FollowUpState(TypedDict):
#     follow_up_id: int
#     client_name: str
#     client_email: str
#     purpose: str
#     notes: str

#     action: str
#     email_subject: str
#     email_body: str

#     provider_reference: str | None
#     success: bool
#     error: str | None

#     messages: Annotated[list[BaseMessage], add_messages]


# tools = [
#     test_send_follow_up_email,
# ]

# llm_with_tools = llm.bind_tools(tools)


# def agent(state: FollowUpState):
#     messages = state["messages"]

#     # First agent pass
#     if not messages:
#         prompt = f"""
# You are an AI client follow-up assistant.

# Client name: {state["client_name"]}
# Client email: {state["client_email"]}

# Follow-up purpose:
# {state["purpose"]}

# Additional notes:
# {state["notes"]}

# Your task is to:

# 1. Write a professional and friendly follow-up email.
# 2. Create a suitable subject.
# 3. Send the email to the client using the test_send_follow_up_email tool.

# Do not ask the user for permission.
# The email should be concise and professional.
# """

#         response = llm_with_tools.invoke(
#             [HumanMessage(content=prompt)]
#         )

#     # Second agent pass after tool execution
#     else:
#         response = llm.invoke(messages)

#     return {
#         "messages": [response]
#     }

# graph_builder = StateGraph(FollowUpState)

# graph_builder.add_node(
#     "agent",
#     agent,
# )

# graph_builder.add_node(
#     "tools",
#     ToolNode(tools),
# )

# graph_builder.add_edge(
#     START,
#     "agent",
# )

# graph_builder.add_conditional_edges(
#     "agent",
#     tools_condition,
# )

# graph_builder.add_edge(
#     "tools",
#     "agent",
# )

# follow_up_agent = graph_builder.compile()



from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from backend.app.core.llm import llm
from backend.app.tools.gmail_tool import send_follow_up_email
from backend.app.schemas.ai_follow_up import FollowUpEmail
class FollowUpState(TypedDict):
    follow_up_id: int
    client_name: str
    client_email: str
    purpose: str
    notes: str

    action: str
    email_subject: str
    email_body: str

    provider_reference: str | None
    success: bool
    error: str | None

    messages: Annotated[list[BaseMessage], add_messages]


# tools = [
#     test_send_follow_up_email,
# ]
tools = [
    send_follow_up_email,
]

llm_with_tools = llm.bind_tools(tools)

email_generator = llm.with_structured_output(FollowUpEmail)
def agent(state: FollowUpState):
    prompt = f"""
You are an AI client follow-up assistant.

Client name: {state["client_name"]}
Client email: {state["client_email"]}

Follow-up purpose:
{state["purpose"]}

Additional notes:
{state["notes"]}

Your task is:

1. Write a professional and friendly follow-up email.
2. Create a suitable subject.
3. Send the email using the send_follow_up_email tool.

Do not ask for permission.
The email should be concise and professional.
"""

    response = llm_with_tools.invoke(
        [HumanMessage(content=prompt)]
    )

    return {
        "messages": [response]
    }

def record_result(state: FollowUpState):
    messages = state["messages"]

    tool_message = next(
        (
            message
            for message in reversed(messages)
            if isinstance(message, ToolMessage)
        ),
        None,
    )

    if tool_message is None:
        return {
            "success": False,
            "provider_reference": None,
            "error": "No tool response found",
        }

    if tool_message.status == "error":
        return {
            "success": False,
            "provider_reference": None,
            "error": str(tool_message.content),
        }

    return {
        "provider_reference": str(tool_message.content),
        "success": True,
        "error": None,
    }





def generate_email(state: FollowUpState):
    prompt = f"""
    You are an AI assistant that writes professional client follow-up emails.

    Client Name:
    {state["client_name"]}

    Follow-up Notes:
    {state["notes"]}

    Purpose:
    {state["purpose"]}

    Generate:
    1. A concise email subject.
    2. A professional email body.

    Do not include placeholders.
    """

    email = email_generator.invoke(prompt)

    return {
        "email_subject": email.subject,
        "email_body": email.body,
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

graph_builder.add_node(
    "record_result",
    record_result,
)

graph_builder.add_node("generate_email", generate_email)







graph_builder.add_edge(START, "generate_email")
graph_builder.add_edge("generate_email", "agent")

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
)

# Tool executes and then graph ends
graph_builder.add_edge(
    "tools",
    "record_result",
)

graph_builder.add_edge(
    "record_result",
    "__end__",
)

# graph_builder.add_edge(START, "generate_email")
# graph_builder.add_edge("generate_email", "agent")
# graph_builder.add_edge("agent", "record_result")
# graph_builder.add_edge("record_result", END)



follow_up_agent = graph_builder.compile()


