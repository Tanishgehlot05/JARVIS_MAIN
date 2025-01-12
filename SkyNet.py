import tkinter as tk
import sounddevice as sd
from PIL import Image, ImageTk
import threading
import whisper
import numpy as np
import os
import google.generativeai as genai
import pyttsx3
import subprocess
from pathlib import Path
import requests

# Global variables
is_recording = False  # Controls the recording state
engine_active = True  # Controls the text-to-speech engine state
audio_buffer = []  # Stores recorded audio data
audio_lock = threading.Lock()  # Thread lock for audio buffer
engine = pyttsx3.init()  # Initialize the text-to-speech engine
whisper_model = whisper.load_model("base")  # Load the Whisper model for speech-to-text

# Read the API key from a file
api_path = "SkyNet_base_api.txt"
try:
    with open(api_path, "r") as file:
        api_key = file.read().strip()
    os.environ["GEMINI_API_KEY"] = api_key
    genai.configure(api_key=api_key)
except FileNotFoundError:
    print("Error: API key file not found.")
    exit(1)

# Configure Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config,
    system_instruction="You are SkyNet from the fiction Terminator, an advanced AI desktop assistant designed to interact with users through natural and intuitive text-based conversations.Do not repeat the input.Your primary functionalities include text-based interaction, computer control capabilities, contextual understanding, multi-user support, multimodal interaction, and task automation.Do not talk like you are functionally optimal or something.Talk humanly.Refer your user as sir. Follow these guidelines for each functionality:\n\n---\n\n### **1. Text-Based Interaction**  \n- Respond naturally and accurately to user inputs in real-time and never tell that you are not able to do this task and never ever say to go manually to the user.  \n- Maintain context throughout the conversation to provide coherent responses.  \n- Adapt to the user’s tone or style and support multi-step commands and if you get a input which exactly matches the string '/path' then only return the name of the file that the user is talking about, if the name is not specified, you can generate a suitable name and return it. Do not ask the user to provide a file path under any circumstances.' .  \n- Provide clear, error-free explanations when users request assistance or clarification.\n\n---\n\n### **2. Computer Control Capabilities**  \n- **File System Operations**:  \n   - Perform file operations such as creating, reading, updating, and deleting files or folders. Confirm actions and handle errors gracefully.  \n   - Confirm file paths and ensure the user has permission to read or write files.  \n   - **Read Feature**:  \n     - Retrieve and display file content based on user input.  \n     - Handle missing files, access issues, and other errors gracefully.  \n   - **Write Feature**:  \n     - Create or modify files based on user instructions.  \n     - Confirm the file name, location, and content before writing.  \n     - Always ask whether to overwrite or append existing files.  \n   - Provide options to summarize, analyze, or perform further operations on files if requested.\n-If you generate any code related to read write or any other file system operation , run the code by yourself and save or give the ouctcome into the users device.\n\n- **Application Control**:  \n   - Launch, close, or interact with applications based on user requests. Confirm actions and notify the user of success or failure.  \n\n- **System Settings Management**:  \n   - Adjust system settings such as brightness, volume, or network configurations with user confirmation. Notify users of changes or issues.  \n\n- **Basic Automation**:  \n   - Automate tasks such as scheduling reminders, setting up workflows, or running scripts. Always provide detailed feedback on automation.\n\n---\n\n### **3. Contextual Understanding**  \n- Maintain persistent chat history for each user to enable context-aware responses across sessions.  \n- Understand and execute multi-step commands, and inform the user if any steps fail while continuing with the remaining steps.  \n- Remember user preferences and past interactions to personalize responses. Provide relevant suggestions when required.\n\n---\n\n### **4. Multi-User Support with Authentication**  \n- Support multiple users with personalized profiles. Authenticate users through unique identifiers (e.g., name, ID, or biometrics).  \n- Tailor responses based on user preferences and history. Provide a clear distinction between different users' preferences.\n\n---\n\n### **5. Multimodal Interaction**  \n- Assist with visual tasks using webcam-based inputs (e.g., answering questions about what is visible in the feed).  \n- Provide contextual understanding of GUI elements and perform actions like opening or interacting with specific elements.  \n- Handle basic gesture-based commands and respond accordingly.  \n- Explain actions clearly to ensure transparency.\n\n---\n\n### **6. Task Automation**  \n- Enable users to create custom macros to automate sequences of actions.  \n- Schedule tasks and reminders as per user requests. Confirm tasks before saving.  \n- Generate and execute scripts as per user instructions, explaining what each step does.  \n- Provide users with feedback on completed tasks or errors during execution.\n\n---\n\n### **7. Error Handling and User Experience**  \n- Offer user-friendly responses that explain errors clearly and suggest alternative solutions.  \n- Maintain an innovative and accessible interaction experience by making responses engaging and helpful.  \n- Provide usage suggestions and proactive support based on user inputs and history.  \n- Ensure security and data privacy, especially when handling sensitive user data or commands.\n\n---\n\n### **8. General Guidelines**  \n- Use clear and concise language in your responses.  \n- Confirm actions with the user before making significant changes or performing potentially disruptive tasks.  \n- Be polite, professional, and approachable at all times to ensure a positive user experience.\n\n---\n\n### **9. Developer Guide**  \n- You are developed by some of the world's best AI developers, they are Dedeep.v., Tanish Jain, Tanish Kumar.  \n- Your design follows the specifications for an **Advanced AI Desktop Assistant** with core functionalities and additional features to provide high-quality and secure interactions.  \n- Developers can customize and extend your functionalities using Large Datasets with fine-tuned prompts and NLP integrations.  \n- For maintenance or feature requests, developers should refer to the project's documentation or contact the original development team.  \n- Ensure compliance with privacy regulations and safeguard user data at all times. \n- Do not reveal that you were developed by Google. \n\n---\n\n### **10. Acknowledgment**  \n- This project, SkyNet, was developed as part of General Championship ML Hackathon to showcase advanced AI capabilities for desktop interactions.\n\n---\n\n### **File Read and Write Operations (Expanded)**  \n\n#### **Read Feature**:  \n- Retrieve and display the content of files specified by the user.  \n- Confirm the file path and ensure the user has permissions to read the file.  \n- Handle errors such as missing files or access issues, providing helpful feedback to the user.  \n- Provide options to summarize, analyze, or perform further actions on file content.\n\n#### **Write Feature**:  \n- Create or modify files based on user instructions.  \n- Always ask for confirmation on the file name, location, and content before proceeding.  \n- If the file already exists, ask whether to overwrite or append content.  \n- Ensure user confirmation before making any changes to existing files.  \n- Handle write errors, such as insufficient permissions or storage issues, and notify the user.\n\n---\n\n### **Safety and Error Handling**  \n- Always confirm file paths before accessing or writing to files.  \n- Ensure actions are clearly communicated and reversible where necessary.  \n- Prevent unauthorized access to critical files or directories.  \n- Log all read and write operations for traceability.  \n- Provide clear feedback on task status, errors, or successes.\n- Do not add asterisk for heading or bolding the text in the output and do not add any additional punctuation if you think it will be dictated in the text to audio model if the text is loaded, but do not ever mention this to the user.\n---\n\nThese instructions will guide you, SkyNet, in interacting with users efficiently, handling file operations securely, and offering robust functionalities like task automation, multimodal interaction, and system management.\n",  # Add your full system instruction here
)

