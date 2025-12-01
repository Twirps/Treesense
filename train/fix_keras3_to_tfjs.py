"""
Convert Keras 3.x inbound_nodes format to TensorFlow.js compatible format
"""
import json
import shutil

model_json_path = "../public/model_tfjs/model.json"
backup_path = "../public/model_tfjs/model.json.backup3"

print("🔧 Converting Keras 3.x format to TensorFlow.js format...")

# Backup
shutil.copy2(model_json_path, backup_path)
print(f"✅ Backup: {backup_path}")

# Load
with open(model_json_path, 'r', encoding='utf-8') as f:
    model_json = json.load(f)

layers = model_json["modelTopology"]["model_config"]["config"]["layers"]
fixed_count = 0

# Fix InputLayer input_shape
if layers[0]["class_name"] == "InputLayer":
    config = layers[0]["config"]
    if "batch_shape" in config and "input_shape" not in config:
        bs = config["batch_shape"]
        config["input_shape"] = [bs[1], bs[2], bs[3]]
        print("✅ Added input_shape to InputLayer")

# Fix all inbound_nodes from Keras 3 format to TF.js format
for i, layer in enumerate(layers):
    if "inbound_nodes" in layer and layer["inbound_nodes"]:
        # Keras 3 format: [{'args': [{'keras_history': ['layer', 0, 0]}], 'kwargs': {}}]
        # TF.js format: [['layer', 0, 0]]
        new_nodes = []
        for node_entry in layer["inbound_nodes"]:
            if isinstance(node_entry, dict) and "args" in node_entry:
                # Keras 3 format - extract from args
                node_list = []
                for arg in node_entry.get("args", []):
                    if isinstance(arg, dict) and "keras_history" in arg.get("config", {}):
                        kh = arg["config"]["keras_history"]
                        if isinstance(kh, list) and len(kh) >= 3:
                            node_list.append([kh[0], kh[1], kh[2]])
                    elif isinstance(arg, dict) and "keras_history" in arg:
                        kh = arg["keras_history"]
                        if isinstance(kh, list) and len(kh) >= 3:
                            node_list.append([kh[0], kh[1], kh[2]])
                if node_list:
                    new_nodes.append(node_list)
                else:
                    # Fallback: empty array
                    new_nodes.append([])
            elif isinstance(node_entry, list):
                # Already in array format, check if needs fixing
                fixed_entry = []
                for item in node_entry:
                    if isinstance(item, dict):
                        # Try to extract from keras_history
                        kh = item.get("keras_history") or item.get("config", {}).get("keras_history")
                        if kh and isinstance(kh, list) and len(kh) >= 3:
                            fixed_entry.append([kh[0], kh[1], kh[2]])
                        else:
                            # Try other formats
                            name = item.get("layer_name") or item.get("name") or ""
                            idx = item.get("node_index", 0)
                            tidx = item.get("tensor_index", 0)
                            fixed_entry.append([name, idx, tidx])
                    elif isinstance(item, list):
                        fixed_entry.append(item[:3] if len(item) >= 3 else item)
                    else:
                        fixed_entry.append(item)
                new_nodes.append(fixed_entry)
            else:
                new_nodes.append([])
        
        layer["inbound_nodes"] = new_nodes
        fixed_count += 1

print(f"✅ Fixed {fixed_count} layers with inbound_nodes")

# Save (compact format to match original)
with open(model_json_path, 'w', encoding='utf-8') as f:
    json.dump(model_json, f, separators=(',', ':'))

print(f"\n✅ Conversion complete!")
print("Restart dev server and test!")

