import os
import pandas as pd

from pymongo import MongoClient


mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
db = client.deep_learning

# Just get all metrics
metrics = list(db.metrics.find())

data_frame = pd.DataFrame(metrics)
data_count = data_frame.groupby('run_name').value_loss.count()

print("==============================================================")
print("Data count:")
print(data_count)

print("==============================================================")
print("FPS:")
print(data_frame.groupby('run_name').fps.mean())

print("==============================================================")
print("Max rewards:")
print(data_frame.groupby('run_name')['PMM:episode_rewards'].max())