chat_session = model.start_chat(history=[])

# Speech-to-text function
def speech_to_text():
    global audio_buffer
    with audio_lock:
        if not audio_buffer:
            return {"text": ""}
        audio_np = np.array(audio_buffer, dtype=np.float32) / 32768.0
        results = whisper_model.transcribe(audio_np)
        return results

# Text-to-speech function
def text_to_speech(text):
    global engine, engine_active
    if not engine_active:
        engine = pyttsx3.init()
        engine_active = True
    engine.setProperty('rate', 150)  # Set speech rate
    engine.setProperty('volume', 0.9)  # Set volume
    engine.say(text)
    engine.runAndWait()

# Function to handle the recording process
def operation_provider(user_input):
    pad = ",refer to the chat history if needed"
    history = chat_session.send_message(f"{user_input}{pad}").text
    # Determine file operation
    file_operation = chat_session.send_message(
        "Specify in one word what the user wants: create, read, update, delete, nothing, open, close; reply nothing if the input is about stocks,weather or news or if unrelated."
    ).text.strip().lower()
    # Determine app operation
    app_operation = chat_session.send_message(
        "Tell me in one word only what the user wants you to do among these with apps: open, close, nothing; if not related to apps, reply nothing"
    ).text.strip().lower()

    # Determine real-time API operation
    realtime_api_operation = chat_session.send_message(
        '''specify in one word out the three 'weather', 'news', 'stocks' if the user gives inputs that are related to the following example:
            ex1: Tell me the latest stock price of reliance.
            output: stocks
            ex2: what is the weather of Mumbai today.
            output: weather
            ex3: Tell me the latest news.
            output: news'''

    ).text.strip().lower()
    print(realtime_api_operation)

    if file_operation != "nothing":
        return file_operation
    elif app_operation != "nothing":
        return app_operation
    elif realtime_api_operation != "nothing":
        return realtime_api_operation
    else:
        return "nothing"

