from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import string

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-flash-latest")

STOPWORDS = {"is", "the", "a", "an", "how", "what", "does", "will", "i", "my", "to", "of", "in"}


def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    return set(word for word in words if word not in STOPWORDS)


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


faqs = load_faqs("faq.txt")


def find_best_match(user_question):
    user_words = preprocess(user_question)

    best_score = 0
    best_answer = None

    for question, answer in faqs.items():
        question_words = preprocess(question)
        score = len(user_words.intersection(question_words))

        if score > best_score:
            best_score = score
            best_answer = answer

    return best_answer


def generate_llm_response(context, question):
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

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "Error generating response."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")

    context = find_best_match(user_question)
    answer = generate_llm_response(context, user_question)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
