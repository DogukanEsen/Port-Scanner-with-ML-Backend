from flask import Flask,request,jsonify,make_response
import pickle
import numpy as np
from flask_cors import CORS
import re

model = pickle.load(open("model_pickle","rb"))

app = Flask(__name__)
cors = CORS(app, origins= ["https://ml-port-scanner.netlify.app/","https://ml-port-scanner.netlify.app/"])

@app.route("/predict",methods=["POST","OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        # Preflight isteğine yanıt ver
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "https://ml-port-scanner.netlify.app")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response
    else:
        test=request.get_json()
        if test is None:
            return jsonify({"error": "Geçersiz istek, veri yok."}), 400
        pattern = r'^[0-9.-]+$'
        data=list(request.get_json().values())
        for value in data:
            if not re.match(pattern,value):
                return jsonify({"error": "Geçersiz istek, hatali veri girisi."}), 400
        np_data=np.array(data)
        prediction=model.predict([np_data])
        if prediction:
            return "Zararlı tarama tespit edildi."
        else:
            return "Zararsız tarama tespit edildi."

if __name__=="__main__":
    app.run(debug=False)