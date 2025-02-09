# XTTS Text-to-Speech WebUI 🎤✨

Welcome to the XTTS Text-to-Speech WebUI project! This project leverages a Gradio-based user interface and the state-of-the-art XTTS (Coqui TTS v2) model to generate high-quality, natural-sounding speech from text. The app is designed to work locally with GPU acceleration (via CUDA) when available, making text-to-speech conversion fast and efficient. 🚀

---

## Overview

This project provides:
- **Real-Time Speech Generation**: Convert text into speech using an advanced TTS model.
- **Multi-Language Support**: Choose from a variety of languages including English, Spanish, French, German, Italian, Portuguese, Polish, Turkish, Russian, Dutch, Czech, Arabic, and Chinese (Simplified). 🌐
- **Gradio Web Interface**: Enjoy an interactive UI with easy-to-use controls and examples for quick testing.
- **CUDA/GPU Support**: Automatically utilizes GPU for faster processing when available. ⚡
- **Robust Error Handling**: Clear error messages guide you in case of issues during speech generation.

The core functionality is implemented in the `app.py` file where the TTS model is initialized and integrated into the Gradio interface.

---

## Features

- **Interactive WebUI**: Developed using [Gradio](https://gradio.app/), the interface allows users to:
  - Input text
  - Select a language for speech synthesis
  - Generate and listen to the synthesized audio instantly
- **XTTS Model Integration**: Utilizes the XTTS (Coqui TTS v2) model for natural and expressive speech output.
- **Example Usage**: Predefined examples help you quickly see how the system works:
  - "Hello, this is a test of the XTTS text to speech system." (English)
  - "Bonjour, ceci est un test du système de synthèse vocale XTTS." (French)
  - "Hola, esta es una prueba del sistema de texto a voz XTTS." (Spanish)
- **Error Handling**: Provides user-friendly error messages if speech generation fails. 🔧

---

## Installation & Setup

Follow these steps to install and run the Gradio WebUI:

1. **Prerequisites**:
   - Python 3.8+ installed on your system.
   - [PyTorch](https://pytorch.org/) with CUDA support for GPU acceleration (if available).
   - [Gradio](https://gradio.app/) for the web interface.
   - [Coqui TTS](https://github.com/coqui-ai/TTS) dependencies.
   - FFmpeg (required for audio processing) installed and available in your system path.

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   ```

3. **Install Dependencies**:
   Install the required Python packages. You can install them using the requirements file provided:
   ```bash
   pip install -r requirements.txt
   ```

4. **Running the Application**:
   - **Via Command Line**:
     ```bash
     python app.py
     ```
   - **Using the Provided Batch Script**:
     Double-click on `run-gradio.bat` or run it from the command line:
     ```bash
     run-gradio.bat
     ```

5. **Accessing the Web Interface**:
   Once the application is running, open your browser and navigate to:
   ```
   http://0.0.0.0:7860
   ```
   Enjoy the interactive TTS experience! 🎉

---

## Project Plan & Future Enhancements

Based on the project's implementation plan:
- **Current Focus**: Establishing a robust TTS pipeline with a clean and responsive user interface.
- **Future Enhancements**:
  - Improved GPU memory optimization.
  - Caching mechanisms for frequent requests.
  - Batch processing and voice preset management.
  - Expanded voice customization features and additional language support.

For a detailed insight into the project approach, refer to the [plan.md](plan.md) file.

---

## Troubleshooting & Support

- Ensure all prerequisites are met and dependencies are correctly installed.
- For GPU acceleration, verify that your system has the necessary NVIDIA GPU with CUDA support.
- If you encounter issues, check the console for clear error messages and tracebacks.

Happy TTS'ing! 🎙️💬
