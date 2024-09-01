import random
import cv2
import numpy as np

width, height = 800, 400

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


cv2.imshow('Active Captha ', threshold_image)


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
        print("Exactly 3 points are above the graph and 3 points are below the graph.")
    else:
        print("The points do not match the required condition.")
        
points = []

def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(color_image, (x, y), 5, (0, 0, 255), -1)
        points.append((x, y))
        
        updated_gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        _, updated_threshold_image = cv2.threshold(updated_gray_image, 100, 255, cv2.THRESH_BINARY)
        
        cv2.imshow('Active Captha ', updated_threshold_image)
        
        if len(points) >= 6:
            print("Selected points:", points)
            check_points_on_graph(points, amplitude, frequency, phase_shift, offset, width, height)
            print("Press 'q' to quit the program.")

            while True:
                key = cv2.waitKey(0)
                if key == ord('q'):
                    break
            cv2.destroyAllWindows()

cv2.setMouseCallback('Active Captha ', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
