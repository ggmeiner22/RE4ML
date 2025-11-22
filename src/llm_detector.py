from typing import Dict, Any
import json
# from openai import OpenAI  # Uncomment if using OpenAI client

LLM_SYSTEM_PROMPT = """
You are an expert requirements engineer.
Given a single software or ML system requirement, decide whether it is CLEAR or AMBIGUOUS.

A requirement is AMBIGUOUS if:
- It uses vague terms (e.g., 'fast', 'user-friendly', 'robust') without measurable criteria, OR
- It refers to unstated conditions (e.g., 'as needed', 'when appropriate'), OR
- It lacks necessary details like thresholds, units, or clear actors.

Return ONLY a JSON object with fields:
- label: "clear" or "ambiguous"
- reason: a short explanation.
"""

LLM_USER_TEMPLATE = """
Requirement:
"{text}"

Respond as specified.
"""


class LLMDetector:
    def __init__(self, client=None, model_name: str = "gpt-4.1-mini"):
        """
        Pass in your configured LLM client (e.g., OpenAI()) if you want.
        For now, this is left as a placeholder.
        """
        # Example:
        # self.client = client or OpenAI()
        self.client = client
        self.model_name = model_name

    def _call_llm(self, text: str) -> Dict[str, Any]:
        """
        Call your LLM and return parsed JSON.

        Replace this implementation with your actual LLM API call.
        Right now it's a placeholder so this file runs without an API key.
        """

        # Example with OpenAI (uncomment and adjust):
        #
        # response = self.client.chat.completions.create(
        #     model=self.model_name,
        #     messages=[
        #         {"role": "system", "content": LLM_SYSTEM_PROMPT},
        #         {"role": "user", "content": LLM_USER_TEMPLATE.format(text=text)},
        #     ],
        #     temperature=0.0,
        # )
        # raw = response.choices[0].message.content
        #
        # # Try to extract JSON
        # raw = raw.strip()
        # if raw.startswith("```"):
        #     # Remove ```json ... ``` wrapper
        #     raw = raw.strip("`")
        #     if raw.lower().startswith("json"):
        #         raw = raw[4:].strip()
        # parsed = json.loads(raw)

        # Placeholder implementation (always "ambiguous"):
        parsed = {
            "label": "ambiguous",
            "reason": "Placeholder LLM result: configure real API call."
        }
        return parsed

    def analyze(self, text: str) -> Dict[str, Any]:
        return self._call_llm(text)
