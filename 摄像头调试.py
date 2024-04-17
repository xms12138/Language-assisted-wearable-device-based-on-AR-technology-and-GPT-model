import cv2
import time
import main

def put_text_multiline(img, text, position, font, font_scale, font_color, thickness, max_line_width):
    lines = []
    font_height = cv2.getTextSize(text, font, font_scale, thickness)[0][1]
    line = ''
    for word in text.split():
        test_line = f'{line} {word}'.strip()
        width = cv2.getTextSize(test_line, font, font_scale, thickness)[0][0]
        if width <= max_line_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    y = position[1]
    for line in lines:
        cv2.putText(img, line, (position[0], y), font, font_scale, font_color, thickness)
        y += font_height


def run():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        exit()
    time_start = time.time()
    font = cv2.FONT_HERSHEY_SIMPLEX
    global text
    text = 'Hello, Sun Mingze'
    text_position = (15, 30)
    font_scale = 0.7
    #font_color = (250, 206, 135)
    font_color = (0,0,0)
    thickness = 2
    max_line_width = 500  # 最大行宽
    copy = 'Hello, Sun Mingze'

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        put_text_multiline(frame, text, text_position, font, font_scale, font_color, thickness, max_line_width)

        cv2.imshow('VR VIVE', frame)
        if time.time() - time_start > 5:
            text = "Hello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun Mingze"
        if time.time() - time_start > 7:
            text = "Hello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun MingzeHello, Sun Mingze"
        if time.time() - time_start > 9:
            text = "Hello, Sun MingzeHello, Sun Mingze"

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


run()
