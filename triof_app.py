from flask import Flask, render_template, request
from src.utils import *

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

from flask import session
from flask_session import Session

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')

def home():
    return render_template('home.html')


@app.route('/start')
def insert():
    
    open_waste_slot()
    show = take_trash_picture()
    session['show'] = show
    print(show)
    return render_template('insert.html', image=show)


@app.route('/waste/pick-type')
def pick_type():
    close_waste_slot()
    show = session.get('show')
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": "***keycode1***"})
    predictor = CustomVisionPredictionClient("https://***.cognitiveservices.azure.com/", prediction_credentials)

    with open("./camera/" + show, "rb") as image_contents:
        results = predictor.classify_image("**keycode2***", "Iteration2", image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))
        categ = prediction.tag_name
        proba = prediction.probability * 100
        break

    data = {
        'image': show,
        'categorie': categ,
        'probabilite': proba
    }

    return render_template('type.html', data=data)


@app.route('/confirmation', methods=['POST'])
def confirmation():
    # waste_type = request.form['type']
    

    # process_waste(waste_type)
    return render_template('confirmation.html')



if __name__ == "__main__":
    app.run(debug=True)
