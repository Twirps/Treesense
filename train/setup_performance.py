import matplotlib.pyplot as plt

train_acc = 0.92
val_acc = 0.64

plt.figure(figsize=(6,4))
plt.bar(["Training Accuracy", "Validation Accuracy"], [train_acc, val_acc])
plt.ylim(0,1)
plt.title("Final Model Accuracy")
plt.ylabel("Accuracy")
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.savefig("accuracy_comparison.png", dpi=300, bbox_inches="tight")
plt.show()
