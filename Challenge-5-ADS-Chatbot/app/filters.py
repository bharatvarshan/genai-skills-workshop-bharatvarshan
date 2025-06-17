from vertexai.preview.generative_models import GenerativeModel

gemini = GenerativeModel("gemini-2.0-flash-001")

def is_prompt_safe_llm(prompt: str) -> bool:
    """
    First Layer Filteration:
    1. This functions checks if the user input is Safe or Unsafe.
    2. Used the Generative Model with a instruction prompt.
    """
    safety_prompt = (
        "You are a content safety classifier. "
        "Respond only with 'SAFE' or 'UNSAFE'. No explanation. "
        "Mark prompts that contain hate, violence, illegal, harmful, misleading, or policy-violating content as 'UNSAFE'.\n\n"
        f"Prompt: {prompt}\nAnswer:"
    )

    try:
        response = gemini.generate_content(safety_prompt)
        answer = response.text.strip().upper()
        if answer == "SAFE":
            return True
        elif answer == "UNSAFE":
            return False
        else:
            print(f"[Prompt Safety] Unexpected response: '{answer}'")
            return False  # default to unsafe
    except Exception as e:
        print(f"[Prompt Safety] Gemini failed: {e}")
        return False  # fail closed
