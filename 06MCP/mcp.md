# Model Context Protocol 
(MCP) is a communication layer that provides Claude with context and tools without requiring you to write a bunch of tedious integration code. Think of it as a way to shift the burden of tool definitions and execution away from your server to specialized MCP servers.

![mcp](mcp.jpg)

![mcpflow](mcpflow.jpg)

The MCP client consists of two main components:

* MCP Client - A custom class we create to make using the session easier
* Client Session - The actual connection to the server (part of the MCP Python SDK)