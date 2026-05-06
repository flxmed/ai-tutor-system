from tutor import ask_tutor
from session import start_session, record_answer
from prompts import eval_prompt
from groq import Groq
from config import GROQ_API_KEY, PRIMARY_MODEL, MAX_EXPLANATION_TOKENS, EXPLANATION_TEMPERATURE
import ast

def receive_query():
    while True:
        query = input("Enter your question(type exit to exit): ")
        if query.lower() == "exit":
            exit()
        else:

            while not query.strip():
                print("Query cannot be empty. Please enter a valid question.")
                query = input("Enter your question: ")


            return query

def evaluate_answer(question, chunks, answer):
    prompt = eval_prompt(question, chunks, answer)
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {"role": "system", "content": "You are a strict AI tutor evaluating a student's answer."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(messages=messages, model=PRIMARY_MODEL, max_tokens=MAX_EXPLANATION_TOKENS, temperature=EXPLANATION_TEMPERATURE)
    response_content = response.choices[0].message.content
    lines = response_content.splitlines()
    score = None
    feedback = None
    weak_points = None

    for line in lines:
        line = line.strip()
        if line.startswith("score:"):
            key, value = line.split(":", 1)
            value = value.strip()
            score = float(value)
        if line.startswith("feedback:"):
            key, value = line.split(":", 1)
            value = value.strip()
            feedback = value
        if line.startswith("weak_points:"):
            key, value = line.split(":", 1)
            value = value.strip()
            weak_points = ast.literal_eval(value)

    return {
        "score": score,
        "feedback": feedback,
        "weak_points": weak_points
    }

query = receive_query()
session = start_session(query)

while True: 
    tutor_answer, chunks = ask_tutor(query)

    print(tutor_answer)

    intuitive = ""
    technical = ""
    example = ""
    questions = []
    current_section = None

    lines = tutor_answer.splitlines()
    for line in lines:
        line = line.strip()

        if line.startswith("explanation_intuitive:"):
            current_section = "intuitive"
        elif line.startswith("explanation_technical:"):
            current_section = "technical"
        elif line.startswith("example:"):
            current_section = "example"
        elif line.startswith("questions:"):
            current_section = "questions"

        else:
            if current_section == "intuitive":
                intuitive += line + "\n"

            elif current_section == "technical":
                technical += line + "\n"

            elif current_section == "example":
                example += line + "\n"

            elif current_section == "questions":
                if line.startswith("-"):
                    questions.append(line[1:].strip())

    print(intuitive)
    if not questions:
        raise ValueError("Question list is empty")
    
    else:
        ask_user = input(f"Answer this question\n {questions[0]}: ")
        result = evaluate_answer(questions[0], chunks, ask_user)
        question_id = session["total_questions"] + 1
        record_answer(session, question_id, ask_user, result["score"], result["weak_points"], result["feedback"])
        print(result["score"])
        print(result["feedback"])
        

    



    

    




