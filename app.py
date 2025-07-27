import streamlit as st
from PIL import Image
import numpy as np
import cv2

from subject_codes import subject_codes
from subjects import subjects
from grid_generation import generate_grids
from marking_detection import detect_marking
from grading import grade_omr

st.title("OMR 채점 웹앱")

# 1페이지: 과목 선택
st.header("1. 채점할 과목 선택")
selected_subjects = st.multiselect("과목을 선택하세요", options=list(subject_codes.keys()), format_func=lambda x: subject_codes[x])
go_next = st.button("입력 완료")

if go_next:
    st.session_state['selected_subjects'] = selected_subjects

# 2페이지: 정답 입력
if 'selected_subjects' in st.session_state:
    st.header("2. 정답 입력")
    answers = {}
    for code in st.session_state['selected_subjects']:
        subject_info = subjects[code]
        st.subheader(f"{subject_info['name']} 정답 입력")
        ans_input = st.text_input(f"{subject_info['name']} 정답 (쉼표로 구분된 번호)", key=f"ans_{code}")
        if ans_input:
            answer_list = list(map(int, ans_input.split(',')))
            answers[code] = dict(zip(range(1, len(answer_list) + 1), answer_list))
    st.session_state['answers'] = answers

    if st.button("정답 입력 완료"):
        st.session_state['input_done'] = True

# 3페이지: 이미지 업로드 및 채점
if st.session_state.get('input_done'):
    st.header("3. OMR 이미지 업로드")
    uploaded = st.file_uploader("이미지 파일 업로드", type=['jpg', 'png'])

    if uploaded:
        image = Image.open(uploaded)
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

        x_lines, y_lines = generate_grids(image_cv)
        markings = detect_marking(gray, x_lines, y_lines)

        for code in st.session_state['selected_subjects']:
            st.subheader(f"{subjects[code]['name']} 채점 결과")
            score = grade_omr(markings, st.session_state['answers'][code])
            st.write(score)