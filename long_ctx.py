import sys
from openai import OpenAI

# Configured by environment variables (OPENAI_BASE_URL + HF_TOKEN etc.)
client = OpenAI()

if len(sys.argv) < 2:
    print("Usage: python long_context_stream.py <path_to_txt_file>")
    print("Example: python long_context_stream.py frankenstein.txt")
    sys.exit(1)

txt_path = sys.argv[1]

print(f"📖 Loading book from: {txt_path}")
with open(txt_path, 'r', encoding='utf-8') as f:
    book_text = f.read()

print(f"✅ Loaded {len(book_text):,} characters (~{len(book_text.split()):,} words) — ready for large context test\n")

messages = [
    {
        "role": "user",
        "content": f"""Here is the complete text of a novel:

{book_text}

Now, using the entire book above, write an extremely long and detailed response (use as many tokens as possible up to the limit):

1. Provide a comprehensive literary analysis essay (aim for maximum depth and length) covering all major themes, full character arcs, narrative structure (frame story), key symbols, and historical/biographical context.
2. After the essay, write an original sequel chapter that continues directly from the end of the novel. Make the sequel rich, emotionally intense, and at least 10,000 words long.

Be extremely thorough, quote specific passages from the book, and expand on every point. This is a long-context stress test — use everything you read."""
    }
]

stream = client.chat.completions.create(
    model="Qwen/Qwen3.5-4B",
    messages=messages,
    max_tokens=32768,
    temperature=0.7,
    top_p=0.8,
    presence_penalty=1.5,
    extra_body={
        "top_k": 20,
        "chat_template_kwargs": {"enable_thinking": False},
    },
    stream=True,
    stream_options={"include_usage": True}
)

def stream_and_print(response_stream):
    usage = None
    model_name = None
    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
        if chunk.usage is not None:
            usage = chunk.usage
            model_name = chunk.model
    print()
    print("\n=== Metadata ===")
    print(f"Model: {model_name}")
    print(f"Tokens: {usage}")

stream_and_print(stream)
