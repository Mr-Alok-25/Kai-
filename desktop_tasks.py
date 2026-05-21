# import win32gui
# import win32con

# def minimize_specific_window(window_name="Visual Studio Code"):
#     """
#     Specific window ko dhoond kar minimize karta hai.
#     window_name: Window ke title ka ek hissa (e.g., 'Visual Studio Code' ya 'Chrome')
#     """
#     def callback(hwnd, extra):
#         title = win32gui.GetWindowText(hwnd)
#         # Check kar raha hai ki kya window ke title mein hamara target name hai
#         if window_name.lower() in title.lower():
#             win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
#             print(f"Target found and minimized: {title}")
#             return False # Mil gaya toh search stop kar do
#         return True

#     try:
#         win32gui.EnumWindows(callback, None)
#     except:
#         # Callback stop hone par exception throw karta hai, use ignore karein
#         pass