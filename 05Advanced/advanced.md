

## Extended thinking
Extended thinking is Claude's advanced reasoning feature that gives the model time to work through complex problems before generating a final response. Think of it as Claude's "scratch paper" - you can see the reasoning process that leads to the answer, which helps with transparency and often results in better quality responses.
https://platform.claude.com/docs/en/build-with-claude/extended-thinking

The key benefits include:
* Better reasoning capabilities for complex tasks
* Increased accuracy on difficult problems
* Transparency into Claude's thought process

However, there are important trade-offs:
* Higher costs (you pay for thinking tokens)
* Increased latency (thinking takes time)
* More complex response handling in your code

The signature is a cryptographic token that ensures you haven't modified the thinking text. This prevents developers from tampering with Claude's reasoning process, which could potentially lead the model in unsafe directions.

Redacted Thinking. This happens when Claude's thinking process gets flagged by internal safety systems. The redacted content contains the actual thinking in encrypted form, allowing you to pass the complete message back to Claude in future conversations without losing context. 


## Image support

There are several important limitations to keep in mind when working with images:

* Up to 100 images across all messages in a single request
* Max size of 5MB per image
* When sending one image: max height/width of 8000px
* When sending multiple images: max height/width of 2000px
* Images can be included as base64 encoding or a URL to the image
* Each image counts as tokens based on its dimensions: tokens = (width px × height px) / 750

## PDF support

## Citation 
When citations are enabled, Claude's response becomes more complex. Instead of simple text, you get structured data that includes citation information for each claim.

Each citation contains several key pieces of information:
* cited_text - The exact text from your document that supports Claude's statement
* document_index - Which document Claude is referencing (useful when you provide multiple documents)
* document_title - The title you assigned to the document
* start_page_number - Where the cited text begins
* end_page_number - Where the cited text ends

Citations are particularly valuable when:
* Users need to verify information for accuracy
* You're working with authoritative documents that users should be able to reference
* Transparency about information sources is critical for your application
* Users might want to explore the broader context around specific facts

## Prompt caching

Prompt caching offers several advantages:
* Faster responses: Requests using cached content execute more quickly
* Lower costs: You pay less for the cached portions of your requests
* Automatic optimization: The initial request writes to the cache, follow-up requests read from it

However, there are important limitations to keep in mind:
* Cache duration: Cached content only lives for one hour
* Limited use cases: Only beneficial when you're repeatedly sending the same content
* High frequency requirement: Most effective when the same content appears extremely frequently in your requests

Prompt caching works best for scenarios like document analysis workflows, where you're asking multiple questions about the same large document, or iterative editing tasks where the base content remains constant while you refine specific aspects.

Caching isn't enabled automatically - you need to manually add cache breakpoints to specific blocks in your messages. Here's how it works:

* Work done on messages is not cached automatically
* You must manually add a 'cache breakpoint' to a block
* Work done for everything before the breakpoint will be cached
* Cache will only be used on follow-up requests if the content up to and including the breakpoint is identical

System Prompts and Tools
You're not limited to text blocks - cache breakpoints can be added to:
* System prompts
* Tool definitions
* Image blocks
* Tool use and tool result blocks

Minimum Content Length
  There's a minimum threshold for caching: content must be at least 1024 tokens long to be cached. This is the sum of all messages and blocks you're trying to cache, not individual blocks.



## File API 
The Files API provides an alternative way to handle file uploads. Instead of encoding images or PDFs directly in your messages as base64 data, you can upload files ahead of time and reference them later.

Here's how it works:

* Upload your file (image, PDF, text, etc.) to Claude using a separate API call
* Receive a file metadata object containing a unique file ID
* Reference that file ID in future messages instead of including raw file data

## Code Execution Tool
Code execution is a server-based tool that doesn't require you to provide an implementation. You simply include a predefined tool schema in your request, and Claude can optionally execute Python code in an isolated Docker container.

Key characteristics of the code execution environment:
* Runs in an isolated Docker container
* No network access (can't make external API calls)
* Claude can execute code multiple times during a single conversation
* Results are captured and interpreted by Claude for the final response

### Downloading Generated Files
One of the most powerful features is Claude's ability to generate files (like plots or reports) and make them available for download. When Claude creates a visualization, it gets stored in the container and you can download it using the Files API.

Look for blocks with type: "code_execution_output" in the response - these contain file IDs for generated content: