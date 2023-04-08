import tensorflow as tf
import numpy as np
import os

model_path = os.path.join(os.getcwd(),"artifacts","advice_ai")
new_model = tf.keras.models.load_model(model_path)

examples = ["Customer Churn"]

results = new_model.predict(examples)
print(np.argmax(results))
