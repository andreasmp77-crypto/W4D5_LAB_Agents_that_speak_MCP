from __future__ import annotations

# Standard library imports for async execution, environment access, and paths.
import asyncio
import os
import sys
from pathlib import Path

# Load environment variables from `.env` so the OpenAI key can be read locally.
from dotenv import load_dotenv

# LangChain pieces used to build the agent around MCP tools.
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

# Windows needs a compatible event loop policy for async subprocess work.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Resolve the repository root from this file's location.
LAB_ROOT = Path(__file__).resolve().parent
# Point at the local ETS source folder that the MCP server will expose.
ETS_DOCS_DIR = LAB_ROOT / "lab_docs" / "ets_fueleu"
# Point at the local MCP server script that wraps the ETS folder.
ETS_MCP_SERVER = LAB_ROOT / "ets_fuel_mcp_server.py"

# Exact lab query the agent should answer from local evidence only.
QUERY = (
    "Explain the difference between mandatory and optional ETS voyage fields "
    "and quote the sections that define each"
)


def verify_openai_key() -> str:
    # Load `.env` before looking for the API key in the environment.
    load_dotenv()
    # Read the OpenAI key from the current process environment.
    api_key = os.getenv("OPENAI_API_KEY")
    # Fail fast if the key is missing so the run does not continue half-configured.
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to your .env file or environment."
        )
    # Return the validated key to the caller.
    return api_key


def build_mcp_client() -> MultiServerMCPClient:
    # Verify the source folder exists before trying to start the MCP server.
    if not ETS_DOCS_DIR.is_dir():
        raise RuntimeError(f"Expected ETS source folder at: {ETS_DOCS_DIR}")
    # Verify the local MCP server script exists.
    if not ETS_MCP_SERVER.is_file():
        raise RuntimeError(f"Expected local MCP server at: {ETS_MCP_SERVER}")

    # Configure one local MCP server over stdio so the agent only sees ETS docs.
    return MultiServerMCPClient(
        {
            "ets-fuel": {
                # stdio means LangChain starts the server as a local subprocess.
                "transport": "stdio",
                # Use the current Python interpreter to run the server script.
                "command": sys.executable,
                # Pass the server file as the subprocess argument list.
                "args": [str(ETS_MCP_SERVER)],
            }
        }
    )


async def load_mcp_tools(client: MultiServerMCPClient):
    # Ask the MCP client to expose all tools from the local server.
    tools = await client.get_tools()

    # Print a short inventory so the run shows what the agent can actually use.
    print(f"Loaded {len(tools)} MCP tools from the local ETS server")
    for tool in tools:
        # Show tool names and a brief description preview for traceability.
        print(f" - {tool.name}: {tool.description[:100]}...")

    # Return the LangChain tool objects to build the agent.
    return tools


def build_ets_agent(model: ChatOpenAI, tools):
    # Build the prompt template that frames the agent behavior.
    prompt = ChatPromptTemplate.from_messages(
        [
            # System instructions define the grounding rules and scope.
            SystemMessage(
                content=(
                    "You are an ETS voyage field analyst. "
                    "Use only the local ETS Fuel MCP server connected to the "
                    "lab_docs/ets_fueleu folder. "
                    "Do not use external sources or internet knowledge. "
                    "First search the local ETS documents, then read the relevant "
                    "files, and ground every claim in tool output from the local folder. "
                    "When answering, quote the exact sections that define mandatory "
                    "and optional ETS voyage fields and name the source file(s) used. "
                    "If the evidence is insufficient, say so clearly."
                )
            ),
            # Chat history is kept so the agent interface stays standard.
            MessagesPlaceholder(variable_name="chat_history"),
            # Insert the current user query here.
            ("human", "{input}"),
            # Scratchpad holds intermediate tool calls and reasoning state.
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Create an OpenAI-tools style agent that can call the MCP tools.
    agent = create_openai_tools_agent(
        llm=model,
        tools=tools,
        prompt=prompt,
    )

    # Wrap the agent in an executor so we can invoke it like a runnable.
    # `return_intermediate_steps=True` preserves the tool trace for debugging.
    # `verbose=False` keeps LangChain from printing the long internal chain log.
    return AgentExecutor(
        agent=agent,
        tools=tools,
        return_intermediate_steps=True,
        verbose=False,
    )


async def main() -> dict[str, object]:
    # Verify the API key exists before any model calls are attempted.
    api_key = verify_openai_key()
    # Instantiate the chat model used by the agent.
    model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
    # Build the MCP client pointing at the local ETS server.
    client = build_mcp_client()

    # Show the basic setup state in the terminal.
    print("Setup OK: OPENAI_API_KEY loaded and local ETS MCP client created.")
    print("Local source folder:", ETS_DOCS_DIR)
    print("Loading MCP tools from the local server...")

    # Load the MCP tools, then build the agent around them.
    tools = await load_mcp_tools(client)
    agent = build_ets_agent(model, tools)

    # Print the exact query so the proof is easy to trace.
    print("\n=== Query ===")
    print(QUERY)
    print("\nRunning agent on the ETS query...")

    # Run the agent once on the single lab question.
    result = await agent.ainvoke(
        {
            "input": QUERY,
            "chat_history": [],
        }
    )

    # Return the full result so a wrapper script can print the trace cleanly.
    return result


if __name__ == "__main__":
    # Start the async entrypoint when the script is executed directly.
    asyncio.run(main())
