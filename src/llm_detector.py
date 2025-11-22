from typing import Dict, Any
import json
import requests

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
    def __init__(self, model_name: str = "llama3.1", base_url: str = "http://localhost:11434"):
        """
        Local FREE detector powered by Ollama.

        Requirements:
          - Ollama installed (https://ollama.com)
          - Ollama server running:    `ollama serve`
          - Model pulled, e.g.:       `ollama pull llama3.1`
        """
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.chat_url = f"{self.base_url}/api/chat"

    def _call_llm_raw(self, text: str) -> str:
        """
        Call Ollama chat API and return raw text response.
        """
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": LLM_SYSTEM_PROMPT},
                {"role": "user", "content": LLM_USER_TEMPLATE.format(text=text)},
            ],
            "stream": False,
        }

        resp = requests.post(self.chat_url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        # Ollama chat API returns:
        # { "message": { "role": "...", "content": "..." }, ... }
        raw = data.get("message", {}).get("content", "")
        if not raw:
            # fallback if something weird happens
            raw = "{}"
        return raw

    def _parse_json(self, raw: str) -> Dict[str, Any]:
        raw = raw.strip()

        # Handle ```json ... ``` wrappers if the model adds them
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()

        try:
            parsed = json.loads(raw)
        except Exception:
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
