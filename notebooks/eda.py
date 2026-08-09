import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("screenshots", exist_ok=True)

df = pd.read_csv("data/customer_churn_dataset-training-master.csv")

print("First rows:")
print(df.head())

print("\nDataset info:")
print(df.info())

print("\nSummary statistics:")
print(df.describe())


plt.figure(figsize=(6, 4))
sns.countplot(x="Churn", data=df)
plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("screenshots/churn_distribution.png")
plt.close()


plt.figure(figsize=(8, 5))
sns.histplot(df["Age"], bins=20, kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("screenshots/age_distribution.png")
plt.close()


numeric_df = df.select_dtypes(include=["float64", "int64"])

plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("screenshots/correlation_heatmap.png")
plt.close()

print("EDA charts saved successfully.")
print(df.head())