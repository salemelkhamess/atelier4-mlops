import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier


def main():
    # Outputs tracked by DVC
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    # 1) Generate an imbalanced churn-like dataset
    X, y = make_classification(
        n_samples=2000,
        n_features=20,
        weights=[0.9, 0.1],
        random_state=42,
    )

    df = pd.DataFrame(X, columns=[f"f{i}" for i in range(X.shape[1])])
    df["target"] = y
    df.to_csv("data/dataset.csv", index=False)

    # 2) Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3) Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # 4) Evaluate
    pred = model.predict(X_test)
    report = classification_report(y_test, pred)

    # 5) Save model + metrics + confusion matrix
    joblib.dump(model, "models/model.pkl")

    with open("models/metrics.txt", "w", encoding="utf-8") as f:
        f.write(report)

    cm = confusion_matrix(y_test, pred)

    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig("models/conf_matrix.png")
    plt.close()

    print("✅ Training done. Outputs written to data/ and models/.")


if __name__ == "__main__":
    main()
