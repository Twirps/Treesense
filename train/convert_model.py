"""
Convert Keras model to TensorFlow.js format with correct input shape.
Run this script to regenerate the model_tfjs files with the correct 160x160 input shape.
"""
import tensorflow as tf
import tensorflowjs as tfjs

# Load the trained model
print("Loading Keras model...")
model = tf.keras.models.load_model("model.keras")

# Verify input shape
print(f"Model input shape: {model.input_shape}")
print(f"Expected input shape: (None, 160, 160, 3)")

# Convert to TensorFlow.js
print("\nConverting to TensorFlow.js format...")
print("This will create/overwrite files in ../public/model_tfjs/")

tfjs.converters.save_keras_model(
    model,
    "../public/model_tfjs",
    quantization_dtype=None  # Use float32 for better accuracy
)

print("\n✅ Conversion complete!")
print("Model files saved to: ../public/model_tfjs/")
print("\nNext steps:")
print("1. Make sure class_mapping.json is in ../public/model_tfjs/")
print("2. Restart your dev server")
print("3. Try uploading an image again")

