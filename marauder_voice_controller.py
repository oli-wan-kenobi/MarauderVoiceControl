import os
import speech_recognition as sr
import time
import ctypes
import platform
import threading
import pyautogui

MIC_INDEX = 1
WAKE_UP_PHRASE = "I solemnly swear I am up to no good"
SLEEP_PHRASE = "mischief managed"

# Global stop event to signal threads to stop
stop_event = threading.Event()


def turn_off_screen():
    """Turns off the display but keeps the computer running."""
    global listener_thread  # Keep track of the listener thread

    system = platform.system()
    if system == "Windows":
        os.system("rundll32.exe user32.dll, LockWorkStation")  # Locks the PC, turning off the screen
        print("The screen is off!")
    elif system == "Linux":
        os.system("xset dpms force off")  # Turns off screen on Linux
    elif system == "Darwin":  # macOS
        os.system("pmset displaysleepnow")  # Turns off screen on Mac

    # Reset stop event and start listening for commands
    stop_event.clear()
    # Check if the listener thread is still running, start only if needed
    if not listener_thread.is_alive():
        listener_thread = threading.Thread(target=listen_for_commands)
        listener_thread.start()


def turn_on_screen():
    """Wakes up the display and stops all threads."""
    try:
        system = platform.system()
        if system == "Windows":
            print("The screen is on!")
            ctypes.windll.user32.mouse_event(1, 0, 0, 0, 0)  # Simulate a tiny mouse move
            pyautogui.moveTo(100, 100)  # Move the mouse to a safe position
            pyautogui.hotkey('ctrl', 'alt', 'delete')
        elif system == "Linux":
            os.system("xset dpms force on")  # Wake screen for Linux
        elif system == "Darwin":  # macOS
            os.system("caffeinate -u -t 1")  # Wake screen on Mac
    except pyautogui.FailSafeException:
        print("Fail-safe exception raised. Ignoring...")


def recognize_speech():
    recognizer = sr.Recognizer()

    #------------------ Uncomment this block to list available microphones ------------------
    # microphones = sr.Microphone.list_microphone_names()
    # print("Available microphones:")
    # for i, mic_name in enumerate(microphones):
    #     print(f"{i}: {mic_name}")
    #---------------------------------------------------------------------------------------

    with sr.Microphone(device_index=MIC_INDEX) as source:
        print("Listening for magic words...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=50, phrase_time_limit=50)
            command = recognizer.recognize_google(audio).lower()
            # print(f"Command recognized: {command}") Uncomment to see recognized commands in the console
            return command.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Could not request results, check internet connection.")
            return None
        except sr.WaitTimeoutError:
            print("No speech heard.")
            return None


def perform_action(command):
    if command is None:
        return

    if WAKE_UP_PHRASE.lower() in command:
        print("Waking up the display!")
        turn_on_screen()
    elif SLEEP_PHRASE.lower() in command:
        print("Turning off the display...")
        turn_off_screen()


def listen_for_commands():
    """Continuously listens for voice commands in a separate thread."""
    while True:  # Infinite loop to keep it running
        if stop_event.is_set():
            print("Listener thread is stopping...")
            break
        command = recognize_speech()
        if command:
            perform_action(command)
        time.sleep(1)  # Prevents excessive CPU usage
    print("Listener thread has stopped.")


if __name__ == "__main__":
    try:
        # Start listening in a separate thread
        listener_thread = threading.Thread(target=listen_for_commands)
        listener_thread.start()

        # Keep the main script running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected! Stopping threads and exiting...")
        stop_event.set()  # Signal thread to stop
        listener_thread.join()  # Wait for thread to exit cleanly
        print("All threads stopped. Exiting now.")
