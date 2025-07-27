import numpy as np

def detect_marking(image, x_lines, y_lines, threshold=0.5):
    height, width = image.shape
    result = {}

    for j, x in enumerate(x_lines):
        for i, y in enumerate(y_lines):
            x1, y1 = y - 10, x - 10
            x2, y2 = y + 10, x + 10

            x1, x2 = max(0, x1), min(width, x2)
            y1, y2 = max(0, y1), min(height, y2)

            region = image[y1:y2, x1:x2]
            dark_ratio = np.sum(region < 127) / region.size

            if dark_ratio > threshold:
                if j not in result:
                    result[j] = {}
                result[j][i] = 1  # 마킹됨

    return result