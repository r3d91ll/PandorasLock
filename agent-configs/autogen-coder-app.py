import autogen

# Load configurations for the agents
config_list = autogen.config_list_from_json("/home/todd6585/git/Ops-Tooling/AtlasProject/python3.11.5/autogen-coder-app.py")

# Define the Planning Agent
planner = autogen.AssistantAgent(
    name="planner",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant to accomplish a task. Do not suggest concrete code. For any action beyond writing code or reasoning, convert it to a step that can be implemented by writing code."
)

# Define the User Proxy Agent for the planner
planner_user = autogen.UserProxyAgent(
    name="planner_user",
    max_consecutive_auto_reply=0,
    human_input_mode="NEVER",
)

def ask_planner(message):
    planner_user.initiate_chat(planner, message=message)
    return planner_user.last_message()["content"]

# Define the Assistant Agent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "temperature": 0,
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
    }
)

# Define the User Proxy Agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "planning"},
    function_map={"ask_planner": ask_planner},
)

# Perform a task
user_proxy.initiate_chat(
    assistant,
    message="""Suggest a fix to an open good first issue of flaml""",
)

# Rest of the script handling the interaction and task execution...
