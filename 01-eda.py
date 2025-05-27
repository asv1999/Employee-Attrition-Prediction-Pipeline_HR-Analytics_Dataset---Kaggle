import pandas as pd
from config import DATA_RAW

df = pd.read_csv(DATA_RAW)
# EDA code here
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data_path = Path("data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv")
df = pd.read_csv(data_path)

# Create a few plots for EDA and save them
eda_output_dir = Path("notebooks/exploratory")
eda_output_dir.mkdir(parents=True, exist_ok=True)

# Distribution of Attrition
plt.figure(figsize=(6, 4))
sns.countplot(x="Attrition", data=df)
plt.title("Attrition Distribution")
plt.savefig(eda_output_dir / "attrition_distribution.png")
plt.close()

# Heatmap of Correlation Matrix
plt.figure(figsize=(12, 10))
corr = df.select_dtypes(include='number').corr()
sns.heatmap(corr, cmap="coolwarm", annot=False)
plt.title("Correlation Heatmap")
plt.savefig(eda_output_dir / "correlation_heatmap.png")
plt.close()

# Boxplot for Age vs Monthly Income grouped by Attrition
plt.figure(figsize=(10, 6))
sns.boxplot(x="Attrition", y="MonthlyIncome", data=df)
plt.title("Monthly Income by Attrition")
plt.savefig(eda_output_dir / "income_by_attrition.png")
plt.close()

# Summary statistics
summary_stats = df.describe(include='all').transpose()
summary_stats.to_csv(eda_output_dir / "summary_statistics.csv")

import ace_tools as tools; tools.display_dataframe_to_user(name="Summary Statistics", dataframe=summary_stats)