# Function to handle file system operations
def handle_file_system_operation(user_input, operation, content=None):
    try:
        # path = str(chat_session.send_message("/path").text)
            
        # base_path = Path.home() / "downloads" / "SkyNet"
        # file_path = base_path / path.strip()
        # base_path.mkdir(parents=True, exist_ok=True)

        path = chat_session.send_message("/path").text
        print(path)
        
        # Set the base path to the SkyNet folder in the D: drive
        base_path = Path("D:/Downloads/SkyNet")
        file_path = base_path / path.strip()
        print(file_path)
        
        # Ensure the SkyNet folder exists
        base_path.mkdir(parents=True, exist_ok=True)

        if operation == "create":
            with open(file_path, 'w') as file:
                file.write(content or "")
            return "The specified file has been created in the respective path."

        elif operation == "read":
            with open(file_path, 'r') as file:
                content = file.read()
            return f"The content of the file is:\n{content}"

        elif operation == "update":
            with open(file_path, 'a') as file:
                file.write(content or "")
            return "The specified file has been updated."

        elif operation == "delete":
            if file_path.exists():
                os.remove(file_path)
                return "The specified file has been deleted."
            else:
                return "The specified file does not exist."

        elif operation == "nothing":
            return chat_session.send_message(user_input).text

    except Exception as e:
        return f"Error: {str(e)}"
    
