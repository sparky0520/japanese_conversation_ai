import tkinter as tk
from tkinter import Canvas, Button, Label
import threading
import queue
import numpy as np
import time

# Import your existing modules
from asr import VoiceActivatedASR
from llm import JapaneseChatBot
from tts import tts_stream

# --- Application Constants ---
BG_COLOR = "#1a1a1a"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#ff6b6b"
CANVAS_COLOR = "#2a2a2a"
FONT_NAME = "Arial"

class AkiTutorApp(tk.Tk):
    """
    The main application class for the Aki AI Tutor GUI.
    """
    def __init__(self):
        super().__init__()
        self.title("Aki - Japanese AI Tutor")
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)

        # --- State Management ---
        self.chat_active = threading.Event()
        self.current_state = "idle"  # idle, listening, thinking, speaking

        # --- Backend Initialization ---
        self.asr = VoiceActivatedASR()
        self.chat_bot = JapaneseChatBot()

        # --- Communication Queues ---
        # Used to pass data between threads (audio/logic) and the GUI
        self.audio_queue = queue.Queue()
        self.transcription_queue = queue.Queue()

        # --- UI Initialization ---
        self._create_widgets()
        self.show_homescreen()

        # Start the GUI update loop
        self.update_gui()

    def _create_widgets(self):
        """Creates all UI widgets for both homescreen and chat screen."""
        # --- Homescreen Widgets ---
        self.homescreen_frame = tk.Frame(self, bg=BG_COLOR)
        self.title_label = Label(self.homescreen_frame, text="Chat with Aki", font=(FONT_NAME, 40, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        self.start_button = Button(self.homescreen_frame, text="Start Chat", font=(FONT_NAME, 20), bg=ACCENT_COLOR, fg=BG_COLOR, command=self.start_chat, relief="flat", padx=20, pady=10)
        self.title_label.pack(pady=50)
        self.start_button.pack(pady=20)

        # --- Chat Screen Widgets ---
        self.chatscreen_frame = tk.Frame(self, bg=BG_COLOR)
        self.waveform_canvas = Canvas(self.chatscreen_frame, bg=CANVAS_COLOR, height=300, width=700, highlightthickness=0)
        self.speak_now_label = Label(self.chatscreen_frame, text="", font=(FONT_NAME, 24, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
        self.end_call_button = Button(self.chatscreen_frame, text="End Call", font=(FONT_NAME, 16), bg="#555555", fg=TEXT_COLOR, command=self.end_chat, relief="flat", padx=15, pady=5)
        self.waveform_canvas.pack(pady=40)
        self.speak_now_label.pack(pady=20)
        self.end_call_button.pack(pady=20)

    def show_homescreen(self):
        """Displays the homescreen and hides the chat screen."""
        self.chatscreen_frame.pack_forget()
        self.homescreen_frame.pack(expand=True, fill="both")
        self.current_state = "idle"

    def show_chatscreen(self):
        """Displays the chat screen and hides the homescreen."""
        self.homescreen_frame.pack_forget()
        self.chatscreen_frame.pack(expand=True, fill="both")

    def start_chat(self):
        """Initializes and starts a new chat session."""
        self.show_chatscreen()
        self.chat_active.set()
        self.chat_bot.reset_conversation()

        # Run the main chat logic in a separate thread to not freeze the GUI
        self.chat_thread = threading.Thread(target=self.run_chat_loop, daemon=True)
        self.chat_thread.start()

    def end_chat(self):
        """Ends the current chat session and returns to the homescreen."""
        self.chat_active.clear()
        # Give the thread a moment to recognize the flag
        self.after(100, self.show_homescreen)

    def run_chat_loop(self):
        """The core logic loop for the conversation."""
        while self.chat_active.is_set():
            # 1. Listen for user's speech
            self.current_state = "listening"
            transcription = self.asr.listen_for_speech()

            if not self.chat_active.is_set(): break

            if transcription.strip():
                # 2. Process input and get AI response
                self.current_state = "thinking"
                if transcription.lower() in ['quit', 'exit', 'bye', 'さようなら', 'バイバイ']:
                    self.end_chat()
                    break

                response = self.chat_bot.get_response(transcription)

                # 3. Speak the AI response
                if response and response.strip():
                    self.current_state = "speaking"
                    tts_stream(response)
            
            # Reset for the next turn
            self.current_state = "idle_listening" # A brief pause before listening again
            time.sleep(0.5)


    def update_gui(self):
        """Periodically updates the GUI elements like the waveform and labels."""
        self.update_waveform()
        self.update_speak_indicator()
        # Schedule the next update
        self.after(50, self.update_gui)

    def update_waveform(self):
        """Redraws the audio waveform on the canvas based on data from the queue."""
        canvas = self.waveform_canvas
        canvas.delete("waveform")

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        h_center = h / 2

        # Drain the queue to get recent audio data
        points = []
        max_amplitude = 0
        while not self.audio_queue.empty():
            data = self.audio_queue.get_nowait()
            amplitude = np.mean(np.abs(data)) * 1000 # Amplification for visibility
            max_amplitude = max(max_amplitude, amplitude)
            points.append(amplitude)

        if not points:
            # Draw a flat line when there's no audio
            canvas.create_line(0, h_center, w, h_center, fill="#666666", width=2, tags="waveform")
            return

        # Determine color based on state
        if self.current_state == "listening":
            line_color = "#4a90e2" # Blue for user
        elif self.current_state == "speaking":
            line_color = ACCENT_COLOR # Red for Aki
        else:
            line_color = "#666666"

        # Create line coordinates
        coords = []
        num_points = len(points)
        for i, p in enumerate(points):
            x = (i / num_points) * w
            y = h_center - (p / max(1, max_amplitude)) * (h_center * 0.8) # Normalize and scale
            coords.extend([x, y])

        if len(coords) > 2:
            canvas.create_line(coords, fill=line_color, width=2.5, tags="waveform")

    def update_speak_indicator(self):
        """Updates the 'Speak Now' label based on the current state."""
        if self.current_state == "listening":
            # Simple "glow" effect by toggling color
            # current_color = self.speak_now_label.cget("fg")
            # next_color = ACCENT_COLOR if current_color == TEXT_COLOR else TEXT_COLOR
            self.speak_now_label.config(text="Speak now", fg=ACCENT_COLOR)
        elif self.current_state == "thinking":
            self.speak_now_label.config(text="Aki is thinking...", fg=TEXT_COLOR)
        else:
            self.speak_now_label.config(text="")


if __name__ == "__main__":
    app = AkiTutorApp()
    app.mainloop()