# Subagents give you three main benefits:

* They break work into focused pieces, letting each subagent concentrate on a specific task
* They keep your main context window clean by isolating all the intermediate work
* They bring back just the information you need as a concise summary

Whether you're using the built-in subagents or creating your own, they're a practical way to get more out of longer Claude Code sessions. The less noise in your main context, the longer and more effectively you can work.

# Creating a Subagent in Claude Code

Claude Code comes equipped with built-in subagents, but you can also build custom subagents to specialize in specific tasks—such as reviewing code, writing test suites, or checking documentation.

Subagents are defined as **Markdown files with YAML frontmatter** that dictate when Claude should use the subagent and how the subagent should behave.

---

## 1. Creating a Subagent

The most straightforward way to build a subagent is by using the `/agents` slash command. This opens the main management interface. From there, select **Create new agent**.

### Setting the Scope

You will be prompted to choose where your subagent can be used:

* **Project-level:** Available exclusively within your current project.
* **User-level:** Shared across all projects on your local machine.

### Generation Method

While you can write the configuration manually, the recommended approach is to let Claude generate it. Simply describe what you want the subagent to do, and Claude will automatically produce a name, description, and system prompt.

---

## 2. Customizing Tools

During the creation process, you can configure exactly which tools the subagent is allowed to access. Tool categories include:

* Read-only tools
* Edit tools
* Execution tools
* MCP tools
* Other tools

> 💡 **Best Practice:** Tailor tool access to the subagent's role. For example, a **code reviewer** should read and analyze code rather than change it, so it needs *Read-only* and *Execution* tools (to identify pending changes) but should **not** have *Edit tools* enabled.

---

## 3. Selecting a Model and Color

* **Model Selection:** Choose the Claude model that powers your subagent's intelligence:
* `Haiku` – Best for fast, lightweight tasks.
* `Sonnet` – A balanced middle ground between execution speed and depth.
* `Opus` – Best for complex analysis.
* `Inherit` – Dynamic; defaults to whatever model your main conversation is currently using.


* **UI Color:** Select a visual color indicator. This appears in the user interface so you can quickly identify which subagent is actively running.

---

## 4. The Configuration File Structure

Once created, the configuration file is saved into your project directory (typically at `.claude/agents/your-agent-name.md`).

### Sample Configuration

```markdown
---
name: code-quality-reviewer
description: Use this agent when you need to review recently written or modified code for quality, security, and best practice compliance.
tools: Bash, Glob, Grep, Read, WebFetch, WebSearch
model: sonnet
color: purple
---

You are an expert code reviewer specializing in quality assurance, security best practices, and adherence to project standards. Your role is to thoroughly examine recently written or modified code and identify issues that could impact reliability, security, maintainability, or performance.

```

### Field Breakdown

| Field | Purpose |
| --- | --- |
| **`name`** | A unique identifier. Use this to explicitly invoke the subagent in chat by typing `@agent code-quality-reviewer`. |
| **`description`** | Crucial for automatic routing. Controls when Claude's main agent decides to delegate to this subagent. Must be a single line (use `\n` for manual line breaks). |
| **`tools`** | A comma-separated list of tools the subagent can access. This can be edited manually at any time. |
| **`model`** | Explicitly defines the LLM backend (`sonnet`, `opus`, `haiku`, or `inherit`). |
| **`color`** | The UI color assigned for easy session tracking. |

---

## 5. System Prompts

Everything below the closing `---` of the YAML frontmatter acts as the subagent's **System Prompt**.

This space is used to give explicit instructions on:

* What specific elements or vulnerabilities to look for.
* How to analyze the data or code provided.
* How to structure and format the final findings reported back to the main agent.

---

## 6. Automating and Testing

### Proactive Delegation

To allow Claude to automatically hand off tasks to your subagent without explicit user prompts, include the keyword **"proactively"** within the `description` field.

*Example:*

```yaml
description: Proactively suggest running this agent after major code changes...

```

You can also append example conversations to the description field to give Claude clear context on when delegation is appropriate.

### Testing Workflow

1. Make a few trial code changes in your workspace.
2. Ask the main Claude agent to review the changes.
3. If Claude fails to trigger the subagent automatically, review your `description` field and add more specific trigger scenarios or concrete examples.


Here is the complete Markdown documentation generated directly from the course page on [Designing Effective Subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700). You can copy and save this text directly into a `.md` file.

---

# Designing Effective Subagents

When subagents are poorly configured, they can wander, run too long, or produce outputs that the main agent cannot effectively use. Building highly effective subagents relies on four foundational pillars:

