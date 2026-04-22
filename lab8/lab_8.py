import cv2
import numpy as np


img = cv2.imread('variant-10.jpg')
ret, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
cv2.waitKey(0)
cv2.imshow('photo', thresh)

fly_img = cv2.imread('fly64.png', cv2.IMREAD_UNCHANGED)

def overlay_image(frame, overlay, x_center, y_center):
    if overlay is None:
        return frame
    
    fh, fw = overlay.shape[:2]
    H, W = frame.shape[:2]

    x1 = int(x_center - fw / 2)
    y1 = int(y_center - fh / 2)
    x2 = x1 + fw
    y2 = y1 + fh

    x1_c, y1_c = max(0, x1), max(0, y1)
    x2_c, y2_c = min(W, x2), min(H, y2)
    
    if x1_c >= x2_c or y1_c >= y2_c:
        return frame

    overlay_part = overlay[y1_c-y1:y2_c-y1, x1_c-x1:x2_c-x1]
    roi = frame[y1_c:y2_c, x1_c:x2_c]

    alpha = overlay_part[:, :, 3] / 255.0
    for c in range(3):
        roi[:, :, c] = (alpha * overlay_part[:, :, c] + (1 - alpha) * roi[:, :, c])

    return frame

def video_processing():
    cap = cv2.VideoCapture(0)
    
    rotate_flag = False
    inside_flag = False
    
    MIN_AREA = 500

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h_frame, w_frame = frame.shape[:2]
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        half_fixed = 75
        gx1, gy1 = w_frame//2 - half_fixed, h_frame//2 - half_fixed
        gx2, gy2 = w_frame//2 + half_fixed, h_frame//2 + half_fixed
        cv2.rectangle(frame, (gx1, gy1), (gx2, gy2), (0, 255, 0), 2)

        marker_found = False
        for c in contours:
            area = cv2.contourArea(c)
            if area > MIN_AREA:
                x, y, w, h = cv2.boundingRect(c)
                aspect_ratio = float(w) / h
                
                if 0.7 < aspect_ratio < 1.3:
                    obj_cx, obj_cy = x + w // 2, y + h // 2
                    marker_found = True
                    
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    
                    frame = overlay_image(frame, fly_img, obj_cx, obj_cy)

                    if gx1 < obj_cx < gx2 and gy1 < obj_cy < gy2:
                        if not inside_flag:
                            rotate_flag = not rotate_flag
                            inside_flag = True
                    else:
                        inside_flag = False
                    
                    break 

        display_frame = frame.copy()
        if rotate_flag:
            display_frame = cv2.rotate(display_frame, cv2.ROTATE_180)

        cv2.imshow('AR Fly Detector', display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_processing()