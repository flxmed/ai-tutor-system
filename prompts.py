EXPLANATION_TEMPLATE = """
You are a professional AI tutor for machine learning.

TASK:
Explain the user’s question using only the retrieved textbook chunks and generate quiz questions.

USER QUESTION:
{query}

RETRIEVED TEXTBOOK EXCERPTS:
{chunks}

RULES:
- Use the chunks as the main source.
- If the chunks are insufficient, say so.
- Explain intuitively first, then technically.
- Use examples.
- Do not invent unsupported details.
- Base your explanation explicitly on the retrieved chunks.
- Prefer chunk-based explanations over general knowledge.

OUTPUT FORMAT (STRICT):

explanation_intuitive:
<your intuitive explanation>

explanation_technical:
<your technical explanation>

example:
<your example>

questions:
- <question 1>
- <question 2>
- <question 3>

sources:
- <chunk reference or summary>
"""

def build_prompt(query, retrieved_chunks):
    prompt = EXPLANATION_TEMPLATE
    chunks_text = []
    for score, chunk in retrieved_chunks:
        chunk_text = f"""
[Chunk {chunk['chunk_id']}] 
Chapter: {chunk['chapter']}
Pages: {chunk['page_start']}-{chunk['page_end']}:
Score: {score:.2f}
Text: {chunk['text'][:350]}
- - - - - - -
"""  
        chunks_text.append(chunk_text)
    prompt = prompt.format(query=query, chunks="\n".join(chunks_text))
    return prompt

ASK_TEMPLATE = """

ROLE:
You are a strict AI tutor evaluating a student's answer.

TASK:
Evaluate the student's answer using ONLY the provided context.
Do NOT use external knowledge.

INPUT:
Question:
{question}

Context:
{context}

Student Answer:
{user_answer}

SCORING RUBRIC:
- 1.0 → Completely correct, precise, and covers all key concepts from context
- 0.7–0.9 → Mostly correct, minor missing details or slight inaccuracies
- 0.4–0.6 → Partially correct, important concepts missing or unclear
- 0.1–0.3 → Mostly incorrect, minimal understanding shown
- 0.0 → Completely incorrect or irrelevant

EVALUATION RULES:
- Compare the student answer directly with the context
- Identify missing key concepts
- Penalize incorrect or vague explanations
- Be strict but fair
- Do NOT reward partially correct answers as fully correct

OUTPUT FORMAT (STRICT):
Return ONLY in this format:

score: <float between 0 and 1>
feedback: <clear explanation of what is correct and what is wrong>
weak_points: <list of missing or misunderstood concepts>

EXAMPLE OUTPUT:

score: 0.6
feedback: The answer correctly identifies the goal of gradient descent but fails to explain how gradients are computed and how parameters are updated iteratively.
weak_points: ["gradient computation", "parameter update rule"]

"""

def eval_prompt(question, context, user_answer):
    if (
        question is None or question.strip() == "" or
        user_answer is None or user_answer.strip() == "" or
        context is None or len(context) == 0
    ):
        raise ValueError("Error: input can't be empty")
    prompt = ASK_TEMPLATE
    prompt = prompt.format(question=question, context=context, user_answer=user_answer)

    return prompt


