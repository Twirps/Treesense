"""
Fix model.json file to add input_shape and fix structure issues.
This works without needing TensorFlow - just fixes the JSON structure.
"""
import json
import os
import shutil

# Paths
model_json_path = "../public/model_tfjs/model.json"
backup_path = "../public/model_tfjs/model.json.backup"

print("🔧 Fixing model.json structure...")

# Create backup
if os.path.exists(model_json_path):
    shutil.copy2(model_json_path, backup_path)
    print(f"✅ Created backup: {backup_path}")
else:
    print(f"❌ Error: {model_json_path} not found!")
    exit(1)

# Load model.json
with open(model_json_path, 'r') as f:
    model_json = json.load(f)

# Fix 1: Add input_shape to InputLayer
if model_json.get("modelTopology") and model_json["modelTopology"].get("model_config"):
    layers = model_json["modelTopology"]["model_config"]["config"]["layers"]
    if layers and layers[0].get("class_name") == "InputLayer":
        input_layer = layers[0]
        config = input_layer.get("config", {})
        
        if config.get("batch_shape") and not config.get("input_shape"):
            batch_shape = config["batch_shape"]
            if batch_shape and len(batch_shape) == 4:
                # Extract input_shape from batch_shape (remove batch dimension)
                config["input_shape"] = [batch_shape[1], batch_shape[2], batch_shape[3]]
                print(f"✅ Added input_shape: {config['input_shape']}")
        
        # Ensure batch_shape is correct too
        if config.get("batch_shape"):
            batch_shape = config["batch_shape"]
            if batch_shape[1] == 224 or batch_shape[2] == 224:
                # Model expects 224x224, so keep it
                print(f"   Model batch_shape: {batch_shape}")

# Fix 2: Ensure inbound_nodes have proper structure (arrays, not objects)
def fix_inbound_nodes(obj):
    """Recursively fix inbound_nodes structure"""
    if isinstance(obj, dict):
        fixed = {}
        for key, value in obj.items():
            if key == "inbound_nodes" and isinstance(value, list):
                # Fix inbound_nodes: ensure nodeData is always an array
                fixed[key] = []
                for node_group in value:
                    if isinstance(node_group, list):
                        fixed_node_group = []
                        for node_data in node_group:
                            if isinstance(node_data, dict):
                                # Convert object to array [layer_name, node_index, tensor_index]
                                layer_name = node_data.get("layer_name") or node_data.get("name") or ""
                                node_index = node_data.get("node_index", node_data.get(1, 0))
                                tensor_index = node_data.get("tensor_index", node_data.get(2, 0))
                                fixed_node_group.append([layer_name, node_index, tensor_index])
                            elif isinstance(node_data, list):
                                # Already an array, ensure it has 3 elements
                                if len(node_data) >= 3:
                                    fixed_node_group.append(node_data[:3])
                                else:
                                    fixed_node_group.append([node_data[0] if len(node_data) > 0 else "", 
                                                           node_data[1] if len(node_data) > 1 else 0,
                                                           node_data[2] if len(node_data) > 2 else 0])
                            else:
                                fixed_node_group.append(node_data)
                        fixed[key].append(fixed_node_group)
                    else:
                        fixed[key].append(node_group)
            else:
                fixed[key] = fix_inbound_nodes(value)
        return fixed
    elif isinstance(obj, list):
        return [fix_inbound_nodes(item) for item in obj]
    else:
        return obj

print("🔧 Fixing inbound_nodes structure...")
model_json["modelTopology"] = fix_inbound_nodes(model_json["modelTopology"])
print("✅ Fixed inbound_nodes structure")

# Save fixed model.json
with open(model_json_path, 'w') as f:
    json.dump(model_json, f, indent=2)

print(f"\n✅ Fixed model.json saved to: {model_json_path}")
print("\nNext steps:")
print("1. Restart your dev server")
print("2. Try uploading an image again")
print(f"3. If something goes wrong, restore from backup: {backup_path}")

