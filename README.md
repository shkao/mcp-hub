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

### Running a Server

To run a server, follow these steps:

1. Navigate to the `servers` directory:

   ```bash
   cd servers
   ```

2. Execute the desired server script. For example, to start the CWA weather server, run:

   ```bash
   python cwa_server.py
   ```

3. By default, the server will start on port 8000 and use Server-Sent Events (SSE) for communication.

4. To expose your local server to the internet, run the following command in a separate terminal:

   ```bash
   grok http 8000
   ```

### Running an Example Client

To test the server using an example client script, follow these steps:

1. Navigate to the `examples` directory:

   ```bash
   cd examples
   ```

2. Run the example script to interact with the server using the OpenAI Python client:

   ```bash
   python test_mcp.py
   ```

3. Before running the script, ensure you edit it to point to your server's URL and adjust any necessary parameters.

## Adding New Servers

To add a new MCP server, follow these steps:

1. Create a new Python script in the `servers/` directory.
2. Initialize a `FastMCP` instance and define tools using the `@mcp.tool()` decorator.
3. Add a `__main__` block to run the server, specifying transport and port.
