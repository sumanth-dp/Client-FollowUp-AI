from backend.app.core.llm import llm


response = llm.invoke(
    "Explain in one sentence what an AI agent is."
)

print(response.content)