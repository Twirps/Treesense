"""
Check model.json structure for issues that could cause hanging
"""
import json

model_json_path = "../public/model_tfjs/model.json"

print("🔍 Checking model structure for issues...")
print("=" * 60)

with open(model_json_path, 'r', encoding='utf-8') as f:
    model_json = json.load(f)

layers = model_json["modelTopology"]["model_config"]["config"]["layers"]
print(f"Total layers: {len(layers)}")

# Check for problematic inbound_nodes
issues = []
for i, layer in enumerate(layers):
    if "inbound_nodes" not in layer:
        continue
    
    for node_group in layer["inbound_nodes"]:
        if isinstance(node_group, list):
            for node_item in node_group:
                if not isinstance(node_item, list):
                    issues.append(f"Layer {i} ({layer.get('name', 'unknown')}): nodeData is not a list")
                elif len(node_item) != 3:
                    issues.append(f"Layer {i} ({layer.get('name', 'unknown')}): nodeData has wrong length: {len(node_item)}")
                elif not isinstance(node_item[0], str):
                    issues.append(f"Layer {i} ({layer.get('name', 'unknown')}): nodeData[0] is not a string")
        elif isinstance(node_group, dict):
            issues.append(f"Layer {i} ({layer.get('name', 'unknown')}): nodeGroup is still a dict (Keras 3 format)")

print(f"\nFound {len(issues)} structural issues")
if issues:
    print("\nFirst 10 issues:")
    for issue in issues[:10]:
        print(f"  ❌ {issue}")
    print("\n⚠️  These issues can cause the model to hang during compilation!")
    print("   Run fix_model_complete_final.py to fix them.")
else:
    print("✅ No obvious structural issues found")
    print("   The hang might be due to model size/complexity")

print("\n" + "=" * 60)

