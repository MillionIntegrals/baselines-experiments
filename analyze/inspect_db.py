import os
import pandas as pd

from pymongo import MongoClient


mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
db = client.deep_learning

# Just get all metrics
metrics = list(db.metrics.find())

data_frame = pd.DataFrame(metrics)
data_count = data_frame.groupby('run_name')['PMM:episode_rewards'].count()

print("==============================================================")
print("Data count:")
print(data_count.to_string())

print("==============================================================")
print("FPS:")
print(data_frame.groupby('run_name').fps.mean().to_string())

print("==============================================================")
last_rows = data_frame.set_index(['run_name', 'epoch_idx']).sort_index().groupby(level=0).last()
print("Last rewards:")
print(last_rows['PMM:episode_rewards'].to_string())


def safe_mean(data):
    if len(data) > 2:
        return data.sort_values().iloc[1:-1].mean()
    else:
        return data.mean()


print("==============================================================")
print("Per-model means:")
print(last_rows.groupby('model_name')['PMM:episode_rewards'].apply(safe_mean).to_string())
