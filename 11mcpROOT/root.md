# roots

Roots are a way to grant MCP servers access to specific files and folders on your local machine. Think of them as a permission system that says "Hey, MCP server, you can access these files" - but they do much more than just grant permission.

## Roots in Action
Here's how the workflow changes with roots:

* User asks to convert a video file
* Claude calls list_roots to see what directories it can access
* Claude calls read_dir on accessible directories to find the file
* Once found, Claude calls the conversion tool with the full path

This happens automatically - users can still just say "convert biking.mp4" without providing full paths.

## Security and Boundaries
Roots also provide security by limiting access. If you only grant access to your Desktop folder, the MCP server cannot access files in other locations like Documents or Downloads.

When Claude tries to access a file outside the approved roots, it gets an error and can inform the user that the file isn't accessible from the current server configuration.

## Implementation Details
The MCP SDK doesn't automatically enforce root restrictions - you need to implement this yourself. A typical pattern is to create a helper function like is_path_allowed() that:

* Takes a requested file path
* Gets the list of approved roots
* Checks if the requested path falls within one of those roots
* Returns true/false for access permission

You then call this function in any tool that accesses files or directories before performing the actual file operation.

## Key Benefits
* User-friendly - Users don't need to provide full file paths
* Focused search - Claude only looks in approved directories, making file discovery faster
* Security - Prevents accidental access to sensitive files outside approved areas
* Flexibility - You can provide roots through tools or inject them directly into prompts

Roots make MCP servers both more powerful and more secure by giving Claude the context it needs to find files while maintaining clear boundaries around what it can access.


## server implementation

### Using the roots

On to the server. The server will use the roots in two scenarios:

* Whenever a tool attempts to access a file or folder
* When a LLM (like Claude) needs to resolve a file or folder to a full path. Think of when a user says 'read the todos.txt file' - Claude needs to figure out where the text file is, and might do so by looking at the list of roots

To handle the second case, we can either define a tool that lists out the roots or inject them directly in a prompt.

```python
@mcp.tool()
async def list_roots(ctx: Context):
    """
    List all directories that are accessible to this server.
    These are the root directories where files can be read from or written to.
    """
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    return [file_url_to_path(root.uri) for root in client_roots]
```

Roots are accessed by calling ctx.session.list_roots().

This sends a message back to the client, which causes it to run the root-listing callback.

> Remember: the MCP SDK does not attempt to limit what files or folders your tools attempt to read! You must implement that check yourself.

Consider implementing a function like is_path_allowed, which will decide whether a path is accessible by comparing it to the list of roots.

Once you've put an authorization function together - like is_path_allowed - use it throughout your tools to ensure the requested path is accessible.

## client implementation

The client doesn't immediately provide the list of roots to the server. Instead, the server can make a request to the client at some future point in time. We make a callback that will be executed when the server requests the roots. The callback needs to return the list of roots inside of a ListRootsResult object.

```python
    async def _handle_list_roots(
        self, context: RequestContext["ClientSession", None]
    ) -> ListRootsResult | ErrorData:
        """Callback for when server requests roots."""
        return ListRootsResult(roots=self._roots)

async def connect(self):
    server_params = StdioServerParameters(
        command=self._command,
        args=self._args,
        env=self._env,
    )
    stdio_transport = await self._exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    _stdio, _write = stdio_transport
    self._session = await self._exit_stack.enter_async_context(
        ClientSession(
            _stdio,
            _write,
            list_roots_callback=self._handle_list_roots
            if self._roots
            else None,
        )
    )
    await self._session.initialize()
```