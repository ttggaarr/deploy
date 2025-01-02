from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model_path = 'C:\\Deploy\\best_svm_model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/klasifikasi', methods=['GET', 'POST'])
def klasifikasi():
    if request.method == 'GET':
        return render_template('klasifikasi.html')
    elif request.method == 'POST':
        try:
        # Ambil data dari form dengan nilai 1-2
            input_data = [
                int(request.form['YELLOW_FINGERS']),
                int(request.form['ANXIETY']),
                int(request.form['PEER_PRESSURE']),
                int(request.form['CHRONIC DISEASE']),
                int(request.form['FATIGUE']),
                int(request.form['ALLERGY']),
                int(request.form['WHEEZING']),
                int(request.form['ALCOHOL CONSUMING']),
                int(request.form['COUGHING']),
                int(request.form['SWALLOWING DIFFICULTY']),
                int(request.form['CHEST PAIN']),
            ]

            # Pastikan nilai input berada di antara 1 dan 2
            if not all(1 <= value <= 2 for value in input_data):
                return "Input hanya boleh bernilai 1 atau 2.", 400

            # Hitung jumlah nilai 2
            count_2 = input_data.count(2)
            count_1 = input_data.count(1)

            # Tentukan hasil berdasarkan nilai input
            if count_2 > count_1:
                result = "Positif Kanker Paru-Paru"
            else:
                result = "Negatif Kanker Paru-Paru"

            # Render template dengan hasil
            return render_template('result.html', result=result)

        except Exception as e:
            print("Error:", e)
            return "Terjadi kesalahan dalam prediksi. Silakan periksa kembali input Anda.", 500
            
if __name__ == '__main__':
    app.run(debug=True)
