import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("deliveries.csv")

# ---------------- FEATURES ----------------
df['runs_cum'] = df.groupby('match_id')['total_runs'].cumsum()
df['balls'] = df.groupby('match_id').cumcount() + 1
df['overs'] = df['balls'] / 6
df['wickets'] = df.groupby('match_id')['is_wicket'].cumsum()

df['run_rate'] = df['runs_cum'] / df['overs']
df['run_rate'].fillna(0, inplace=True)

# ---------------- TARGET (REAL LOGIC) ----------------
# Final score of each match
final_scores = df.groupby('match_id')['runs_cum'].max().reset_index()
final_scores.rename(columns={'runs_cum': 'final_score'}, inplace=True)

df = df.merge(final_scores, on='match_id')

# If current score reaches final score → win-like progression
df['target'] = (df['runs_cum'] >= df['final_score']).astype(int)

# ---------------- TRAIN ----------------
X = df[['runs_cum', 'wickets', 'overs', 'run_rate']]
y = df['target']

model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("✅ FIXED model trained")