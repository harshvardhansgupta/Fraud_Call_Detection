# THIS WILL RUN ONLY LOCALYY AND NOT ON COLLAB

import speech_recognition as sr
import pickle

# Load the trained model and vectorizer

with open(r'trained_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open(r'vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Initialize the recognizer
r = sr.Recognizer()

print("Starting detection, start speaking (Press Ctrl + C to exit)")
try:
    while True:
        try:
            # Use the microphone as the source for input
            with sr.Microphone() as source2:
                # Adjust the energy threshold based on surrounding noise
                r.adjust_for_ambient_noise(source2, duration=2)

                # Listen for the user's input
                audio2 = r.listen(source2)

                # Convert audio to text using Google's Speech Recognition API
                MyText = r.recognize_google(audio2).lower()
                print("Did you say:", MyText)

                # Convert text input to features and predict
                text_to_predict = vectorizer.transform([MyText])
                prediction = model.predict(text_to_predict)

                if prediction[0] == 1:
                    print("Prediction: Fraudulent call ")
                else:
                    print("Prediction: Normal call ")

        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        except sr.UnknownValueError:
            print("Unknown error occurred (speech not recognized)")

except KeyboardInterrupt:
    print("\nExiting... Goodbye! ")
