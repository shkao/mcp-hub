# MCP Hub

A collection of Model Context Protocol (MCP) servers

## Structure

- servers/: Contains MCP server scripts.
- examples/: Example client scripts for interacting with the servers.
- requirements.txt: Project dependencies.
- .gitignore: Git ignore rules.

## Requirements

- Python 3.7+
- pip

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Environment Variables

Before running the servers, set the required API keys and optional ports:

```bash
export CWA_API_KEY=YOUR_CWA_API_KEY_HERE
export SERPAPI_API_KEY=YOUR_SERPAPI_API_KEY_HERE
# Optional: override default ports (defaults: 8000, 8001, 8002)
export CWA_SERVER_PORT=8000
export FLIGHTS_SERVER_PORT=8001
export DICE_SERVER_PORT=8002
```

You can also create a `.env` file from `.env.example` and source it:

```bash
cp .env.example .env
source .env
```

### Running Servers

From the project root, start the desired server:

```bash
# CWA weather server
python servers/cwa_server.py

# SerpAPI flight search server
python servers/serpapi_flights_server.py

# Dice roller server
python servers/dice_server.py
```

By default, each server will start on its configured port and use Server-Sent Events (SSE) for communication.

To expose your local server to the internet (e.g., via ngrok), run:

```bash
ngrok http <port>
```

### Running Example Clients

Example client scripts are in the `examples/` directory. Update the `url` variable at the top of each script to point to your server's URL, then run:

```bash
cd examples

python test_cwa_server.py
python test_serpapi_flights_server.py
python test_dice_server.py
```

## Adding New Servers

To add a new MCP server, follow these steps:

1. Create a new Python script in the `servers/` directory.
2. Initialize a `FastMCP` instance and define tools using the `@mcp.tool()` decorator.
3. Add a `__main__` block to run the server, specifying transport and port.
