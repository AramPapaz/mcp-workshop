# ECCB MCP Workshop: Setup and Run

## 1. Initial setup

1. Open the project repository on GitHub.
2. Select **Code**, then **Codespaces**, then **Create codespace**.
3. Wait for the environment to finish building (you should see this README file in the main window).

## 2. Start the MCP server

Once setup is complete, start the MCP server:

```bash
./server.py >& server.log
```

## Workshop examples

`server.py` provides two STRING-based tools: one searches a local term file,
and the other retrieves Gene Ontology Biological Process annotations for a
protein.

The server output is written to `server.log`. It includes messages similar to:

```text
INFO:     Started server process [2464]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## 3. Make the port public

Once the environment is running:

- Open the **Ports** tab.
- Find port `8000`.
- Right-click the port, then select **Port Visibility** → **Public**.
- Right-click the port again, then select **Copy Local Address**. You will
  need it in the next step.

## 4. Configure the chat client

Click `chat.conf` in the left-hand file explorer and replace both placeholder values.
For `MCP_SERVER_URL`, paste the local address you copied in the previous step
and add `/mcp`:

```text
OPENAI_API_KEY="your-api-key-here"
MCP_SERVER_URL="<your-copied-local-address>/mcp"
```

Do not commit a real API key. Then return to this README.

## 5. Open a new terminal

Open the **Terminal** tab and click **+** to start a fresh terminal.

## 6. Open the server log

Click `server.log` in the left-hand file explorer and keep it open on the right. It shows errors and debug information from your MCP server.

## 7. Start the chat client and begin chatting

```bash
./chat.py
```

The client reads the server URL from `chat.conf`. You can now start interacting with the MCP server through the chat interface.

Example prompts:

- `Search the human Biological Process terms for cell cycle.`
- `What Gene Ontology Biological Process annotations does human CDK1 have?`

## Troubleshooting

- Ensure the server is fully running before starting `chat.py`.
- Ensure both values in `chat.conf` have been replaced before starting the chat client.
- If the endpoint fails, double-check the `/mcp` suffix.
