import os
from openai import OpenAI

MODEL = "gpt-4o-mini"  # Using gpt-4o-mini - the most cost-effective option (cheaper than gpt-3.5-turbo)


def make_client(api_key: str = None):
    # if api_key is None, the OpenAI library will pick from env
    if api_key:
        return OpenAI(api_key=api_key)
    return OpenAI()


def generate_section(prompt_template: str, requirement_text: str, api_key: str = None, max_tokens: int = 2000):
    client = make_client(api_key)
    prompt = prompt_template.replace("{requirement}", requirement_text)
    # Chat completion style
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs structured BA artifacts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        # pick the first choice - use attribute access for OpenAI SDK
        text = response.choices[0].message.content
        return text
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {e}")


def generate_all(requirement_text: str, prompts_dir: str = "prompts", api_key: str = None, max_tokens: int = 2000):
    outputs = {}
    # load templates
    # Flows generation commented out to save API costs - can be re-enabled later
    for name in ["user_stories.txt", "acceptance_criteria.txt", "test_cases.txt", "summary.txt"]:  # "flows.txt" commented out
        path = os.path.join(prompts_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                template = f.read()
            key = name.replace('.txt','')
            outputs[key] = generate_section(template, requirement_text, api_key, max_tokens)
        except FileNotFoundError:
            raise Exception(f"Prompt file not found: {path}")
        except Exception as e:
            raise Exception(f"Error processing {name}: {e}")
    
    # Set empty flows to prevent errors when accessing outputs.get('flows')
    outputs['flows'] = ""
    
    return outputs