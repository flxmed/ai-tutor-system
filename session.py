def start_session(query):
    session = {
        "topic": query,
        "questions": [],
        "results": [],
        "total_score": 0.0,
        "total_questions": 0,
        "weak_points": [],
        "mastered": False
    }

    return session

def record_answer(session, question_id, user_answer, score, weak_points, feedback):
    record = {
        "question_id": question_id,
        "user_answer": user_answer,
        "score": score,
        "weak_points": weak_points,
        "feedback": feedback
    }
    session["results"].append(record)
    session["total_questions"] += 1
    session["total_score"] += score
    session["weak_points"].extend(weak_points)
    average = session["total_score"] / session["total_questions"]
    if average >= 0.8:
        session["mastered"] = True
    else:
        session["mastered"] = False




    




    
