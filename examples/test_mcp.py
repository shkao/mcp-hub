from openai import OpenAI

# Your server URL (replace with your actual URL)
url = "https://fdc6-118-168-250-146.ngrok-free.app"

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "cwa_server",
            "server_url": f"{url}/sse",
            "require_approval": "never",
        },
    ],
    input="明天早上新北市的天氣怎麼樣呢?",
)

print(resp.output_text)
