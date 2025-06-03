from openai import OpenAI

# Your server URL (replace with your actual URL)
url = "http://localhost:8002"

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "dice_server",
            "server_url": f"{url}/sse",
            "require_approval": "never",
        },
    ],
    input="請幫我擲 5 顆骰子，並回傳結果。",
)

print(resp.output_text)