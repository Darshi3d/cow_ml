import json
from tensorflow.python.ops.numpy_ops import np_config
import requests
np_config.enable_numpy_behavior()
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras import optimizers, losses
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# cow_url = "https://gumlet.assettype.com/greaterkashmir%2F2022-08%2F031e4e36-3d97-454f-a52d-0ebc8c64cbb1%2FScreenshot__2983_.png?auto=format%2Ccompress&fit=max&format=webp&w=768&dpr=1.0"
# cow_path = tf.keras.utils.get_file('random_pic', origin=cow_url)

s_path = "/workspaces/cow_ml/lumpy_Test.webp"
img = image.load_img(s_path, target_size=(256, 256))
# Convert Image to a numpy array
img = image.img_to_array(img, dtype=np.uint8)
# Scaling the Image Array values between 0 and 1
img = np.array(img)/255.0

class_names =['Lumpy_Skin', 'Normal_Skin']
data = json.dumps({"signature_name": "serving_default", "instances":img[np.newaxis, ...].tolist()})
print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))
headers = {"content-type": "application/json"}
json_response = requests.post('http://localhost:8502/v1/models/fashion_model:predict', data=data, headers=headers)
predictions = json.loads(json_response.text)['predictions']

index = predictions[0].index(max(predictions[0]))
print(class_names[index])