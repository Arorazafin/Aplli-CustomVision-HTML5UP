from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": "***keycode1***"})
predictor = CustomVisionPredictionClient("https://xxxx.cognitiveservices.azure.com/", prediction_credentials)

with open("./camera/" + "100-gobelets-transparent.jpg", "rb") as image_contents:
    results = predictor.classify_image("***keycode2***", "Iteration2", image_contents.read())

# Display the results.
for prediction in results.predictions:
    print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))