# Model Context Protocol (MCP): The STDIO Transport

[The STDIO Transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296291) is the baseline communication mechanism used for Model Context Protocol (MCP) clients and servers running on the same local machine. It relies on standard input (`stdin`) and standard output (`stdout`) streams to seamlessly exchange bidirectional JSON messages.

---

## What is a Transport?

MCP clients and servers communicate by exchanging structured JSON messages. The communication channel that transmits these messages is called a **transport**. While transports can be implemented using various architectures (such as WebSockets or HTTP), the **stdio transport** is the default standard for local development.

---

## How the Stdio Transport Works

When using the stdio transport, the MCP client launches the MCP server as a local subprocess.

* **Client to Server:** The client transmits JSON messages directly into the server's `stdin`.
* **Server to Client:** The server processes the input and writes its responses back to the client's `stdout`.
* **Bidirectional Freedom:** Either party can initiate a message at any time.

> ⚠️ **Note:** The stdio transport only functions when the MCP client and the MCP server are running locally on the exact same machine.

---

## The MCP Connection Sequence (handshake)

Every successful connection over an MCP transport must execute a specific three-message handshake sequence before any other requests (like tool execution or prompt listings) can occur:

1. **Initialize Request:** Sent by the client to kick off the connection.
2. **Initialize Result:** Sent by the server, detailing its specific capabilities.
3. **Initialized Notification:** Sent by the client to confirm receipt. No response is expected from the server after this point.

---

## Communication Patterns

There are four essential communication flows that must be handled over the transport layer:

| Initiator | Direction | Channel Used | Requires Response? |
| --- | --- | --- | --- |
| **Client** | Client $\rightarrow$ Server Request | Server `stdin` | Yes (Server $\rightarrow$ Client Result) |
| **Server** | Server $\rightarrow$ Client Response | Server `stdout` | No (Fulfills initial request) |
| **Server** | Server $\rightarrow$ Client Request | Server `stdout` | Yes (Client $\rightarrow$ Server Result) |
| **Client** | Client $\rightarrow$ Server Response | Server `stdin` | No (Fulfills initial request) |

---

## Why the Stdio Transport Matters

The stdio transport represents the "ideal" implementation of MCP because full, bidirectional communication is entirely unconstrained.

When transitioning to network-based transports (such as HTTP), architecture constraints often prevent the server from freely initiating requests to the client. Understanding how the stdio transport manages bidirectional streams establishes a foundational baseline for navigating the trade-offs of distributed MCP deployments.