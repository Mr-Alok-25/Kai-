import cv2
import os
import numpy as np
import sys

def build_frames(folder_name):
    base_path = "assets/frames/"
    folder_path = os.path.join(base_path, folder_name)
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_name}' nahi mila!")
        return
    
    # Video file dhoondhna
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mov', '.mp4'))]
    if not video_files:
        print(f"Error: '{folder_name}' mein koi video file nahi hai!")
        return
        
    video_path = os.path.join(folder_path, video_files[0])
    print(f"\n--- Starting Frame Generation for: {folder_name} ---")
    print(f"Video Source: {video_path}")

    cap = cv2.VideoCapture(video_path)
    
    # Purane frames delete karna taaki confusion na ho
    print("Cleaning old frames...")
    for f in os.listdir(folder_path):
        if f.endswith(".png"):
            os.remove(os.path.join(folder_path, f))

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 1. BGR se HSV (Green Screen detection ke liye)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 2. Green Range (Adjustable)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.medianBlur(mask, 3) # Edges smooth karne ke liye
        mask_inv = cv2.bitwise_not(mask)
        
        # 3. BGRA (Transparency)
        b, g, r = cv2.split(frame)
        final_rgba = cv2.merge([b, g, r, mask_inv])
        
        # 4. Save PNG
        file_name = os.path.join(folder_path, f"{count:03d}.png")
        cv2.imwrite(file_name, final_rgba)
        
        count += 1
        print(f"Generated Frame: {count}", end="\r")
        
    cap.release()
    print(f"\nSuccess! {count} transparent frames generated in '{folder_name}' folder. 🚀")

if __name__ == "__main__":
    # Agar terminal se naam diya hai (e.g. python frame_builder.py talking)
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
        build_frames(target_folder)
    else:
        # Default testing ke liye agar koi command na di ho
        print("Tip: Aap terminal mein aise command de sakte hain: python frame_builder.py talking")
        choice = input("Kaunse folder ke frames generate karne hain? (talking/listening/sleep/wakeup): ").strip().lower()
        build_frames(choice)