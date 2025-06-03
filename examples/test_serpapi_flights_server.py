from openai import OpenAI

# Your server URL (replace with your actual URL)
url = "https://762a-118-168-250-146.ngrok-free.app"

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
    input="幫我找2025/6/29 - 2025/7/3從台北出發到大阪的來回機票，需要最便宜且直飛的。",
)

print(resp.output_text)
