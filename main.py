from __future__ import annotations

import asyncio
import sys

from mcp_langchain import main as run_agent


def print_intermediate_steps(result: dict[str, object]) -> None:
    # Pull the intermediate steps captured by the agent executor.
    steps = result.get("intermediate_steps", [])

    print("\n=== Tool Trace ===")

    if not steps:
        print("No intermediate steps were returned.")
        return

    for index, step in enumerate(steps, start=1):
        print(f"\nStep {index}")

        # Each step is typically (AgentAction, observation).
        if isinstance(step, tuple) and len(step) == 2:
            action, observation = step
            tool_name = getattr(action, "tool", "<unknown>")
            tool_input = getattr(action, "tool_input", None)
            log_text = getattr(action, "log", "")

            accessed_file = tool_input
            if isinstance(tool_input, dict):
                accessed_file = (
                    tool_input.get("path")
                    or tool_input.get("file")
                    or tool_input.get("document")
                    or tool_input.get("filename")
                    or tool_input.get("query")
                )
            if accessed_file in (None, "", "<unknown>") and isinstance(observation, list) and observation:
                first_item = observation[0]
                if isinstance(first_item, dict):
                    accessed_file = first_item.get("path") or first_item.get("file")

            log_preview = log_text.strip().replace("\n", " ")[:200]

            print(f"Tool: {tool_name}")
            print(f"File: {accessed_file}")
            print(f"Agent log: {log_preview}")
            continue

        # Fall back to a generic representation if the step shape differs.
        print(step)


if __name__ == "__main__":
    print("Starting ETS MCP lab agent...")
    try:
        result = asyncio.run(run_agent())
        print_intermediate_steps(result)
        print("\n=== Final Answer ===")
        print(result.get("output", ""))
    except Exception as exc:
        print(f"Run failed: {exc}")
        sys.exit(1)
    print("Run completed successfully.")
