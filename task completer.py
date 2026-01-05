# { "Depends": "py-genlayer:test" }

from genlayer import *


class TaskCompletionChecker(gl.Contract):
    """
    A simple Intelligent Contract that evaluates whether a task has been completed
    based on a task description and a completion statement.

    Returns one of three statuses:
    - Completed: The completion statement clearly matches the task
    - Not Completed: The statement does not align with the task
    - Needs Clarification: The statement is vague, incomplete, or partially related
    """

    task_description: str
    completion_statement: str
    status: str
    reasoning_summary: str

    def __init__(self, task_description: str, completion_statement: str):
        """
        Initialize the contract with task details.

        Args:
            task_description: A brief sentence explaining what the task was
            completion_statement: What the user claims to have done
        """
        self.task_description = task_description
        self.completion_statement = completion_statement
        self.status = ""
        self.reasoning_summary = ""

    @gl.public.write
    def check_completion(self) -> dict:
        """
        Main method that evaluates task completion using AI reasoning.

        Returns:
            dict: Contains 'status' and 'reasoning_summary'
        """

        def evaluate_task():
            """Non-deterministic block that uses LLM to evaluate task completion"""

            prompt = f"""You are evaluating whether a task has been completed.

Task Description: "{self.task_description}"
Completion Statement: "{self.completion_statement}"

Your job is to compare these two statements and determine if the task was actually completed.

Rules:
1. If the completion statement clearly shows the task was done as described, respond with "Completed"
2. If the completion statement shows something different was done or the task wasn't done, respond with "Not Completed"
3. If the completion statement is vague, unclear, or only partially addresses the task, respond with "Needs Clarification"
4. Do not invent details that weren't provided
5. If key information is missing, default to "Needs Clarification"

Respond in EXACTLY this format:
STATUS: [Completed / Not Completed / Needs Clarification]
REASONING: [2-4 sentences explaining your decision clearly and simply]"""

            result = gl.exec_prompt(prompt)
            return result

        # Use equivalence principle to get consensus on the evaluation
        llm_response = gl.eq_principle.llm_eq(evaluate_task)

        # Parse the response
        self._parse_response(llm_response)

        return {
            "status": self.status,
            "reasoning_summary": self.reasoning_summary
        }

    def _parse_response(self, response: str) -> None:
        """
        Parse the AI response to extract status and reasoning.

        Args:
            response: The raw AI response text
        """
        lines = response.strip().split('\n')

        for line in lines:
            if 'STATUS:' in line:
                self.status = line.replace('STATUS:', '').strip()
            elif 'REASONING:' in line:
                self.reasoning_summary = line.replace('REASONING:', '').strip()

        # Validate that we got both required fields
        if not self.status or not self.reasoning_summary:
            self.status = "Needs Clarification"
            self.reasoning_summary = "Unable to parse the evaluation response properly."

    @gl.public.view
    def get_status(self) -> str:
        """
        Get the current evaluation status.

        Returns:
            str: The status (Completed, Not Completed, or Needs Clarification)
        """
        return self.status

    @gl.public.view
    def get_reasoning(self) -> str:
        """
        Get the reasoning summary for the evaluation.

        Returns:
            str: The reasoning explanation
        """
        return self.reasoning_summary

    @gl.public.view
    def get_task_info(self) -> dict:
        """
        Get all task information including the original inputs.

        Returns:
            dict: Complete task information
        """
        return {
            "task_description": self.task_description,
            "completion_statement": self.completion_statement,
            "status": self.status,
            "reasoning_summary": self.reasoning_summary
        }
