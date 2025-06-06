from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Your server URL (replace with your actual URL)
url = "https://1b38-220-135-69-190.ngrok-free.app"

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "serpapi_flights_server",
            "server_url": f"{url}/sse",
            "require_approval": "never",
        },
    ],
    input="請幫我搜尋 2025/6/28 - 2025/7/3 之間，從台北到大阪最便宜的來回機票",
)

console = Console()
markdown_output = Markdown(resp.output_text)
console.print(markdown_output)
