# Task Completion Checker

This is a simple intelligent contract experiment that uses AI to verify if tasks were actually completed.

## What it does

You give it:
- A task description (what needed to be done)
- A completion statement (what someone claims they did)

It tells you:
- **Completed** - Yep, task was done
- **Not Completed** - Nope, doesn't match
- **Needs Clarification** - Unclear or vague

## Example

```python
task = "Write a blog post about AI"
statement = "I published a 1500-word article on AI trends"
# Result: Completed ✓
```

```python
task = "Fix the login bug"
statement = "I worked on some stuff"
# Result: Needs Clarification
```

## How it works

The contract uses GenLayer's consensus mechanism to evaluate task completion. Multiple AI validators independently assess whether the completion statement matches the task, then reach consensus on the result.

## Why I made this

Just playing around with AI-powered smart contracts and seeing how they can handle subjective evaluations. Thought it'd be interesting to automate the "did you actually do it?" question.

## Setup

Depends on `py-genlayer:test`

Initialize with your task and completion statement:

```python
checker = TaskCompletionChecker(
    task_description="Your task here",
    completion_statement="What was done"
)

result = checker.check_completion()
print(result['status'])
print(result['reasoning_summary'])
```

---

This is purely experimental, if any errors turn up, please do not hesitate to let me know
