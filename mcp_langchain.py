# W4D5_LAB_LAB_Agents_that_speak_MCP_fluently
# Week 4 / Day 5
# Student: Andreas Papachristophorou
# Course: AI Consulting & Integration 2026-07
# Date: 2026-07-31

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent

if sys.platform == "win32":
    # For HTTP transport, the event loop policy is less critical, but you can keep this.
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

LAB_ROOT = Path(__file__).resolve().parent

# === MCP server config: switch to HTTP-based LangChain docs MCP server ===
LANGCHAIN_DOCS_CONNECTION = {
    "langchain-docs": {
        "transport": "streamable_http",
        "url": "https://docs.langchain.com/mcp",
    }
}


def build_mcp_client() -> MultiServerMCPClient:
    # Create the MCP client from the HTTP server connection config.
    return MultiServerMCPClient(LANGCHAIN_DOCS_CONNECTION)


def verify_openai_key() -> str:
    # Load variables from .env before reading the OpenAI key.
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to your .env file or environment."
        )
    return api_key


async def load_mcp_tools(client: MultiServerMCPClient):
    # Stateless call: creates short-lived MCP sessions internally
    tools = await client.get_tools()

    print(f"Loaded {len(tools)} tools from MCP server(s)")
    for tool in tools:
        # Show name and a short preview of description
        print(f" - {tool.name}: {tool.description[:80]}...")

    return tools


def build_docs_agent(model: ChatOpenAI, tools):
    """
    Create an agent that:
    - knows it should use LangChain docs tools,
    - must ground answers in documentation,
    - and can take a single question.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a LangChain + MCP documentation assistant. "
                    "You must use the available tools to look up information "
                    "in the LangChain docs when answering questions. "
                    "Always base your answers on tool outputs, and avoid guessing. "
                    "When possible, explain where in the docs your answer is grounded."
                )
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_openai_tools_agent(
        llm=model,
        tools=tools,
        prompt=prompt,
    )

    return AgentExecutor(agent=agent, tools=tools)

async def main() -> None:
    api_key = verify_openai_key()
    model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
    client = build_mcp_client()

    print("Setup OK: OPENAI_API_KEY loaded and MCP client created.")
    print("Ready for the next lab step: loading tools from the MCP server.")
    print("Loading tools from MCP server...")

    tools = await load_mcp_tools(client)

    print("MCP tools loaded.")
    print("Building LangChain docs agent with MCP tools...")

    docs_agent = build_docs_agent(model, tools)

    # Single lab query for grounding + failure mode analysis
    user_question = (
        "Using the LangChain documentation, explain what MultiServerMCPClient.get_tools() "
        "does and describe one way it can fail or be limited. Cite the relevant docs sections."
    )

    print("Running agent on lab query...")
    result = await docs_agent.ainvoke(
        {
            "input": user_question,
            "chat_history": [],
        }
    )

    print("\n=== Agent answer ===")
    print(result["output"])


if __name__ == "__main__":
    asyncio.run(main())
