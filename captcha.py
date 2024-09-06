import random
import cv2
import numpy as np

width, height = 850, 400

def create_ishihara_background(width, height):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            image[y, x] = [random.randint(0, 254)] * 3  # Grayscale image
    return image

gray_image = create_ishihara_background(width, height)

amplitude = random.randint(50, 100)
frequency = random.uniform(0.02, 0.06)
phase_shift = random.uniform(-np.pi, np.pi)
offset = height // 2

steps = 0
for x in range(width):
    if steps == random.randint(5, 8) or steps > 10:
        steps = 0
        y = int(amplitude * np.sin(frequency * (x - width // 2) + phase_shift) + offset)
        # Ensure y is within image bounds
        y = min(max(y, 0), height - 1)
        cv2.circle(gray_image, (x, y), random.randint(2, 4), (0, 0, random.randint(0, 254)), -1)
    steps += 1

def overlay_instructions(image):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Mark three points above the graph and three below."
    font_scale = 1
    font_thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

    text_x, text_y = 10, 30
    rect_x1, rect_y1 = text_x - 10, text_y - text_size[1] - 10
    rect_x2, rect_y2 = text_x + text_size[0] + 10, text_y + 10
    cv2.rectangle(image, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 0), -1)
    cv2.putText(image, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

def display_result(image, message):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_size = cv2.getTextSize(message, font, font_scale, font_thickness)[0]
    text_x, text_y = 10, height - 30
    rect_x1, rect_y1 = text_x - 10, text_y - text_size[1] - 10
    rect_x2, rect_y2 = text_x + text_size[0] + 10, text_y + 10
    cv2.rectangle(image, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 0), -1)
    cv2.putText(image, message, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

def check_points_on_graph(points, amplitude, frequency, phase_shift, offset, width, height):
    above = 0
    below = 0

    for (x, y) in points:
        graph_y = int(amplitude * np.sin(frequency * (x - width // 2) + phase_shift) + offset)
        # Ensure graph_y is within image bounds
        graph_y = min(max(graph_y, 0), height - 1)

        if y < graph_y:
            above += 1
        else:
            below += 1

    if above == 3 and below == 3:
        result_message = "Correct! Exactly 3 points are above and 3 below."
    else:
        result_message = "Incorrect. The points do not match the required condition."

    return result_message

points = []

def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        # Draw a cross at the clicked position
        cross_size = 10
        cross_color = (0, 255, 0)  # Green color for the cross
        cv2.line(gray_image, (x - cross_size, y), (x + cross_size, y), cross_color, 2)
        cv2.line(gray_image, (x, y - cross_size), (x, y + cross_size), cross_color, 2)

        points.append((x, y))

        if len(points) >= 6:
            result_message = check_points_on_graph(points, amplitude, frequency, phase_shift, offset, width, height)
            display_result(gray_image, result_message)
            print("Selected points:", points)
            print(result_message)
            print("Press 'q' to quit the program.")

        cv2.imshow('Active Captcha', gray_image)

        while True:
            key = cv2.waitKey(0)
            if key == ord('q'):
                break
        cv2.destroyAllWindows()

overlay_instructions(gray_image)
cv2.imshow('Active Captcha', gray_image)
cv2.setMouseCallback('Active Captcha', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
