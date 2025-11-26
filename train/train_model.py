import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import json
import os
import matplotlib.pyplot as plt


# -----------------------------
# CONFIG
# -----------------------------
DATASET_DIR = "../dataset"   # relative to train/train_model.py
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20


# -----------------------------
# Load Class Names
# -----------------------------
class_names = sorted(os.listdir(DATASET_DIR))
class_names = [c for c in class_names if os.path.isdir(os.path.join(DATASET_DIR, c))]

print("Detected Classes:")
for c in class_names:
    print(" -", c)

num_classes = len(class_names)

# Save class mapping for web frontend
with open("class_mapping.json", "w") as f:
    json.dump({i: name for i, name in enumerate(class_names)}, f, indent=4)


# -----------------------------
# Data Generators
# -----------------------------
datagen = ImageDataGenerator(
    rescale=1/255.0,
    validation_split=0.30,
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.1,
    horizontal_flip=True,
)

train_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    subset="training",
    class_mode="categorical"
)

val_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    subset="validation",
    class_mode="categorical"
)


# -----------------------------
# Build Model (MobileNetV2 Transfer Learning)
# -----------------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(*IMAGE_SIZE, 3)
)

base_model.trainable = False  # freeze base weights

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
output = Dense(num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()


# -----------------------------
# Callbacks
# -----------------------------
checkpoint = ModelCheckpoint(
    "model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

early_stop = EarlyStopping(
    monitor="val_accuracy",
    patience=5,
    restore_best_weights=True
)


# -----------------------------
# Train Model
# -----------------------------
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=[checkpoint, early_stop]
)


# -----------------------------
# Plot & Save Training Graph
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(history.history["accuracy"], label="Train Accuracy")
plt.plot(history.history["val_accuracy"], label="Val Accuracy")
plt.title("Model Accuracy Over Time")
plt.legend()
plt.savefig("history_plot.png")
plt.close()

print("\nTraining complete! Model saved as model.keras")
