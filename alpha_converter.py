import cv2
import os
import numpy as np

# Abhi hum sirf talking folder ko process kar rahe hain
folder_name = 'talking'
base_path = "assets/frames/"

def process_talking_frames():
    folder_path = os.path.join(base_path, folder_name)
    
    if not os.path.exists(folder_path):
        print(f"Error: {folder_path} folder nahi mila!")
        return
    
    # Folder mein video file dhoondhna (.mov ya .mp4)
    files = [f for f in os.listdir(folder_path) if f.endswith(('.mov', '.mp4'))]
    if not files:
        print(f"Error: {folder_name} folder mein koi video nahi mili!")
        return
        
    video_path = os.path.join(folder_path, files[0])
    print(f"Processing Video: {video_path}")

    cap = cv2.VideoCapture(video_path)
    count = 0
    
    # Pehle se maujood purane PNGs delete kar dena behtar hai
    print("Purane frames saaf ho rahe hain...")
    for f in os.listdir(folder_path):
        if f.endswith(".png"):
            os.remove(os.path.join(folder_path, f))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 1. BGR se HSV mein badalna (Green Screen removal ke liye)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 2. Green Color ki Range (Bright Neon Green ke liye)
        # Agar edges par green reh jaye toh lower_green ko [30, 50, 50] karke dekhein
        lower_green = np.array([35, 40, 40]) 
        upper_green = np.array([85, 255, 255])
        
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Mask ko thoda saaf karna (Noise hatane ke liye)
        mask = cv2.medianBlur(mask, 3)
        
        # Mask ko ulta karna (Avatar ko rakhne ke liye)
        mask_inv = cv2.bitwise_not(mask)
        
        # 3. BGRA (Alpha Channel) add karna
        b, g, r = cv2.split(frame)
        rgba = [b, g, r, mask_inv]
        final_frame = cv2.merge(rgba, 4)
        
        # 4. PNG Frame save karna (000.png, 001.png...)
        frame_filename = os.path.join(folder_path, f"{count:03d}.png")
        cv2.imwrite(frame_filename, final_frame)
        
        count += 1
        print(f"Frame {count} saved...", end="\r")
        
    cap.release()
    print(f"\n\nDone! Talking mode ke {count} transparent frames tayyar hain. 🚀")

if __name__ == "__main__":
    process_talking_frames()