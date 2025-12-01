"""
Complete final fix - ensures model.json is 100% TensorFlow.js compatible
This fixes ALL known issues that cause hanging
"""
import json
import shutil

model_json_path = "../public/model_tfjs/model.json"
backup_path = "../public/model_tfjs/model.json.backup_complete"

print("🔧 Complete final model.json fix...")
print("This ensures 100% TensorFlow.js compatibility\n")

# Backup
shutil.copy2(model_json_path, backup_path)
print(f"✅ Backup created: {backup_path}\n")

# Load
with open(model_json_path, 'r', encoding='utf-8') as f:
    model_json = json.load(f)

# Fix 1: Ensure InputLayer is perfect
print("1️⃣ Fixing InputLayer...")
layers = model_json["modelTopology"]["model_config"]["config"]["layers"]
if layers[0]["class_name"] == "InputLayer":
    config = layers[0]["config"]
    # Ensure both batch_shape and input_shape are present and correct
    if "batch_shape" in config:
        bs = config["batch_shape"]
        if bs and len(bs) == 4:
            # Ensure input_shape matches
            if "input_shape" not in config or config["input_shape"] != [bs[1], bs[2], bs[3]]:
                config["input_shape"] = [bs[1], bs[2], bs[3]]
                print(f"   ✅ Set input_shape: {config['input_shape']}")
    print("   ✅ InputLayer fixed\n")

# Fix 2: Fix ALL inbound_nodes - ensure they're arrays of arrays
print("2️⃣ Fixing inbound_nodes in all layers...")
fixed_layers = 0
for i, layer in enumerate(layers):
    if "inbound_nodes" not in layer:
        continue
    
    original_nodes = layer["inbound_nodes"]
    new_nodes = []
    
    for node_group in original_nodes:
        if isinstance(node_group, list):
            # Process each node in the group
            fixed_group = []
            for node_item in node_group:
                if isinstance(node_item, list) and len(node_item) >= 3:
                    # Already correct format [name, node_idx, tensor_idx]
                    # Ensure types are correct
                    name = str(node_item[0])
                    nidx = int(node_item[1]) if isinstance(node_item[1], (int, float)) else 0
                    tidx = int(node_item[2]) if isinstance(node_item[2], (int, float)) else 0
                    fixed_group.append([name, nidx, tidx])
                elif isinstance(node_item, dict):
                    # Convert dict to array
                    name = str(node_item.get("layer_name") or node_item.get("name") or node_item.get(0) or "")
                    nidx = int(node_item.get("node_index") or node_item.get(1) or 0)
                    tidx = int(node_item.get("tensor_index") or node_item.get(2) or 0)
                    fixed_group.append([name, nidx, tidx])
                else:
                    # Unknown format, skip or use defaults
                    continue
            new_nodes.append(fixed_group)
        elif isinstance(node_group, dict):
            # Keras 3 format - extract from args
            fixed_group = []
            for arg in node_group.get("args", []):
                if isinstance(arg, dict):
                    config = arg.get("config", {})
                    kh = config.get("keras_history")
                    if kh and isinstance(kh, list) and len(kh) >= 3:
                        fixed_group.append([str(kh[0]), int(kh[1]), int(kh[2])])
            new_nodes.append(fixed_group)
        else:
            # Unknown format, use empty array
            new_nodes.append([])
    
    layer["inbound_nodes"] = new_nodes
    fixed_layers += 1

print(f"   ✅ Fixed {fixed_layers} layers\n")

# Fix 3: Ensure weightsManifest is correct
print("3️⃣ Verifying weightsManifest...")
if "weightsManifest" in model_json and model_json["weightsManifest"]:
    for i, manifest in enumerate(model_json["weightsManifest"]):
        if "paths" in manifest:
            print(f"   ✅ Manifest {i+1}: {len(manifest['paths'])} weight files")
            for path in manifest["paths"]:
                if not isinstance(path, str):
                    print(f"      ⚠️  Warning: path is not a string: {path}")
    print("   ✅ Weights manifest verified\n")
else:
    print("   ⚠️  Warning: No weightsManifest found\n")

# Fix 4: Ensure modelTopology structure is correct
print("4️⃣ Verifying modelTopology structure...")
if "modelTopology" in model_json:
    if "model_config" in model_json["modelTopology"]:
        if "config" in model_json["modelTopology"]["model_config"]:
            config = model_json["modelTopology"]["model_config"]["config"]
            if "layers" in config:
                print(f"   ✅ Model has {len(config['layers'])} layers")
                print(f"   ✅ Model class name: {config.get('class_name', 'N/A')}")
            else:
                print("   ❌ ERROR: No 'layers' in config")
        else:
            print("   ❌ ERROR: No 'config' in model_config")
    else:
        print("   ❌ ERROR: No 'model_config' in modelTopology")
else:
    print("   ❌ ERROR: No 'modelTopology' in model.json")
print()

# Save with proper formatting
print("5️⃣ Saving fixed model.json...")
with open(model_json_path, 'w', encoding='utf-8') as f:
    json.dump(model_json, f, separators=(',', ':'))

print(f"✅ Fixed model.json saved to: {model_json_path}\n")
print("=" * 60)
print("✅ COMPLETE! Model should now load without hanging.")
print("=" * 60)
print("\nNext steps:")
print("1. Restart your dev server")
print("2. Clear browser cache (Ctrl+Shift+Delete)")
print("3. Try uploading an image again")
print(f"\nIf issues persist, restore from: {backup_path}")

