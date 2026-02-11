import google.generativeai as genai

genai.configure(api_key="AIzaSyAbIC6MS4nqWBpk3xcT7_jbU9dII_thkAI")

model = genai.GenerativeModel("models/gemini-flash-latest")


def load_faqs(file_path):
    faqs = {}

    with open(file_path, "r") as file:
        content = file.read()

    blocks = content.split("Q:")

    for block in blocks:
        if block.strip():
            parts = block.split("A:")
            if len(parts) == 2:
                question = parts[0].strip()
                answer = parts[1].strip()
                faqs[question] = answer

    return faqs


def find_best_match(user_question, faqs):
    user_words = set(user_question.lower().split())
    best_score = 0
    best_answer = None

    for question, answer in faqs.items():
        question_words = set(question.lower().split())
        score = len(user_words.intersection(question_words))

        if score > best_score:
            best_score = score
            best_answer = answer

    return best_answer



def generate_llm_response(context, question):
    if not question.strip():
      return "Please enter a valid question."

    if context is None:
        return "Sorry, I could not find relevant information."
    
    prompt = f"""
    You are a helpful FAQ assistant.

    Use the following FAQ context to answer the user's question.
    If the answer is not present in the context, politely say you do not know.

    Context:
    {context}

    Question:
    {question}
    """

    response = model.generate_content(prompt)
    return response.text


def main():
    faqs = load_faqs("faq.txt")

    print("Smart FAQ Chatbot (type 'exit' to quit)")

    while True:
        user_question = input("\nAsk a question: ")

        if user_question.lower() == "exit":
            break

        context = find_best_match(user_question, faqs)
        answer = generate_llm_response(context, user_question)

        print("\nBot:", answer)


if __name__ == "__main__":
    main()
