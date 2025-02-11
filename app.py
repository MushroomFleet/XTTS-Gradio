import gradio as gr
import torch
import numpy as np
from TTS.api import TTS
import soundfile as sf
import os

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

def generate_cloned_speech(text, language="en", speed=1.0, speaker_file="path_to_speaker_reference.wav", use_gpu=True):
    """Generate cloned speech from text using TTS cloning based on the XTTS model"""
    try:
        # Process speaker_file input: if not a string, assume it's a microphone recording (tuple of sample_rate and numpy array)
        temp_speaker_file = None
        if not isinstance(speaker_file, str):
            try:
                # Expecting a tuple: (sample_rate, audio_array)
                sr, sp_audio = speaker_file
                duration = len(sp_audio) / sr
                if duration < 2:
                    raise gr.Error("Speaker reference audio is too short. Please provide a longer audio sample (at least 2 seconds).")
                temp_speaker_file = "temp_speaker.wav"
                sf.write(temp_speaker_file, sp_audio, sr)
                speaker_file = temp_speaker_file
            except Exception as proc_err:
                raise gr.Error(f"Error processing speaker audio: {str(proc_err)}")
        
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=use_gpu)
        temp_file = "temp_cloned.wav"
        tts.tts_to_file(
            text=text,
            file_path=temp_file,
            speaker_wav=[speaker_file],
            language=language,
            split_sentences=True
        )
        audio_data, samplerate = sf.read(temp_file)
        os.remove(temp_file)
        
        if temp_speaker_file is not None:
            os.remove(temp_speaker_file)
            
        adjusted_samplerate = int(samplerate * speed)
        return (adjusted_samplerate, audio_data)
    except Exception as e:
        raise gr.Error(f"Error generating cloned speech: {str(e)}")

def create_ui():
    with gr.Blocks(title="XTTS Text-to-Speech App") as app:
        gr.Markdown("# XTTS Text-to-Speech App")
        with gr.Tabs():
            with gr.Tab("TTS"):
                gr.Markdown("## Original XTTS Text-to-Speech")
                with gr.Row():
                    with gr.Column():
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
                        audio_output = gr.Audio(
                            label="Generated Speech",
                            type="numpy"
                        )
                generate_btn.click(
                    fn=generate_speech,
                    inputs=[text_input, language],
                    outputs=audio_output
                )
                gr.Examples(
                    examples=[
                        ["Hello, this is a test of the XTTS text to speech system.", "en"],
                        ["Bonjour, ceci est un test du système de synthèse vocale XTTS.", "fr"],
                        ["Hola, esta es una prueba del sistema de texto a voz XTTS.", "es"]
                    ],
                    inputs=[text_input, language]
                )
            with gr.Tab("Cloner"):
                gr.Markdown("## Voice Cloner 🗣️")
                with gr.Row():
                    with gr.Column():
                        text_cloner = gr.Textbox(
                            label="Text to clone 📝",
                            placeholder="Enter text to clone voice...",
                            lines=5
                        )
                        language_cloner = gr.Dropdown(
                            choices=["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn"],
                            value="en",
                            label="Language"
                        )
                        speed_input = gr.Slider(
                            minimum=0.5,
                            maximum=2.0,
                            value=1.0,
                            step=0.1,
                            label="Speed ⚡"
                        )
                        use_gpu_checkbox = gr.Checkbox(
                            label="Use GPU",
                            value=False
                        )
                        speaker_audio = gr.Audio(
                            label="Upload Speaker Reference Audio 🎤",
                            type="filepath"
                        )
                        clone_btn = gr.Button("Clone Voice 😎", variant="primary")
                    with gr.Column():
                        audio_cloner = gr.Audio(
                            label="Cloned Speech",
                            type="numpy"
                        )
                clone_btn.click(
                    fn=generate_cloned_speech,
                    inputs=[text_cloner, language_cloner, speed_input, speaker_audio, use_gpu_checkbox],
                    outputs=audio_cloner
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
