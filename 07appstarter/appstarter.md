01 first open claud and use the following instruction
```acl
read @README.md file and execute the setup directions leasted in it 
```

02 execute 
```
/init
```


## Common Workflows
Claude works best when you approach it as an effort multiplier. The more context and structure you provide, the better results you'll get. Here's the most effective workflow:

* Step 1: Feed Context into Claude
Before asking Claude to build something, identify files in your codebase that are relevant to the feature you want to create. Ask Claude to read and analyze these files first. This gives Claude examples of your coding patterns and existing functionality it can build upon.
```
Read and analize the math.py and document.py files
```

* Step 2: Tell Claude to Plan a Solution
Instead of jumping straight to implementation, ask Claude to think through the problem and create a plan. Tell Claude specifically not to write any code yet - just focus on the approach and steps needed.
```
shif + tab -> plan mode

build a new tool called "Document_pass_to_markdown". It should take in the path to a PDF or DOCX file, read the file then convert its contents to Markdown and return the result. Write out a plan to implement this feature. Don't write any code yet. 
```
* Step 3: Ask Claude to Implement the Solution
Once you have a solid plan, ask Claude to implement it. Claude will write code based on the context and planning work you've already done together.
```
implement the plan
```
Test-Driven Development Workflow
For even better results, you can use a test-driven approach:

* Feed context into Claude - Same as before, show Claude relevant files
```
Read and analize the math.py and document.py files
```
* Ask Claude to think of test cases - Have Claude brainstorm what tests would validate your new feature
```
think of some tests to write to evaluate a new tool called "Document_pass_to_markdown". It should take in the pass to a PDF or DOCX file, read the file, then convert its contents to markdown and return the result Don't write any code yet 
```
* Ask Claude to implement those tests - Select the most relevant tests and have Claude write them
```
implement test 1-4 
```
* Ask Claude to write code that passes the tests - Claude will iterate on the implementation until all tests pass
```
write code to make the tests pass. Remember to connect the document tool to the MCP server in MAIN.py Also remember to run a test with 'uv' 
```
This approach often produces more robust code because Claude has clear success criteria to work toward.