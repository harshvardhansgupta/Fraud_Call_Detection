from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import speech_recognition as sr
import pickle
import threading

# Load the trained model and vectorizer
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

class FraudDetectionApp(App):
    def build(self):
        self.running = False  # To track if speech recognition is running

        # Main Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Title
        self.title_label = Label(text="📞 Fraud Call Detector", font_size=28, bold=True)
        layout.add_widget(self.title_label)

        # Live Speech-to-Text Display
        self.speech_text_label = Label(text="🎤 Speak and see text here...", font_size=18, size_hint_y=None, height=50)
        layout.add_widget(self.speech_text_label)

        # Scroll View for Prediction Output
        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.result_label = Label(text="Press 'Start' to begin detection", font_size=18, size_hint_y=None, height=100)
        scroll_view.add_widget(self.result_label)
        layout.add_widget(scroll_view)

        # Buttons Layout
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        # Start Button
        self.start_button = Button(text="▶ Start", font_size=20, background_color=(0, 1, 0, 1))
        self.start_button.bind(on_press=self.start_speech_recognition)
        button_layout.add_widget(self.start_button)

        # Stop Button
        self.stop_button = Button(text="⏹ Stop", font_size=20, background_color=(1, 0, 0, 1))
        self.stop_button.bind(on_press=self.stop_speech_recognition)
        button_layout.add_widget(self.stop_button)

        layout.add_widget(button_layout)
        return layout

    def start_speech_recognition(self, instance):
        """Start continuous speech recognition in a separate thread"""
        if not self.running:
            self.running = True
            threading.Thread(target=self.recognize_speech, daemon=True).start()
            self.result_label.text = "🎤 Listening for calls..."

    def stop_speech_recognition(self, instance):
        """Stop the continuous speech recognition"""
        self.running = False
        self.result_label.text = "⏹ Detection Stopped."

    def recognize_speech(self):
        """Handles speech recognition and continuous prediction"""
        recognizer = sr.Recognizer()
        while self.running:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source)

                text = recognizer.recognize_google(audio).lower()
                self.speech_text_label.text = f"📢 You said: {text}"

                # Predict using the trained model
                text_features = vectorizer.transform([text])
                prediction = model.predict(text_features)

                if prediction[0] == 1:
                    result = "⚠ Fraudulent Call Detected!"
                else:
                    result = "✅ Normal Call"

                self.result_label.text = result  # Update UI with the prediction result

            except sr.UnknownValueError:
                self.speech_text_label.text = "😕 Couldn't recognize speech"
            except sr.RequestError:
                self.speech_text_label.text = "🔗 Error connecting to API"

if __name__ == "__main__":
    FraudDetectionApp().run()
