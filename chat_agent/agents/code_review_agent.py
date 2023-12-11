from chat_agent import ChatAgentConfig
from chat_agent.tools import tool_see_git_diff, tool_commit_all

code_review_agent_config = ChatAgentConfig(
    name="code review bot",
    description="A chat agent that can review code.",
    tools=[
        tool_see_git_diff, tool_commit_all
    ],
)
