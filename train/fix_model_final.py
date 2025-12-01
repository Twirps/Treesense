"""
Final comprehensive fix for model.json - ensures TensorFlow.js compatibility
"""
import json
import shutil

model_json_path = "../public/model_tfjs/model.json"
backup_path = "../public/model_tfjs/model.json.backup_final"

print("🔧 Final comprehensive model.json fix...")

# Backup
shutil.copy2(model_json_path, backup_path)
print(f"✅ Backup: {backup_path}")

# Load
with open(model_json_path, 'r', encoding='utf-8') as f:
    model_json = json.load(f)

layers = model_json["modelTopology"]["model_config"]["config"]["layers"]
fixed_count = 0

# Fix 1: InputLayer
if layers[0]["class_name"] == "InputLayer":
    config = layers[0]["config"]
    if "batch_shape" in config:
        bs = config["batch_shape"]
        if "input_shape" not in config:
            config["input_shape"] = [bs[1], bs[2], bs[3]]
        print("✅ Fixed InputLayer")

# Fix 2: Convert ALL inbound_nodes to proper format
print("🔧 Fixing inbound_nodes in all layers...")
for i, layer in enumerate(layers):
    if "inbound_nodes" not in layer:
        continue
    
    new_nodes = []
    for node_entry in layer["inbound_nodes"]:
        if isinstance(node_entry, list):
            # Already an array of arrays
            fixed_entry = []
            for item in node_entry:
                if isinstance(item, list) and len(item) >= 3:
                    # Ensure it's [name, node_idx, tensor_idx]
                    fixed_entry.append([str(item[0]), int(item[1]) if isinstance(item[1], (int, float)) else 0, int(item[2]) if isinstance(item[2], (int, float)) else 0])
                elif isinstance(item, dict):
                    # Convert dict to array
                    name = str(item.get("layer_name") or item.get("name") or item.get(0) or "")
                    nidx = int(item.get("node_index") or item.get(1) or 0)
                    tidx = int(item.get("tensor_index") or item.get(2) or 0)
                    fixed_entry.append([name, nidx, tidx])
                else:
                    fixed_entry.append(item)
            new_nodes.append(fixed_entry)
        elif isinstance(node_entry, dict):
            # Keras 3 format - extract from args/keras_history
            fixed_entry = []
            for arg in node_entry.get("args", []):
                if isinstance(arg, dict):
                    kh = arg.get("config", {}).get("keras_history") or arg.get("keras_history")
                    if kh and isinstance(kh, list) and len(kh) >= 3:
                        fixed_entry.append([str(kh[0]), int(kh[1]), int(kh[2])])
            if fixed_entry:
                new_nodes.append(fixed_entry)
            else:
                new_nodes.append([])
        else:
            new_nodes.append([])
    
    layer["inbound_nodes"] = new_nodes
    fixed_count += 1

print(f"✅ Fixed {fixed_count} layers")

# Fix 3: Ensure weightsManifest structure is correct
if "weightsManifest" in model_json:
    print("✅ Weights manifest present")
    for manifest in model_json["weightsManifest"]:
        if "paths" in manifest:
            print(f"   Found {len(manifest['paths'])} weight files")

# Save (compact format)
with open(model_json_path, 'w', encoding='utf-8') as f:
    json.dump(model_json, f, separators=(',', ':'))

print(f"\n✅ Fixed model.json saved")
print("Restart dev server and test!")

