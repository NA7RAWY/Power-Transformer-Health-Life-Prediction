from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

clf = joblib.load("transformer_status_model.pkl")    
reg = joblib.load("transformer_life_model.pkl")       
scaler = joblib.load("scaler.pkl")                    

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        input_data = np.array([[data['hydrogen'], data['methane'], data['acethylene'], data['ethylene']]])
        input_scaled = scaler.transform(input_data)

        status_model = clf.predict(input_scaled)[0]  
        life = reg.predict(input_scaled)[0]

    
        if life > 50:
            final_status = "Good"
        elif life < 20:
            final_status = "Bad"
        else:
            final_status = "Good" if status_model == 1 else "Bad"

        recommendation = "Transformer is healthy." if final_status == "Good" else "Consider maintenance or inspection soon."

        return jsonify({
            "status": final_status,
            "status_model": "Good" if status_model == 1 else "Bad",
            "life": round(life, 2),
            "recommendation": recommendation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
