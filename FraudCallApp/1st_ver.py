# from kivymd.uix.toolbar import MDToolbar

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
import speech_recognition as sr
import pickle

# Load the trained model and vectorizer
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

KV = """
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Fraud Call Detector"
            font_size: "20sp"
            halign: "center"
        Label:
            id: result_label
            text: "Press the mic and speak"
            font_size: "20sp"
            halign: "center"
        MDFillRoundFlatButton:
            text: "🎤 Speak"
            pos_hint: {"center_x": 0.5}
            on_release: app.start_speech_recognition()
"""

class MainScreen(Screen):
    pass

class FraudDetectionApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def start_speech_recognition(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.root.get_screen("main").ids.result_label.text = "Listening..."
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio).lower()
                self.root.get_screen("main").ids.result_label.text = f"You said: {text}"

                # Predict using trained model
                text_features = vectorizer.transform([text])
                prediction = model.predict(text_features)

                if prediction[0] == 1:
                    result = "⚠️ Fraudulent Call Detected!"
                else:
                    result = "✅ Normal Call"

                self.root.get_screen("main").ids.result_label.text = result

            except sr.UnknownValueError:
                self.root.get_screen("main").ids.result_label.text = "Couldn't recognize speech"

            except sr.RequestError:
                self.root.get_screen("main").ids.result_label.text = "Error connecting to API"

if __name__ == "__main__":
    FraudDetectionApp().run()
