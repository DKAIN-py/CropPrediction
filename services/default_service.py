from flask import request, render_template
import pandas as pd
import ydf

# Load the trained crop recommendation model
model = ydf.load_model("CropRecommendModel")

def get_prediction():
    if request.method == 'POST':
        # Read form data
        input_data = {
            'N': float(request.form['N']),
            'P': float(request.form['P']),
            'K': float(request.form['K']),
            'temperature': float(request.form['temperature']),
            'humidity': float(request.form['humidity']),
            'ph': float(request.form['ph']),
            'rainfall': float(request.form['rainfall']),
        }

        # Convert to DataFrame
        df = pd.DataFrame([input_data])

        # Make prediction
        probs = model.predict(df)
        labels = model.label_classes()
        predicted_label = labels[probs[0].argmax()]

        return render_template('form.html', prediction=predicted_label, input_data=input_data)

    return render_template('form.html', prediction=None)