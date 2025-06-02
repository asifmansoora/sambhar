import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data
n_rows = 1000

# Generate dates
base_date = datetime(2023, 1, 1)
dates = [base_date + timedelta(days=x) for x in range(n_rows)]

# Generate numeric data
numeric_normal = np.random.normal(100, 15, n_rows)  # Normal distribution
numeric_uniform = np.random.uniform(0, 1000, n_rows)  # Uniform distribution
integers = np.random.randint(1, 100, n_rows)

# Generate categorical data
categories = ['A', 'B', 'C', 'D', 'E']
categorical = np.random.choice(categories, n_rows, p=[0.3, 0.25, 0.2, 0.15, 0.1])

# Generate boolean data
boolean = np.random.choice([True, False], n_rows)

# Generate text data
text_options = [
    "High performance",
    "Medium performance",
    "Low performance",
    "Needs improvement",
    "Excellent"
]
text_data = np.random.choice(text_options, n_rows)

# Create missing values
numeric_with_missing = numeric_normal.copy()
missing_indices = np.random.choice(n_rows, size=int(n_rows * 0.1), replace=False)
numeric_with_missing[missing_indices] = np.nan

# Create DataFrame
df = pd.DataFrame({
    'date': dates,
    'numeric_normal': numeric_normal,
    'numeric_uniform': numeric_uniform,
    'numeric_with_missing': numeric_with_missing,
    'integer': integers,
    'category': categorical,
    'boolean': boolean,
    'text': text_data
})

# Convert category column to categorical type
df['category'] = df['category'].astype('category')

# Save as parquet file
output_file = 'sample_data.parquet'
df.to_parquet(output_file, index=False)

print(f"Generated {output_file} with {n_rows} rows")
print("\nDataset Summary:")
print(df.info())
print("\nFirst few rows:")
print(df.head()) 