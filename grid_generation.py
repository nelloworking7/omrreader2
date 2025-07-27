import cv2
import numpy as np

def generate_grids(image):
    # 흑백 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # 좌측 타이밍 마크 검출 (인적사항 제외)
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    timing_marks = [cv2.boundingRect(cnt) for cnt in contours if cv2.boundingRect(cnt)[2] > 5 and cv2.boundingRect(cnt)[3] > 10]

    # y좌표 기준 정렬
    timing_marks.sort(key=lambda x: x[1])
    timing_marks = sorted(timing_marks, key=lambda x: x[1])[:25]  # 20문항 이상 보장

    # 기준길이 = 마지막 두 마크의 y 차이
    base_len = timing_marks[-1][1] - timing_marks[-2][1]

    # x축 그리드: 1번 문제 y = timing_marks[0][1] + base_len * 5.2
    start_y = int(timing_marks[0][1] + base_len * 5.2)
    x_lines = [start_y + i * base_len for i in range(30)]  # 최대 30문항 처리

    # y축 그리드: 11번~ 오른쪽 마킹
    timing_marks.sort(key=lambda x: x[0])  # 좌우 정렬
    y_marks = timing_marks[10:]  # 11번부터 끝까지
    y_lines = [x + w//2 for (x, _, w, _) in y_marks]

    return x_lines, y_lines