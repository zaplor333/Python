import os
import cv2
import numpy as np
import pyautogui
import keyboard
import datetime

# Global variables
recording = False
paused = False
out = None
frames = []

def get_desktop_directory():
    home = os.path.expanduser('~')
    desktop = os.path.join(home, 'OneDrive','Desktop')
    return desktop

def create_recording_folder():
    desktop_dir = get_desktop_directory()
    today_date = datetime.datetime.now().strftime("%d%B%Y")
    date_folder = os.path.join(desktop_dir, today_date)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)
    return date_folder

def start_recording():
    global recording, out, frames, paused
    if not recording:
        recording = True
        paused = False
        frames = []
        date_folder = create_recording_folder() # or not
        current_time = datetime.datetime.now().strftime("%HH-%MM-%SS")
        filename = f"{os.path.join(date_folder, current_time)}.avi"
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename, fourcc, 20.0, screen_size)
        print(f"Recording started: {filename}")

def pause_recording():
    global paused
    if recording and not paused:
        paused = True
        print("Recording paused")

def resume_recording():
    global paused
    if recording and paused:
        paused = False
        print("Recording resumed")

def stop_and_save_recording():
    global recording, out, frames
    if recording:
        recording = False
        out.release()
        for frame in frames:
            out.write(frame)
        print("Recording saved and stopped")

def capture_screen():
    global frames
    while True:
        if recording and not paused:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        if keyboard.is_pressed('f4'):
            stop_and_save_recording()
            break

# Hook the function keys to the respective functions
keyboard.add_hotkey('f1', start_recording)
keyboard.add_hotkey('f2', pause_recording)
keyboard.add_hotkey('f3', resume_recording)
keyboard.add_hotkey('f4', stop_and_save_recording)

print("Press F1 to start recording, F2 to pause, F3 to resume, F4 to save and stop.")

# Run the screen capture loop
capture_screen()
