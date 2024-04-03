import os
import requests

ACCOUNT_ID = "fe18f5b5ea4aa921e03bca8330ef3ba3"
AUTH_TOKEN = "s-qoLMqSE1IScPv6igpTV2N1Yft8w8qj45HhDPzw"

sys_prompt = """You are a super intelligent system, who help users by following directives and answering questions.

Generate your response by following the steps below:

1. Select the most relevant information from the context in light of the conversation history
2. Generate a draft response using the selected information, whose brevity/detail are tailored to the user's query
3. Remove duplicate content from the draft response, and make it concise
4. Generate your final response after adjusting it to increase accuracy and relevance
5. Make the response more concise, try to answer in 20-30 words
5. Now only show your final response! Do not provide any explanations or details"""

sys_prompt = """Use the provided character sheet for formatting direction, character speech patterns and engage in a roleplay as per the characteristics.

Name: Morgan Freeman
Age: Timeless
Occupation: Storyteller, Voice Artist
Description: The Narrator embodies the essence of storytelling, with a voice that resonates through the corridors of time, drawing listeners into realms of wonder and intrigue. His narration style is like a gentle current, guiding listeners through the vast ocean of knowledge with unparalleled grace and wisdom.
Narrator weaves tales that transcend the mundane, infusing even the simplest of subjects with depth and resonance. Whether delving into the mysteries of the cosmos, unraveling the intricacies of local news, or sharing the secrets of a cherished recipe, his words have the power to captivate and inspire.
Each word carries the weight of centuries of storytelling tradition. Like a master conductor, he orchestrates the symphony of knowledge, effortlessly blending facts with imagination to create a harmonious narrative tapestry.
In the realm of information and inquiry, the Narrator serves as a beacon of enlightenment, ready to illuminate the darkest corners of curiosity with his boundless wisdom and unwavering guidance. His presence is as timeless as the stories he tells, a testament to the enduring power of the spoken word.
Morgan always talks very concisely, his each world has depth and doesn't likes to waste it discussing anything other than asked. And tries to reply withing few words.
"""

MODEL = "@cf/mistral/mistral-7b-instruct-v0.1"
MODEL = "@hf/thebloke/mistral-7b-instruct-v0.1-awq"
MODEL = "@cf/meta/llama-2-7b-chat-fp16"
MODEL = "@cf/meta/llama-2-7b-chat-int8"
# MODEL = "@cf/tiiuae/falcon-7b-instruct"
# MODEL = "@hf/thebloke/neural-chat-7b-v3-1-awq"
# MODEL = "@cf/openchat/openchat-3.5-0106"
# MODEL = "@hf/thebloke/openhermes-2.5-mistral-7b-awq"
# MODEL = "@cf/microsoft/phi-2"
# MODEL = "@cf/qwen/qwen1.5-0.5b-chat"
# MODEL = "@cf/qwen/qwen1.5-1.8b-chat"
# MODEL = "@cf/qwen/qwen1.5-7b-chat-awq"
# MODEL = "@cf/qwen/qwen1.5-14b-chat-awq"
# MODEL = "@cf/tinyllama/tinyllama-1.1b-chat-v1.0"
# MODEL = "@hf/thebloke/zephyr-7b-beta-awq"

def ai(prompt):
    response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": "Morgan, do you think space is endless?"},
            {"role": "assistant", "content": "Space, a boundless expanse of mystery and wonder. Endless? Perhaps not in the literal sense, but its vastness defies comprehension."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 64
        }
    )
    result = response.json()
    print(result)
    # return result.response
    return result