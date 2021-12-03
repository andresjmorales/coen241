import keras
from keras.models import load_model
from flask import Flask
from flask import request
from upload import *
from download import *
import numpy as np
import json

global_path = ''
global_bucket =  'coen241_core'
input_vars = ["radius_mean","texture_mean","perimeter_mean","area_mean","smoothness_mean","compactness_mean","concavity_mean","concave_points_mean","symmetry_mean","fractal_dimension_mean","radius_se","texture_se","perimeter_se","area_se","smoothness_se","compactness_se","concavity_se","concave_points_se","symmetry_se","fractal_dimension_se","radius_worst","texture_worst","perimeter_worst","area_worst","smoothness_worst","compactness_worst","concavity_worst","concave_points_worst","symmetry_worst","fractal_dimension_worst"]


# radius_mean=17.99&texture_mean=10.38&perimeter_mean=122.8&area_mean=1001&smoothness_mean=0.1184&compactness_mean=0.2776&concavity_mean=0.3001&concave_points_mean=0.1471&symmetry_mean=0.2419&fractal_dimension_mean=0.07871&radius_se=1.095&texture_se=0.9053&perimeter_se=8.589&area_se=153.4&smoothness_se=0.006399&compactness_se=0.04904&concavity_se=0.05373&concave_points_se=0.01587&symmetry_se=0.03003&fractal_dimension_se=0.006193&radius_worst=0.006193&texture_worst=17.33&perimeter_worst=184.6&area_worst=2019&smoothness_worst=0.1622&compactness_worst=0.6656&concavity_worst=0.7119&concave_points_worst=0.2654&symmetry_worst=0.4601&fractal_dimension_worst=0.1189
#17.99,10.38,122.8,1001,0.1184,0.2776,0.3001,0.1471,0.2419,0.07871,1.095,0.9053,8.589,153.4,0.006399,0.04904,0.05373,0.01587,0.03003,0.006193,0.006193,17.33,184.6,2019,0.1622,0.6656,0.7119,0.2654,0.4601,0.1189

#
#
#
def diagnosis(pred):
    if pred <= .5:
        return "Malignant"
    else:
        return "Benign"


def download_files(parent_project_name):
    if download(global_path + parent_project_name + ".h5", parent_project_name + ".h5", global_bucket):
        pass
    else:
        return False

    return True

def upload_files(parent_project_name):
    if upload(parent_project_name + ".png", parent_project_name + ".png", global_bucket):
        pass
    else:
        return False
    if upload(parent_project_name + ".h5", parent_project_name + ".h5", global_bucket):
        pass
    else:
        return False

    return True

def get_args(content):
    input_arr = []
    for features in input_vars:
        input_arr.append(float(content[features]))

    return np.array(input_arr)


if download_files('data'):
    pass
else:
    exit()
model = load_model('data.h5')


app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def index():
    content = request.json
    get_args(content)
    arr = get_args(content)
    return "Predictions is: " + diagnosis(model.predict(np.array([arr,])))

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8080)
