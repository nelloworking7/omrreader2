def grade_omr(markings, answer_sheet):
    scores = {}
    for q_num in markings:
        if q_num in answer_sheet:
            selected = list(markings[q_num].keys())[0]
            correct = answer_sheet[q_num]
            scores[q_num] = (selected == correct)
    return scores