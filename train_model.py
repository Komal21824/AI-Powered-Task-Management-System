import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load dataset
df = pd.read_csv("dataset/large_task_dataset.csv")

# Clean nulls
df.dropna(inplace=True)

# Task type model
task_pipe = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])
task_pipe.fit(df["task"], df["task_type"])

# Priority model
priority_pipe = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])
priority_pipe.fit(df["task"], df["priority"])

# Save models
with open("task_classifier.pkl", "wb") as f:
    pickle.dump(task_pipe, f)

with open("priority_classifier.pkl", "wb") as f:
    pickle.dump(priority_pipe, f)

print("✅ Models trained and saved successfully.")
