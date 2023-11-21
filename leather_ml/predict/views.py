import tensorflow as tf
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
import os
import time
import numpy as np

import uuid
import pandas as pd
import json
import re
from django.contrib import messages
from django.views.decorators.cache import never_cache
from tensorflow.python.ops.numpy_ops import np_config
import requests
from tensorflow.keras.preprocessing import image

import numpy as np
import matplotlib.pyplot as plt
import os
np_config.enable_numpy_behavior()
# Create your views here.
path = ""

@never_cache
def index(request):
    request.session["uuid"] = str(uuid.uuid4())
    print(request.session["uuid"])
    return render(request, 'index.html')

@never_cache
def predict(data):
    headers = {"content-type": "application/json"}
    json_response = requests.post(
        'http://localhost:8502/v1/models/fashion_model:predict', data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']

    return predictions


@never_cache
@csrf_exempt
def upload(request):
    if request.method == "POST":
        u = request.session["uuid"]
        print(u, str(u))
        os.system("mkdir media/"+str(u))
        os.system("mkdir media/"+str(u)+"/output")
        uploaded_file = request.FILES['pic']
        # objtype_name = request.POST["obj"]
        dat =[]
        fs = FileSystemStorage()
        f1_name = uploaded_file.name
        filename = uploaded_file.name.replace(" ", "_")
        if (re.search(re.compile("([^\\s]+(\\.(?i)(jpeg|jpg|png|gif|bmp))$)"), filename)):
            temp = []
            # print(filename)
            urlname = fs.save(str(u)+"/"+filename, uploaded_file)
            url = fs.url(urlname)
            # fig = url.rsplit("/",1)[0]
            # print(fig)

            img = image.load_img(url, target_size=(256, 256))
            # Convert Image to a numpy array
            img = image.img_to_array(img, dtype=np.uint8)
            # Scaling the Image Array values between 0 and 1
            img = np.array(img)/255.0

            class_names = ['Bad Skin', 'Normal Skin']
            data = json.dumps({"signature_name": "serving_default",
                              "instances": img[np.newaxis, ...].tolist()})
            # print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
            predictions = predict(data)
            inde = predictions[0].index(max(predictions[0]))
            print(class_names[inde])
            class_names[inde] = class_names[inde].replace("_", " ")
            res = class_names[inde]
            score = predictions[0]
            content = "This image belongs to the class {} and with the confidence rate of {:.2f}%.".format(
            class_names[inde], 100 * np.max(score))
            temp.append(url)
            temp.append(res)
            temp.append(content)
            dat.append(temp)
            # print(dat)
            te_dat = dat[0].copy()
            des = "/workspaces/cow_ml/leather_ml/media/{}/output/output.csv".format(str(u))
            context = {"dat":dat,"des":des}
            # print(te_dat)
            te_dat[0] = te_dat[0].split("/")[-1]
            te_dat[2] = "{:.2f}%".format(100 * np.max(score))
            df = pd.DataFrame([te_dat],columns=["Image","Type","Percentage"])
            df.to_csv("media/{}/output/output.csv".format(str(u)))
        elif (re.search(re.compile("([^\\s]+(\\.(?i)(zip|rar|tar.gz))$)"), filename)):
            if filename.endswith("zip"):
                print("zip")
                urlname = fs.save(str(u)+"/"+filename, uploaded_file)
                time.sleep(3)
                os.system("unzip media/{}/{} -d media/{}/input/".format(str(u),filename,str(u)))
                directory = "/workspaces/cow_ml/leather_ml/media/{}/input/".format(str(u))
                for filename in os.scandir(directory):
                    if filename.is_file():
                        os.rename(filename.path,filename.path.replace(" ","_"))
                for filename in os.scandir(directory):
                    if filename.is_file():
                        temp  = []
                        url = filename.path
                        print(url)
                        img = image.load_img(url, target_size=(256, 256))
                        # Convert Image to a numpy array
                        img = image.img_to_array(img, dtype=np.uint8)
                        # Scaling the Image Array values between 0 and 1
                        img = np.array(img)/255.0
                        class_names = ['Bad Skin', 'Normal Skin']
                        data = json.dumps({"signature_name": "serving_default",
                              "instances": img[np.newaxis, ...].tolist()})
                        # print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
                        predictions = predict(data)
                        inde = predictions[0].index(max(predictions[0]))
                        print(class_names[inde])
                        class_names[inde] = class_names[inde].replace("_", " ")
                        res = class_names[inde]
                        score = predictions[0]
                        content = "This image belongs to the class {} and with the confidence rate of {:.2f}%.".format(
                        class_names[inde], 100 * np.max(score))
                        temp.append(url)
                        temp.append(res)
                        temp.append(content)
                        dat.append(temp)
                data_csv = []
                # data_csv = data_csv[0]
                des = "/workspaces/cow_ml/leather_ml/media/{}/output/output.csv".format(str(u))
                context = {"dat":dat,"des":des}
                print(dat)
                for i in range(0,len(dat)):
                    temp = dat[i].copy()
                    data_csv.append(temp)
                    data_csv[i][0] = data_csv[i][0].split("/")[-1]
                    data_csv[i][2] = data_csv[i][2].split("and with the confidence rate of")[-1]
                df = pd.DataFrame(data_csv,columns=["Image","Type","Percentage"])
                df.to_csv("media/{}/output/output.csv".format(str(u)))

            elif filename.endswith("rar"):
                print("rar")
                urlname = fs.save(str(u)+"/"+filename, uploaded_file)
                time.sleep(3)
                os.system("unrar e media/{}/{} -o media/{}/input/".format(str(u),filename,str(u)))
                directory = "/workspaces/cow_ml/leather_ml/media/{}/input/".format(str(u))
                for filename in os.scandir(directory):
                    if filename.is_file():
                        os.rename(filename.path,filename.path.replace(" ","_"))
                for filename in os.scandir(directory):
                    if filename.is_file():
                        temp  = []
                        url = filename.path
                        print(url)
                        img = image.load_img(url, target_size=(256, 256))
                        # Convert Image to a numpy array
                        img = image.img_to_array(img, dtype=np.uint8)
                        # Scaling the Image Array values between 0 and 1
                        img = np.array(img)/255.0
                        class_names = ['Bad Skin', 'Normal Skin']
                        data = json.dumps({"signature_name": "serving_default",
                              "instances": img[np.newaxis, ...].tolist()})
                        # print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
                        predictions = predict(data)
                        inde = predictions[0].index(max(predictions[0]))
                        print(class_names[inde])
                        class_names[inde] = class_names[inde].replace("_", " ")
                        res = class_names[inde]
                        score = predictions[0]
                        content = "This image belongs to the class {} and with the confidence rate of {:.2f}%.".format(
                        class_names[inde], 100 * np.max(score))
                        temp.append(url)
                        temp.append(res)
                        temp.append(content)
                        dat.append(temp)
                data_csv = []
                # data_csv = data_csv[0]
                des = "/workspaces/cow_ml/leather_ml/media/{}/output/output.csv".format(str(u))
                context = {"dat":dat,"des":des}
                print(dat)
                for i in range(0,len(dat)):
                    temp = dat[i].copy()
                    data_csv.append(temp)
                    data_csv[i][0] = data_csv[i][0].split("/")[-1]
                    data_csv[i][2] = data_csv[i][2].split("and with the confidence rate of")[-1]
                df = pd.DataFrame(data_csv,columns=["Image","Type","Percentage"])
                df.to_csv("media/{}/output/output.csv".format(str(u)))
                

            elif filename.endswith(".tar.gz"):
                print(".tar.gz")
                urlname = fs.save(str(u)+"/"+filename, uploaded_file)
                time.sleep(3)
                os.system("mkdir media/{}/input/".format(str(u)))
                os.system("tar -xvzf media/{}/{} -C media/{}/input/".format(str(u),filename,str(u)))
                directory = "/workspaces/cow_ml/leather_ml/media/{}/input/".format(str(u))
                for filename in os.scandir(directory):
                    if filename.is_file():
                        os.rename(filename.path,filename.path.replace(" ","_"))
                for filename in os.scandir(directory):
                    if filename.is_file():
                        temp  = []
                        url = filename.path
                        print(url)
                        img = image.load_img(url, target_size=(256, 256))
                        # Convert Image to a numpy array
                        img = image.img_to_array(img, dtype=np.uint8)
                        # Scaling the Image Array values between 0 and 1
                        img = np.array(img)/255.0
                        class_names = ['Bad Skin', 'Normal Skin']
                        data = json.dumps({"signature_name": "serving_default",
                              "instances": img[np.newaxis, ...].tolist()})
                        # print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
                        predictions = predict(data)
                        inde = predictions[0].index(max(predictions[0]))
                        print(class_names[inde])
                        class_names[inde] = class_names[inde].replace("_", " ")
                        res = class_names[inde]
                        score = predictions[0]
                        content = "This image belongs to the class {} and with the confidence rate of {:.2f}%.".format(
                        class_names[inde], 100 * np.max(score))
                        temp.append(url)
                        temp.append(res)
                        temp.append(content)
                        dat.append(temp)
                data_csv = []
                # data_csv = data_csv[0]
                des = "/workspaces/cow_ml/leather_ml/media/{}/output/output.csv".format(str(u))
                context = {"dat":dat,"des":des}
                print(dat)
                for i in range(0,len(dat)):
                    temp = dat[i].copy()
                    data_csv.append(temp)
                    data_csv[i][0] = data_csv[i][0].split("/")[-1]
                    data_csv[i][2] = data_csv[i][2].split("and with the confidence rate of")[-1]
                df = pd.DataFrame(data_csv,columns=["Image","Type","Percentage"])
                df.to_csv("media/{}/output/output.csv".format(str(u)))


            elif filename.endswith(".tar.bz2"):
                print(".tar.bz2")
            else:
                messages.error(
                request, "Check the uploaded file must either be an image or a compressed files(zip,rar,tar.gz) containing image!")
                return render(request, "index.html")
        else:
            messages.error(
                request, "Check the uploaded file must either be an image or a compressed folder containing image!")
            return redirect(index)


    return render(request, "result.html", context)
