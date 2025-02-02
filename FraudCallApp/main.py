from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
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
        # Main Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Title
        self.title_label = Label(text="Fraud Call Detector", font_size=24, bold=True)
        layout.add_widget(self.title_label)

        # Result Label
        self.result_label = Label(text="Press the button & speak", font_size=18)
        layout.add_widget(self.result_label)

        # Speak Button
        self.speak_button = Button(text="🎤 Speak", font_size=18, size_hint=(1, 0.2))
        self.speak_button.bind(on_press=self.start_speech_recognition)
        layout.add_widget(self.speak_button)

        return layout

    def start_speech_recognition(self, instance):
        """Start speech recognition in a separate thread to prevent UI freezing"""
        threading.Thread(target=self.recognize_speech, daemon=True).start()

    def recognize_speech(self):
        """Handles speech recognition and prediction"""
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.result_label.text = "🎤 Listening..."
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio).lower()
            self.result_label.text = f"📢 You said: {text}"

            # Predict using the trained model
            text_features = vectorizer.transform([text])
            prediction = model.predict(text_features)

            if prediction[0] == 1:
                result = "⚠ Fraudulent Call Detected!"
            else:
                result = "✅ Normal Call"

            self.result_label.text = result

        except sr.UnknownValueError:
            self.result_label.text = "😕 Couldn't recognize speech"
        except sr.RequestError:
            self.result_label.text = "🔗 Error connecting to API"

if __name__ == "__main__":
    FraudDetectionApp().run()