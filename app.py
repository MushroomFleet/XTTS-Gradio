import gradio as gr
import torch
import numpy as np
from TTS.api import TTS

def initialize_tts():
    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Initialize TTS with XTTS model
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    return tts

def generate_speech(text, language="en"):
    """Generate speech from text using XTTS"""
    try:
        # Get TTS instance (initialized once and cached)
        tts = initialize_tts()
        
        # Generate speech with speaker if available
        if hasattr(tts, "speakers") and tts.speakers:
            default_speaker = tts.speakers[0]
            wav = tts.tts(text=text, language=language, speaker=default_speaker)
        else:
            wav = tts.tts(text=text, language=language)
        
        wav = np.array(wav, dtype=np.float32)
        return (22050, wav)  # Return sample rate and audio
    except Exception as e:
        raise gr.Error(f"Error generating speech: {str(e)}")

# Create Gradio interface
def create_ui():
    with gr.Blocks(title="XTTS Text-to-Speech") as app:
        gr.Markdown("# XTTS Text-to-Speech")
        
        with gr.Row():
            with gr.Column():
                # Input components
                text_input = gr.Textbox(
                    label="Text to speak",
                    placeholder="Enter the text you want to convert to speech...",
                    lines=5
                )
                
                language = gr.Dropdown(
                    choices=["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn"],
                    value="en",
                    label="Language"
                )
                
                generate_btn = gr.Button("Generate Speech", variant="primary")
            
            with gr.Column():
                # Output components
                audio_output = gr.Audio(
                    label="Generated Speech",
                    type="numpy"
                )
                
        # Handle generation
        generate_btn.click(
            fn=generate_speech,
            inputs=[text_input, language],
            outputs=audio_output
        )
        
        # Examples
        gr.Examples(
            examples=[
                ["Hello, this is a test of the XTTS text to speech system.", "en"],
                ["Bonjour, ceci est un test du système de synthèse vocale XTTS.", "fr"],
                ["Hola, esta es una prueba del sistema de texto a voz XTTS.", "es"]
            ],
            inputs=[text_input, language]
        )
        
    return app

if __name__ == "__main__":
    # Create and launch the UI
    app = create_ui()
    app.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )
