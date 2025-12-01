import tensorflow as tf
import numpy as np
import json
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# ---- Load Model ----
model = tf.keras.models.load_model("model.keras")

# ---- Load class mapping from JSON ----
with open("class_mapping.json", "r") as f:
    class_map = json.load(f)

class_names = [class_map[str(i)] for i in range(len(class_map))]
print("Loaded class names:", class_names)

# ---- Path to test image ----
img_path = "test_images/loblolly_pine.jpg"

# ---- Preprocess image ----
img = image.load_img(img_path, target_size=(160, 160))
img_array = image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)
img_array = img_array / 255.0

# ---- Predict ----
pred = model.predict(img_array)[0]

# ---- Top 3 predictions ----
top3_indices = pred.argsort()[-3:][::-1]
top3_conf = pred[top3_indices]

print("\n🔍 Top 3 Predictions")
for i, idx in enumerate(top3_indices):
    print(f"{i+1}. {class_names[idx]} — {top3_conf[i]*100:.2f}%")

best_idx = top3_indices[0]
print("\n🎯 Best Prediction:", class_names[best_idx])
print(f"Confidence: {top3_conf[0]*100:.2f}%")

# ---- Augmentation Visualization ----
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1/255.0,
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.1,
    horizontal_flip=True,
)

# Create 5 augmented samples
aug_images = datagen.flow(
    np.expand_dims(image.img_to_array(image.load_img(img_path, target_size=(160,160))), 0),
    batch_size=1
)

plt.figure(figsize=(10,4))
for i in range(5):
    batch = next(aug_images)[0]
    plt.subplot(1,5,i+1)
    plt.imshow(batch)
    plt.axis('off')

plt.tight_layout()
plt.savefig("augmentation_examples.png")
plt.close()

print("\n📸 Saved augmented examples to augmentation_examples.png")
