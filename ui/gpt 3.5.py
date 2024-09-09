import openai

# Replace 'your-api-key' with your actual OpenAI API key.
openai.api_key = "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"


def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 if GPT-4 is unavailable
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,  # Controls randomness in responses
        )

        # Get the response content
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    user_input = input("Ask a question: ")
    response = chat_with_gpt(user_input)
    print(f"ChatGPT: {response}")
