from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model_path = 'C:\Deploy3\gb_model'
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    raise Exception(f"Model file '{model_path}' not found. Please ensure the file exists.")

@app.route('/')
def home():
    """Route untuk halaman utama."""
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Route untuk melakukan prediksi."""
    if request.method == 'GET':
        return render_template('predict.html')  # Tampilkan halaman prediksi
    
    elif request.method == 'POST':
        try:
            # Ambil data JSON dari request
            input_data = request.json

            # Pastikan semua parameter ada
            required_features = [
                'age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholestoral',
                'fasting_blood_sugar', 'rest_ecg', 'Max_heart_rate', 'exercise_induced_angina',
                'oldpeak', 'slope', 'vessels_colored_by_flourosopy', 'thalassemia'
            ]

            # Validasi input
            if not all(feature in input_data for feature in required_features):
                missing_features = [feature for feature in required_features if feature not in input_data]
                return jsonify({"error": f"Missing features: {', '.join(missing_features)}"}), 400

            # Konversi data ke array numpy
            feature_values = [input_data[feature] for feature in required_features]
            input_array = np.array(feature_values).reshape(1, -1)

            # Prediksi
            prediction = model.predict(input_array)[0]

            # Tentukan hasil prediksi
            result = "Positif Terkena Penyakit Jantung" if prediction == 1 else "Negatif Terkena Penyakit Jantung"

            return jsonify({"prediction": result})

        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
