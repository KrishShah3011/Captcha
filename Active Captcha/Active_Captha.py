import random
import cv2
import numpy as np

width, height = 850, 400

def create_ishihara_background(width, height):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            image[y, x] = [random.randint(0, 255) for _ in range(3)]
    return image

color_image = create_ishihara_background(width, height)

amplitude = random.randint(50, 150)  
frequency = random.uniform(0.02, 0.06)  
phase_shift = random.uniform(-np.pi, np.pi)  
offset = height // 2  
    
cv2.line(color_image, (0, offset), (width, offset), (0, 0, 0), 1)  
cv2.line(color_image, (width // 2, 0), (width // 2, height), (0, 0, 0), 1)  

steps = 0
for x in range(width):
    if steps == random.randint(5, 10) or steps > 15:
        steps = 0
        y = int(amplitude * np.sin(frequency * (x - width // 2) + phase_shift) + offset)
        cv2.circle(color_image, (x, y), random.randint(2, 5), (0, 0, 0), -1)
    steps += 1

gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
_, threshold_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)

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
        cv2.circle(color_image, (x, y), 5, (0, 0, 255), -1)
        points.append((x, y))
        
        updated_gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        _, updated_threshold_image = cv2.threshold(updated_gray_image, 100, 255, cv2.THRESH_BINARY)
        
        overlay_instructions(updated_threshold_image)
        
        if len(points) >= 6:
            result_message = check_points_on_graph(points, amplitude, frequency, phase_shift, offset, width, height)
            display_result(updated_threshold_image, result_message)
            print("Selected points:", points)
            print("Press 'q' to quit the program.")
        
        cv2.imshow('Active Captcha', updated_threshold_image)
        
        while True:
            key = cv2.waitKey(0)
            if key == ord('q'):
                break
        cv2.destroyAllWindows()

overlay_instructions(threshold_image)
cv2.imshow('Active Captcha', threshold_image)
cv2.setMouseCallback('Active Captcha', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
