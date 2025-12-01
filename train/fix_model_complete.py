"""
Complete fix for model.json - fixes ALL nodeData issues
"""
import json
import shutil

model_json_path = "../public/model_tfjs/model.json"
backup_path = "../public/model_tfjs/model.json.backup2"

print("🔧 Complete model.json fix...")

# Backup
shutil.copy2(model_json_path, backup_path)
print(f"✅ Backup: {backup_path}")

# Load
with open(model_json_path, 'r', encoding='utf-8') as f:
    model_json = json.load(f)

# Fix 1: InputLayer input_shape
layers = model_json["modelTopology"]["model_config"]["config"]["layers"]
if layers[0]["class_name"] == "InputLayer":
    config = layers[0]["config"]
    if "batch_shape" in config and "input_shape" not in config:
        bs = config["batch_shape"]
        config["input_shape"] = [bs[1], bs[2], bs[3]]
        print("✅ Added input_shape")

# Fix 2: Fix ALL inbound_nodes - more aggressive
def fix_all_inbound_nodes(layers_list):
    """Fix inbound_nodes in all layers"""
    for layer in layers_list:
        if "inbound_nodes" in layer:
            fixed_nodes = []
            for node_group in layer["inbound_nodes"]:
                if isinstance(node_group, list):
                    fixed_group = []
                    for item in node_group:
                        if isinstance(item, dict):
                            # Object -> convert to array
                            name = item.get("layer_name") or item.get("name") or item.get(0) or ""
                            idx = item.get("node_index") if "node_index" in item else (item.get(1) if isinstance(item.get(1), int) else 0)
                            tidx = item.get("tensor_index") if "tensor_index" in item else (item.get(2) if isinstance(item.get(2), int) else 0)
                            fixed_group.append([name, idx, tidx])
                        elif isinstance(item, list):
                            # Already array, keep it
                            fixed_group.append(item[:3] if len(item) >= 3 else [item[0] if len(item) > 0 else "", item[1] if len(item) > 1 else 0, item[2] if len(item) > 2 else 0])
                        else:
                            fixed_group.append(item)
                    fixed_nodes.append(fixed_group)
                else:
                    fixed_nodes.append(node_group)
            layer["inbound_nodes"] = fixed_nodes

fix_all_inbound_nodes(layers)
print("✅ Fixed all inbound_nodes")

# Save
with open(model_json_path, 'w', encoding='utf-8') as f:
    json.dump(model_json, f, separators=(',', ':'))

print(f"\n✅ Fixed model.json")
print("Restart dev server and try again!")

