from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
import re
import ast


# =========================
# HOME
# =========================
def home(request):
    return render(request, "index.html")


# =========================
# GENERATE CODE (CLEAN + SAFE)
# =========================
def generate_code(request):
    if request.method != "POST":
        return JsonResponse({"code": "Invalid request method."})

    try:
        data = json.loads(request.body)
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return JsonResponse({"code": "Please provide a prompt."})

        strict_prompt = f"""
You are a senior Python developer.

Generate a simple, correct, beginner-friendly Python program.

Rules:
- Return ONLY executable Python code.
- No markdown.
- No backticks.
- No explanations.
- No comments.
- If input is required, use input().
- Always print results using print().
- Code must run without syntax errors.

User request:
{prompt}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": strict_prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            return JsonResponse({"code": f"Model Error: {response.text}"})

        result = response.json()
        raw_code = result.get("response", "").strip()

        # 🔥 Remove markdown & quotes
        raw_code = re.sub(r"```python", "", raw_code)
        raw_code = re.sub(r"```", "", raw_code)
        raw_code = raw_code.replace('"""', "")
        raw_code = raw_code.replace("'''", "")

        # 🔥 Remove explanation lines
        lines = raw_code.split("\n")
        cleaned_lines = []

        for line in lines:
            stripped = line.strip().lower()

            if stripped.startswith((
                "here",
                "sure",
                "this",
                "below",
                "example",
                "for example"
            )):
                continue

            cleaned_lines.append(line)

        cleaned_code = "\n".join(cleaned_lines).strip()

        # 🔥 Validate syntax
        try:
            ast.parse(cleaned_code)
        except SyntaxError:
            split_lines = cleaned_code.split("\n")

            for i in range(len(split_lines)):
                attempt = "\n".join(split_lines[i:])
                try:
                    ast.parse(attempt)
                    cleaned_code = attempt
                    break
                except SyntaxError:
                    continue

        return JsonResponse({"code": cleaned_code.strip()})

    except requests.exceptions.Timeout:
        return JsonResponse({"code": "Model response timed out."})

    except Exception as e:
        return JsonResponse({"code": f"Generation Error: {str(e)}"})