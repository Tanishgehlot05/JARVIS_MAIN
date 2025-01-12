# SkyNet: AI Desktop Assistant

SkyNet is an advanced AI desktop assistant developed as part of the General Championship ML Hackathon. This assistant provides a wide range of functionalities like natural language interactions, file system operations, application control, weather updates, news fetching, and task automation.

## Features

- **Text-Based Interaction:** Responds to user input in a natural way, handles context, and executes multi-step commands.
- **File System Operations:** Can create, read, update, and delete files, as well as manage file paths.
- **Application Control:** Open or close applications such as Notepad, Chrome, and many more.
- **System Settings Management:** Can adjust settings such as volume or brightness.
- **Multimodal Interaction:** Supports basic gesture-based commands and webcam input.
- **Task Automation:** Automate tasks by running custom scripts, scheduling reminders, and more.
- **Real-Time Data Fetching:** Fetch stock prices, weather, and news from APIs.
- **Speech-to-Text and Text-to-Speech:** Speech input and output for hands-free interaction.

## Requirements

To run SkyNet, the following libraries must be installed:

- `tkinter`: For the graphical interface.
- `sounddevice`: For audio recording.
- `PIL` (Pillow): For image handling.
- `whisper`: For speech-to-text functionality.
- `pyttsx3`: For text-to-speech functionality.
- `google.generativeai`: For advanced natural language processing.
- `requests`: For fetching weather, news, and stock data.

You can install them using pip:

```bash
pip install tkinter sounddevice pillow whisper pyttsx3 google-generativeai requests
```
## Setup
-API Key: Before running SkyNet, you must configure your API keys.
-Place your API key in a file named SkyNet_base_api.txt in the same directory as this script.
-Whisper Model: SkyNet uses the Whisper model for speech-to-text. Ensure the model is correctly loaded with whisper.load_model("base").

## Usage
-Speech-to-Text and Text-to-Speech
-SkyNet can transcribe speech to text and read text aloud using the following functions:
 -speech_to_text(): Transcribes recorded speech into text. 
 -text_to_speech(text): Converts text into speech.

## File Operations
-SkyNet can interact with files, including:
 -create: Create new files.
 -read: Read content from files.
 -update: Append content to files.
  -delete: Remove files.

## Configuration
-Gemini Model Configuration
-The assistant is powered by Google's Gemini model for text-based interactions. The configuration options include temperature, top_p, and other parameters for customizing the generation behavior.

## SkyNet can open and close applications such as:
-Chrome
-Notepad
-Calculator
-Word
-Excel
-Paint
-Command Prompt
-Real-Time Operations
-Weather: Fetch the current weather for a specified city.
-News: Retrieve the latest headlines.
-Stock Prices: Fetch real-time stock prices.

## Example Commands
### File Operations: "Create a new file named 'test.txt'."
### Application Control: "Open Chrome."
### Weather: "What is the weather in Mumbai?"
### News: "Tell me the latest news."
### Stock Prices: "What is the stock price of Apple?"
### Handling Errors
-SkyNet provides robust error handling for file operations and network requests. It ensures that actions are reversible, file paths are confirmed, and feedback is provided to the user.

## Developer Guide
-Developed by: Dedeep.v., Tanish Jain, Tanish Kumar, Kapil Mulay.
-Customizable for developers using fine-tuned prompts and large datasets.
-For maintenance or feature requests, refer to the project's documentation or contact the original development team.

## Acknowledgments
-This project was developed for the General Championship ML Hackathon and aims to showcase advanced AI capabilities for desktop interactions.

## Error Handling
-The assistant provides helpful feedback in case of errors, such as missing files, API issues, or incorrect commands.

## License
-This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
-If you would like to contribute to the development of SkyNet, feel free to submit a pull request. Please ensure your code is well-documented and follows the project's coding standards.
