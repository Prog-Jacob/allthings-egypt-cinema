import asyncio
import aiohttp
from rich import print
from rich.rule import Rule
from rich.panel import Panel
from rich.console import Group
from rich.markdown import Markdown

# This script is under development.
# An LLM server must be up locally to run this script.
# I use LM Studio for this purpose, with qwen2.5.1-coder-7b-instruct model.


LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"


async def ask(session, system_message, user_message):
    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {"role": "user", "content": user_message},
    ]
    payload = {
        "model": "qwen2.5.1-coder-7b-instruct",
        "messages": messages,
        "temperature": 0.7,
        "stream": False,
    }

    async with session.post(LLM_URL, json=payload) as response:
        result = await response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")


async def ask_many(system_message, user_messages):
    async with aiohttp.ClientSession() as session:
        tasks = [
            ask(session, system_message, user_message) for user_message in user_messages
        ]
        responses = await asyncio.gather(*tasks)
        return responses


def _print(system_message, user_messages, responses):
    messages = []
    messages.append(
        Group(
            "[bold magenta]System Message>[/bold magenta] ",
            Markdown(system_message),
        )
    )

    for user_message, response in zip(user_messages, responses):
        message = Group(
            "[bold green]User Message>[/bold green] ", Markdown(user_message)
        )
        response = Group("[bold blue]LLM Response>[/bold blue] ", Markdown(response))
        messages.append(Group(Rule(), message, response, Rule()))

    messages.append("[bold red]End of Conversation[/bold red]")
    terminal = Panel(
        Group(*messages),
        title="[bold cyan]Local LLM Terminal[/bold cyan]",
        expand=False,
    )
    print(terminal)


def main(args):
    user_messages = args["user_messages"]
    system_message = args["system_message"]
    responses = asyncio.run(ask_many(system_message, user_messages))
    _print(system_message, user_messages, responses)
