from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
import speech_recognition as sr
import pickle
import threading
import time
from functools import partial

# Load the trained model and vectorizer
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

class PulsingWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pulse_size = 0
        self.alpha = 0
        
        with self.canvas:
            self.color = Color(0, 1, 0.8, 0)
            self.circle = Line(circle=(self.center_x, self.center_y, 0))
            
    def start_pulsing(self):
        Clock.schedule_interval(self.pulse, 1/60)
        
    def stop_pulsing(self):
        Clock.unschedule(self.pulse)
        self.pulse_size = 0
        self.alpha = 0
        self.color.a = 0
        
    def pulse(self, dt):
        self.pulse_size += 2
        self.alpha = max(0, 1 - self.pulse_size/100)
        self.color.a = self.alpha
        self.circle.circle = (self.center_x, self.center_y, self.pulse_size)
        
        if self.pulse_size > 100:
            self.pulse_size = 0
            
    def set_color(self, r, g, b):
        self.color.rgb = (r, g, b)

class FuturisticButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex('#1a1a2e')
        self.border = (0, 0, 0, 0)
        
        with self.canvas.before:
            Color(*get_color_from_hex('#00f2ff'))
            self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size

class FraudDetectionApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#0a0a1e')
        self.running = False
        self.listening_paused = False
        
        # Main Layout
        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=30)
        
        # Title with glowing effect
        title_box = BoxLayout(size_hint=(1, 0.15))
        self.title_label = Label(
            text="[color=#00f2ff]\U0001F50AAI Fraud Shield[/color]",
            font_size=32,
            bold=True,
            markup=True
        )
        title_box.add_widget(self.title_label)
        main_layout.add_widget(title_box)
        
        # Status Container
        status_container = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        
        # Pulse Animation Widget
        self.pulse_widget = PulsingWidget(size_hint=(1, 0.7))
        status_container.add_widget(self.pulse_widget)
        
        # AI Status Display
        self.status_label = Label(
            text="[color=#00f2ff]System Ready[/color]",
            font_size=24,
            markup=True,
            size_hint=(1, 0.3)
        )
        status_container.add_widget(self.status_label)
        main_layout.add_widget(status_container)
        
        # Live Speech Display
        self.speech_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.2),
            padding=[20, 10]
        )
        with self.speech_box.canvas.before:
            Color(*get_color_from_hex('#1a1a2e'))
            self.speech_rect = RoundedRectangle(pos=self.speech_box.pos, size=self.speech_box.size, radius=[15])
        
        self.speech_text_label = Label(
            text="[color=#00f2ff]Awaiting Voice Input...[/color]",
            markup=True,
            font_size=18
        )
        self.speech_box.add_widget(self.speech_text_label)
        main_layout.add_widget(self.speech_box)
        
        # Results Display
        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.result_label = Label(
            text="[color=#00f2ff]Detection Results Will Appear Here[/color]",
            markup=True,
            font_size=20,
            size_hint_y=None,
            height=100
        )
        scroll_view.add_widget(self.result_label)
        main_layout.add_widget(scroll_view)
        
        # Control Buttons
        button_layout = BoxLayout(size_hint=(1, 0.15), spacing=20)
        
        self.start_button = FuturisticButton(
            text="Initialize Shield",
            font_size=20
        )
        self.start_button.bind(on_press=self.start_speech_recognition)
        
        self.stop_button = FuturisticButton(
            text="  Deactivate",
            font_size=20
        )
        self.stop_button.bind(on_press=self.stop_speech_recognition)
        
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        main_layout.add_widget(button_layout)
        
        # Bind layout updates
        self.speech_box.bind(pos=self.update_speech_rect, size=self.update_speech_rect)
        
        return main_layout
    
    def update_speech_rect(self, *args):
        self.speech_rect.pos = self.speech_box.pos
        self.speech_rect.size = self.speech_box.size
    
    def start_speech_recognition(self, instance):
        if not self.running:
            self.running = True
            self.listening_paused = False
            self.pulse_widget.start_pulsing()
            self.animate_status("Shield Active - Monitoring")
            threading.Thread(target=self.recognize_speech, daemon=True).start()
    
    def stop_speech_recognition(self, instance):
        self.running = False
        self.pulse_widget.stop_pulsing()
        self.animate_status("Shield Deactivated")
    
    def animate_status(self, text):
        self.status_label.text = f"[color=#00f2ff]{text}[/color]"
        anim = Animation(opacity=0.5, duration=0.2) + Animation(opacity=1, duration=0.2)
        anim.start(self.status_label)
    
    def update_ui(self, text, result, is_fraud):
        """Update UI elements on the main thread"""
        self.speech_text_label.text = f"[color=#00f2ff]Detected Speech: {text}[/color]"
        self.result_label.text = result
        if is_fraud:
            self.pulse_widget.set_color(1, 0, 0)  # Red for fraud
        else:
            self.pulse_widget.set_color(0, 1, 0)  # Green for safe
        
        # Schedule resuming listening after delay
        self.listening_paused = True
        Clock.schedule_once(self.resume_listening, 0.5)  # 0.5 second delay
    
    def resume_listening(self, dt):
        """Resume listening after delay"""
        if self.running:
            self.listening_paused = False
    
    def recognize_speech(self):
        recognizer = sr.Recognizer()
        while self.running:
            if not self.listening_paused:
                try:
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        Clock.schedule_once(lambda dt: setattr(
                            self.speech_text_label, 'text', 
                            "[color=#00f2ff]Analyzing Audio...[/color]"
                        ))
                        audio = recognizer.listen(source)
                    
                    text = recognizer.recognize_google(audio).lower()
                    
                    # Predict using the model
                    text_features = vectorizer.transform([text])
                    prediction = model.predict(text_features)
                    
                    if prediction[0] == 1:
                        result = "[color=#ff0000]ALERT: Potential Fraud Detected!\nDisconnect the call immediately[/color]"
                        is_fraud = True
                    else:
                        result = "[color=#00ff00]Communication Verified Safe[/color]"
                        is_fraud = False
                    
                    # Schedule UI updates on the main thread
                    Clock.schedule_once(lambda dt: self.update_ui(text, result, is_fraud))
                    
                except sr.UnknownValueError:
                    Clock.schedule_once(lambda dt: setattr(
                        self.speech_text_label, 'text',
                        "[color=#ffa500]Speech Unclear - Please Repeat[/color]"
                    ))
                except sr.RequestError:
                    Clock.schedule_once(lambda dt: setattr(
                        self.speech_text_label, 'text',
                        "[color=#ff0000]Network Error - Check Connection[/color]"
                    ))
            
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            
            if not self.running:
                break

if __name__ == "__main__":
    FraudDetectionApp().run()