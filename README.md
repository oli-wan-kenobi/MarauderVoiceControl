# MarauderVoiceControl

A voice-activated script that locks your computer and unlocks it using speech commands.

## Features
- **Sleep Command:** "Mischief managed" (Locks the screen)
- **Wake-Up Command:** "I solemnly swear I am up to no good" (Unlocks the screen)
- Works on **Windows, macOS, and Linux**

## 🛠 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/oli-wan-kenobi/MarauderVoiceControl.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python marauder_voice_controller.py
   ``` 

## Notes

- Ensure your microphone index named `MIC_INDEX` is set correctly in `marauder_voice_controller.py`.
- The script cannot unlock password-protected screen due to security restrictions.
- In case the microphone does not recognize the voice due to accent issues, try google translate voice.

## Running on Windows 10 with a Virtual Environment
Using a Python virtual environment is recommended to keep dependencies isolated:

    1. Create the python virtual environment:
        ```bash
        python3 -m venv venv
        ```

    2. Activate the virtual environment:
        ```bash
        .\venv\Scripts\activate
        ```

    3. If the virtual environment activation fails with the following error 
        ```bash
        FullyQualifiedErrorId : UnauthorizedAccess
        ```

        Run the followiung command to fix it
        ```bash
        Set-ExecutionPolicy Unrestricted -Scope Process
        ```

    4. Install dependencies and run the script
        ```bash
        pip install -r requirements.txt
        python marauder_voice_controller.py
        ```