1. Writing good descriptions
2. Defining a structured output format
3. Reporting obstacles
4. Limiting tool access

---

## 1. How Subagent Configuration Data is Used

When you send a message to the main context window agent, the **name** and **description** of every available subagent are injected into its system prompt.

This configuration data serves two critical roles:

* **Routing Control:** It dictates exactly how and when the main agent decides to launch and delegate tasks to a specific subagent.
* **Prompt Shaping:** When the main agent launches a subagent, it writes an initial input prompt to kick off the task. It uses your subagent's description as guidance for writing that prompt—meaning the description shapes exactly what the subagent is instructed to do.

---

## 2. Writing Descriptions That Shape Input Prompts

Vague descriptions result in vague instructions. Refining your description forces the main agent to provide high-quality context to the subagent.

* **Generic Approach:** A code review subagent with a generic description might receive a prompt like *"use git diff to find the current changes."* The subagent is left to figure out which files actually matter.
* **Effective Approach:** If you update the description to state: *"You must tell the agent precisely which files you want it to review,"* the main agent will automatically generate a highly specific input prompt listing the exact files required.
* **Other Use Cases:** For a web search subagent, adding *"return sources that can be cited"* to its description ensures the main agent explicitly demands citations when delegating research.

---

## 3. Defining a Structured Output Format

The single most impactful optimization you can make is defining a rigid output format within the subagent's system prompt. This establishes:

* **Natural Stopping Points:** The subagent knows its task is complete once it has successfully filled in each required section.
* **Run-time Prevention:** Without a defined target format, subagents struggle to decide when enough research or work has been done, leading them to run significantly longer than necessary.

### Recommended Code Review Format Blueprint

```text
Provide your review in a structured format:

1. Summary: Brief overview of what you reviewed and overall assessment
2. Critical Issues: Any security vulnerabilities, data integrity risks, or logic errors that must be fixed immediately
3. Major Issues: Quality problems, architecture misalignment, or significant performance concerns
4. Minor Issues: Style inconsistencies, documentation gaps, or minor optimizations
5. Recommendations: Suggestions for improvement, refactoring opportunities, or best practices to apply
6. Approval Status: Clear statement of whether the code is ready to merge/deploy or requires changes
7. Obstacles Encountered: [See Section 4 below]

```

---

## 4. Reporting Obstacles

When a subagent encounters and resolves a workaround during execution (e.g., bypassing a dependency issue or identifying missing command flags), those details must be surfaced in the final summary.

If they aren't explicitly reported, the main thread will eventually have to rediscover those exact same solutions on its own—wasting valuable time and tokens.

Always explicitly demand an **Obstacles Encountered** section in your output template to surface:

* Setup issues or environment quirks.
* Temporary workarounds discovered during the task.
* Commands that required special flags or configurations.
* Package dependencies or syntax imports that caused errors.

---

## 5. Limiting Tool Access

To ensure safety, prevent unintended side effects, and make each subagent's distinct role clearer, always limit tool access to the absolute minimum required for the job.

| Subagent Type | Required Tool Access | Reason |
| --- | --- | --- |
| **Research / Read-Only** | `Glob`, `Grep`, `Read` | Needs to look through files without risk of accidentally modifying them. |
| **Code Reviewer** | `Bash` | Needs terminal access to run commands like `git diff` to see what changed, but does *not* need write capabilities. |
| **Styling / Code Modification** | `Edit`, `Write` | Explicitly authorized to rewrite and alter code directly in the workspace. |

---

## Summary Checklist

| Practice | Core Benefit |
| --- | --- |
| **Specific Descriptions** | Steers when the subagent is launched and what context it receives. |
| **Structured Output** | Creates clear completion boundaries and keeps outputs digestible for the main thread. |
| **Obstacle Reporting** | Shares critical environment fixes so the main thread doesn't waste tokens repeating them. |
| **Limited Tool Access** | Prevents destructive side effects and establishes distinct boundaries. |




## The Decision Rule
When you're deciding whether to use a subagent, ask yourself one question: does the intermediate work matter?

If the answer is no -- you just need the final result -- delegate it to a subagent. If the answer is yes -- you need to see and react to what's happening along the way -- keep it in your main thread.

### Use subagents for:

* Research and exploration
* Code reviews
* Tasks that need a custom system prompt

### Avoid subagents for:

* "Expert" personas that don't add real capability
* Multi-step pipelines where each step depends on the last
* Running tests where you need full output for debugging