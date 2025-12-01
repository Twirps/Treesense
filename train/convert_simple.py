"""
Simple model conversion that avoids tensorflow_hub import issues
"""
import tensorflow as tf
import json
import os

# Load model
print("Loading Keras model...")
model = tf.keras.models.load_model("model.keras")
print(f"Model input shape: {model.input_shape}")

# Save as SavedModel first (avoids tensorflowjs import issues)
print("\nSaving as SavedModel...")
saved_model_dir = "saved_model_temp"
if os.path.exists(saved_model_dir):
    import shutil
    shutil.rmtree(saved_model_dir)
tf.saved_model.save(model, saved_model_dir)
print("✅ SavedModel created")

# Now use command line converter
print("\nConverting SavedModel to TensorFlow.js...")
print("Run this command manually:")
print(f'  tensorflowjs_converter --input_format=tf_saved_model --output_format=tfjs_layers_model "{saved_model_dir}" "../public/model_tfjs"')
print("\nOr use the Python API directly...")

# Try direct conversion without tensorflowjs imports
try:
    # Import only what we need
    from tensorflowjs.converters import keras_h5_conversion
    import tempfile
    
    # Save model as H5 temporarily
    h5_path = "model_temp.h5"
    model.save(h5_path)
    print(f"\n✅ Saved as H5: {h5_path}")
    
    # Convert using the converter
    print("Converting H5 to TensorFlow.js...")
    keras_h5_conversion.h5_to_tfjs_graph_model(
        h5_path,
        "../public/model_tfjs",
        quantization_dtype=None
    )
    print("✅ Conversion complete!")
    
    # Cleanup
    os.remove(h5_path)
    
except Exception as e:
    print(f"\n❌ Direct conversion failed: {e}")
    print("\nPlease run the tensorflowjs_converter command manually (see above)")