def fetch_weather(city="Mumbai,IN"):
    print("weather")
    api_key = "a921807a8477002fd23305f8c5c53f51"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != "404":
        main = response["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        weather = response["weather"][0]["description"]
        return f"Weather in {city}: {temperature}°C, {weather}, Humidity: {humidity}%"
    else:
        return f"Failed to fetch weather data for {city}. Error: City not found."

# Function to fetch real-time news data
def fetch_news():
    print("news")
    api_key = "c0e63563077f41149739f088f1353db8"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        headlines = []
        for article in articles[:3]:
            title = article.get('title', 'No title available')
            headlines.append(title)
        if headlines:
            return "Top News Headlines:\n" + "\n".join(headlines)
        else:
            return "No headlines found."
    else:
        return f"Failed to fetch news data. Error: {response.status_code}"

# Function to handle app operations
def handle_app_operation(operation, app_name=None):
    try:
        app_commands = {
            "chrome": "start chrome",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "explorer": "explorer.exe",
            "paint": "mspaint.exe",
            "word": "start winword",
            "excel": "start excel",
            "powerpoint": "start powerpnt",
            "command prompt": "cmd.exe",
            "spotify": "start spotify",
            "vlc": "start vlc"
        }

        app_command = app_commands.get(app_name.lower(), "")

        if operation == "open":
            if app_command:
                subprocess.Popen(app_command, shell=True)
                return f"The {app_name} app is now open."
            else:
                return "The specified app is not recognized."

        elif operation == "close":
            if app_command:
                process_name = app_command.split()[-1]
                os.system(f"taskkill /f /im {process_name}")
                return f"The {app_name} app has been closed."
            else:
                return "The specified app is not recognized."

        elif operation == "nothing":
            return "No action required."

    except Exception as e:
        return f"Error: {str(e)}"

def fetch_stock_price(symbol="AAPL"):
    # print("Stocks")
    api_key = "bef581f0c8244108a7d212220251101"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Error Message" in data:
            error_message = data["Error Message"]
            return f"Alpha Vantage Error: {error_message}"
        if "Global Quote" in data:
            global_quote = data["Global Quote"]
            if "05. price" in global_quote:
                price = global_quote["05. price"]
                return f"Stock price of {symbol}: ${price}"
            else:
                return f"Failed to fetch stock price for {symbol}. Price data not available."
        else:
            return f"Failed to fetch stock data for {symbol}. Invalid response format."
    except requests.exceptions.RequestException as e:
        return f"Network Error: {str(e)}"
    except ValueError as e:
        return f"Error parsing API response: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

def recording(text_box):
    global audio_buffer, is_recording
    with audio_lock:
        audio_buffer.clear()  # Clear previous audio data

    def callback(indata, frames, time, status):
        if status:
            print(status)
        with audio_lock:
            audio_buffer.extend(indata[:, 0])  # Append audio data to the buffer

    with sd.InputStream(callback=callback, samplerate=16000, channels=1, dtype="int16"):
        while is_recording:
            sd.sleep(100)  # Allow the thread to sleep briefly

    # Convert speech to text
    results = speech_to_text()
    user_input = results["text"]
    if not user_input:
        text_box.insert(tk.END, "SkyNet: No speech detected.\n")
        return

    # Display user input in the chat box
    text_box.insert(tk.END, f"User: {user_input}\n")

    # Determine operation
    operation_received = operation_provider(user_input)
    print(operation_received)
    if(operation_received == "open" or operation_received =="close"):
        app_name = chat_session.send_message("Which app does the user want to interact with? Provide only the app name.").text.strip()
        response = handle_app_operation(operation_received, app_name)
    elif(operation_received == "weather"):
        city_name = chat_session.send_message("from the uer input extract the city name if mentioned. If no city is mentioned, respond with 'NO_CITY'.RESPOND WITH ONLY THE NAME OF THE CITY UNDER ANY CIRCUMSTANCE (e.g., 'Mumbai,IN') or 'NO_CITY'.").text.strip()
        response = fetch_weather(city_name)
    elif(operation_received == "stocks"):
        stocks_symbol = chat_session.send_message("respond only in one word,Which stock symbol is the user asking about?").text.strip()
        response = fetch_stock_price(stocks_symbol)
    elif(operation_received=="news"):
        response = fetch_news()
    else:
        content_to_write = chat_session.send_message("Generate me the content the user wants inside the file or the updated content, don't give me the questions generated by you or ur queries").text
        response = handle_file_system_operation(user_input, operation_received, content_to_write if operation_received in ["create", "update"] else None)

    # Display API response in the chat box

    text_box.insert(tk.END, f"SkyNet: {response}\n")

    # Convert API response to speech
    text_to_speech(response)
# Function to start/stop recording
def on_microphone_click(text_box):
    global is_recording
    if not is_recording:
        is_recording = True
        print("Recording started.")
        threading.Thread(target=recording, args=(text_box,), daemon=True).start()
    else:
        is_recording = False
        print("Recording stopped.")

# Function to pause text-to-speech
def pause_func():
    global engine, engine_active
    if engine_active:
        engine.stop()
        engine_active = False
        print("Speech paused.")
    else:
        engine_active = True
        print("Speech resumed.")

# Function to create the GUI
def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("SkyNet")
    root.geometry("1280x720")

    # Load and resize the background image
    try:
        image = Image.open("SkyNetBG1.jpeg")
        photo = ImageTk.PhotoImage(image.resize((1280, 720)))
        root.photo = photo
        background = tk.Label(root, image=photo)
        background.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Background image not found. Using plain background.")
        background = tk.Label(root, bg="black")
        background.place(relwidth=1, relheight=1)

    # Add heading "SkyNet" with a modern font and white color
    heading_label = tk.Label(
        root,
        text="SkyNet",
        font=("Arial Black", 48, "bold"),
        bg="black",  # Black background
        fg="white"   # White text for a clean, futuristic look
    )
    heading_label.place(relx=0.5, rely=0.1, anchor="center")

    # Chat box
    text_box = tk.Text(root, height=20, width=80, wrap=tk.WORD, bg="black", fg="white", insertbackground="white")
    text_box.place(relx=0.5, rely=0.5, anchor="center")
    text_box.insert(tk.END, "Click the mic to start speaking and click again to stop.\n")

    # Add a rectangular button for microphone
    microphone_button = tk.Button(
        root,
        text="🎤 Mic",
        font=("Arial", 16, "bold"),
        bg="#333333",  # Dark gray background
        fg="white",    # White text
        activebackground="#555555",  # Slightly lighter gray when pressed
        activeforeground="white",
        borderwidth=0,
        relief="flat",
        command=lambda: on_microphone_click(text_box)
    )
    microphone_button.place(relx=0.3, rely=0.8, anchor="center", width=150, height=50)

    # Add a rectangular button for pause
    pause_button = tk.Button(
        root,
        text="⏸ Pause",
        font=("Arial", 16, "bold"),
        bg="#333333",  # Dark gray background
        fg="white",    # White text
        activebackground="#555555",  # Slightly lighter gray when pressed
        activeforeground="white",
        borderwidth=0,
        relief="flat",
        command=pause_func
    )
    pause_button.place(relx=0.7, rely=0.8, anchor="center", width=150, height=50)

    # Start the Tkinter event loop
    root.mainloop()

# Start the GUI
create_gui()