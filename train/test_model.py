import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# ---- Load Model ----
model = tf.keras.models.load_model("model.keras")

# ---- Path to test image ----
img_path = "../train/test_images/test_image.jpg"

# ---- Preprocess image ----
img = image.load_img(img_path, target_size=(160, 160))
img_array = image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
img_array = img_array / 255.0  # Normalize if your training generator normalized

# ---- Predict ----
pred = model.predict(img_array)
predicted_class_index = np.argmax(pred, axis=1)[0]

# ---- Get class names (from training) ----
class_names = [
    "Black_Gum-Tupelo",
    "Eastern_Redbud",
    "Loblolly_Pine",
    "Pignut_Hickory",
    "Red_Maple",
    "Southern_Magnolia",
    "Sweetgum",
    "Tulip_Poplar",
    "White_Oak",
    "Willow_Oak",
]

print("Prediction vector:", pred)
print("Predicted class index:", predicted_class_index)
print("Predicted class name:", class_names[predicted_class_index])
