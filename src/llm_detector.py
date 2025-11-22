from typing import Dict, Any
import json
# from openai import OpenAI  # Uncomment if using OpenAI client

LLM_SYSTEM_PROMPT = """
You are an expert requirements engineer.

Given a single software or ML system requirement, you MUST:

1. Decide whether it is CLEAR or AMBIGUOUS.
2. Give a short explanation (reason).
3. If it is AMBIGUOUS, propose a clearer rewrite that:
   - Uses measurable, testable language.
   - Adds thresholds/units where appropriate.
   - Keeps the original intent.

Output MUST be a JSON object with fields:
- "label": "clear" or "ambiguous"
- "reason": string
- "rewrite": string or null

If the requirement is already clear, set "rewrite" to null.
"""

LLM_USER_TEMPLATE = """
Requirement:
"{text}"

Respond ONLY with the JSON object described above.
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

    def _call_llm_raw(self, text: str) -> str:
        """
        Call your LLM and return raw string response.

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

        # Placeholder JSON so code runs without an API call:
        raw = json.dumps({
            "label": "ambiguous",
            "reason": "Placeholder LLM result: configure real API call.",
            "rewrite": "Placeholder rewrite suggestion."
        })
        return raw

    def _parse_json(self, raw: str) -> Dict[str, Any]:
        raw = raw.strip()

        # Handle ```json ... ``` wrappers if the model adds them
        if raw.startswith("```"):
            # strip leading/trailing fences
            raw = raw.strip("`")
            # after stripping backticks, it may start with 'json'
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            # Fall back to a safe default
            parsed = {
                "label": "ambiguous",
                "reason": "Failed to parse JSON from LLM output.",
                "rewrite": None,
            }
        # Normalize fields
        label = str(parsed.get("label", "ambiguous")).lower()
        if label not in ("clear", "ambiguous"):
            label = "ambiguous"
        reason = str(parsed.get("reason", "")).strip()
        rewrite = parsed.get("rewrite", None)
        if rewrite is not None:
            rewrite = str(rewrite).strip()
            if not rewrite:
                rewrite = None

        return {"label": label, "reason": reason, "rewrite": rewrite}

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Return a dict with:
        {
          "label": "clear" or "ambiguous",
          "reason": "...",
          "rewrite": "..." or None
        }
        """
        raw = self._call_llm_raw(text)
        return self._parse_json(raw)

    def rewrite_only(self, text: str) -> str:
        """
        Convenience helper: returns only the rewrite suggestion if ambiguous,
        or the original text if already clear or if no rewrite is provided.
        """
        result = self.analyze(text)
        if result.get("label") == "ambiguous" and result.get("rewrite"):
            return result["rewrite"]
        return text
