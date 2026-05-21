import pygame
import sys
import os

# --- INITIAL SETUP ---
pygame.init()
WIDTH, HEIGHT = 1100, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KAI - AI Assistant")
clock = pygame.time.Clock()

# --- COLORS ---
USER_BUBBLE_COLOR = (0, 120, 215) 
KAI_BUBBLE_COLOR = (240, 240, 240) 
USER_TEXT_COLOR = (255, 255, 255) 
KAI_TEXT_COLOR = (40, 40, 40)     

# --- GLOBAL CONTROL VARIABLES ---
current_kai_status = "login" 
current_frame_idx = 0
gui_chat_history = [] 
login_complete = False 

# --- 1. ANIMATION LOADER FUNCTION ---
def load_animation_frames(folder_name):
    path = f"assets/frames/{folder_name}/"
    frames = []
    if os.path.exists(path):
        files = sorted([f for f in os.listdir(path) if f.endswith('.png')])
        for f in files:
            try:
                img = pygame.image.load(os.path.join(path, f)).convert_alpha()
                img = pygame.transform.scale(img, (500, 500))
                frames.append(img)
            except:
                continue
    return frames

# --- 2. LOAD ALL ASSETS ---
try:
    bg = pygame.image.load("assets/background.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
except Exception as e:
    bg = None

animations = {
    "sleep": load_animation_frames("sleep"),
    "talking": load_animation_frames("talking"),
    "listening": load_animation_frames("listening"),
    "login": load_animation_frames("login"),
    "logout": load_animation_frames("logout"),
    "wakeup": load_animation_frames("wakeup")
}

try:
    default_avatar = pygame.image.load("assets/kai_avatar.png").convert_alpha()
    default_avatar = pygame.transform.scale(default_avatar, (370, 290))
except:
    default_avatar = pygame.Surface((370, 290), pygame.SRCALPHA)

font = pygame.font.SysFont("Trebuchet MS", 18)

# --- 3. HELPER FUNCTIONS ---
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        w, _ = font.size(test_line)
        if w < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

def draw_bubble(text, y, sender="kai"):
    MAX_BUBBLE_WIDTH = 450
    PADDING = 15
    line_height = font.get_linesize()
    wrapped_lines = wrap_text(text, font, MAX_BUBBLE_WIDTH - (2 * PADDING))
    max_line_w = 0
    for line in wrapped_lines:
        w, _ = font.size(line)
        max_line_w = max(max_line_w, w)
    total_bubble_width = max_line_w + (2 * PADDING)
    total_bubble_height = (len(wrapped_lines) * line_height) + (2 * PADDING)
    
    if sender == "user":
        x = WIDTH - total_bubble_width - 50
        color = USER_BUBBLE_COLOR
        text_color = USER_TEXT_COLOR
    else:
        x = 600 
        color = KAI_BUBBLE_COLOR
        text_color = KAI_TEXT_COLOR

    pygame.draw.rect(screen, color, (x, y, total_bubble_width, total_bubble_height), border_radius=15)
    current_line_y = y + PADDING
    for line in wrapped_lines:
        txt_surface = font.render(line, True, text_color)
        screen.blit(txt_surface, (x + PADDING, current_line_y))
        current_line_y += line_height + 5
    return total_bubble_height + 15

# --- 4. DRAW WINDOW ---
def draw_window():
    global current_frame_idx, current_kai_status, login_complete
    
    if bg:
        screen.blit(bg, (0, 0))
    else:
        screen.fill((30, 30, 30))

    # --- STATUS LOCK LOGIC ---
    if not login_complete:
        current_kai_status = "login"

    anim_list = animations.get(current_kai_status.lower(), [])
    
    if anim_list:
        # --- SEPARATE SPEED ADJUSTMENT ---
        animation_speeds = {
            "login": 0.35,      
            "sleep": 0.1,      
            "talking": 0.10,    
            "listening": 0.08,  
            "wakeup": 0.12,     
            "logout": 0.35      
        }
        
        # 1. Speed uthana
        speed = animation_speeds.get(current_kai_status.lower(), 0.08)
        
        # 2. Frame index ko aage badhana (YE LINE MISSING THI)
        current_frame_idx += speed
        
        # 3. Loop logic aur Status switch
        if current_frame_idx >= len(anim_list):
            if current_kai_status == "login":
                login_complete = True
                current_kai_status = "listening"
            current_frame_idx = 0
            
        frame = anim_list[int(current_frame_idx)]
        screen.blit(frame, (120, 150))
    else:
        screen.blit(default_avatar, (365, 310))
    
    status_txt = font.render(f"Mode: {current_kai_status.upper()}", True, (200, 0, 200))
    screen.blit(status_txt, (10, 600))
    
    current_y = 80
    for line in gui_chat_history[-5:]:
        if line.startswith("Alok:"):
            msg = line.replace("Alok:", "").strip()
            h = draw_bubble(msg, current_y, sender="user")
        elif line.startswith("Kai:"):
            msg = line.replace("Kai:", "").strip()
            h = draw_bubble(msg, current_y, sender="kai")
        current_y += h

    pygame.display.flip()

# --- 5. MAIN LOOP ---
def main_gui_loop():
    while True:
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_window()

if __name__ == "__main__":
    gui_chat_history = ["Kai: Initializing... System Online."]
    main_gui_loop()