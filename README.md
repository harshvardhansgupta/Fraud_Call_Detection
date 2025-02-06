# Fraud_Call_Detection

## Project Files Description

1. **Model_Training.ipynb**: Jupyter notebook where the fraud detection model is trained and saved.
2. **README.md**: Documentation providing an overview of the project and instructions for setup and usage.
3. **main_dataset_fcd.txt**: Dataset containing labeled call data used for training the fraud detection model.
4. **prediction.py**: Python script to load the trained model and vectorizer for making fraud predictions.
5. **trained_model.pkl**: Serialized machine learning model trained for fraud call detection.
6. **vectorizer.pkl**: Serialized vectorizer used to convert text data into numerical features for model input.
7. **FraudCallApp**: Main project folder containing all necessary files for the fraud detection app.

## App Description

The **Fraud Call Detection App** is a user-friendly application developed using **Kivy**, a Python framework for building multi-platform applications with a natural user interface.

### Key Features:
1. **Real-time Predictions**:  
   - The app allows users to input call data and instantly predicts whether the call is **fraudulent** or **normal** using the trained machine learning model.
2. **Speech-to-Text Integration**:  
   - The app utilizes the **Google Speech-to-Text API** to transcribe voice input into text, enabling users to conveniently analyze call data directly from audio.
3. **Seamless Integration**:  
   - The app leverages the **trained_model.pkl** and **vectorizer.pkl** to ensure accurate predictions by transforming input text into features and applying the logistic regression model.
4. **Core Application Code**:  
   - The main logic and UI of the app are implemented in the **main.py** file, which serves as the backbone of the application.
5. **Intuitive Design**:  
   - The app interface is simple, interactive, and designed to provide a smooth user experience, making it accessible for users of all technical backgrounds.
6. **Cross-Platform Compatibility**:  
   - The app can be packaged as an **APK** for Android devices, enabling widespread accessibility and portability.

This app empowers users to detect fraudulent calls effectively, combining robust machine learning capabilities, speech-to-text functionality, and a sleek design.

## Model Description

The fraud call detection model is built using a **dataset of approximately 6000 rows**, labeled as either "fraud" or "normal". 

### Key Steps:
1. **Data Encoding**: 
   - The textual data was encoded using **vectorization** with a maximum of **1000 features**, ensuring efficient and meaningful representation of the data.   
2. **Model Training**: 
   - A **Logistic Regression** algorithm was employed with **C=10** to balance the regularization and achieve optimal performance.

### Performance:
- The model achieved an impressive **accuracy of 98.6%**, demonstrating its effectiveness in accurately identifying fraudulent and normal calls.

The trained model and vectorizer are saved as `trained_model.pkl` and `vectorizer.pkl` for easy deployment and prediction.

## Technologies Used

1. **Kivy**:  
   - Used for developing the app's user interface and ensuring cross-platform compatibility.  
   - Provides a smooth and interactive design for the fraud detection application.
2. **Scikit-learn**:  
   - Utilized for training and implementing the machine learning model (Logistic Regression).  
   - Includes tools like **TfidfVectorizer** for text vectorization and model evaluation.
3. **Google Speech-to-Text API**:  
   - Integrated for converting voice input into text, allowing users to analyze call data directly from audio.
4. **Pickle**:  
   - Used for serializing and saving the trained model (**trained_model.pkl**) and vectorizer (**vectorizer.pkl**) for later use.
5. **Python**:  
   - The core programming language used for all aspects of the project, including machine learning, app development, and API integration.
6. **Buildozer**:  
   - Employed for packaging the app into an **APK** file, making it compatible with Android devices.

These technologies work together to create a robust, efficient, and user-friendly fraud detection application.


