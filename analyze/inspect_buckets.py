import os
import pandas as pd
import collections
import tqdm

import pymongo
from pymongo import MongoClient


mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
db = client.deep_learning

db.metrics.create_index([("run_name", pymongo.ASCENDING), ("epoch_idx", pymongo.ASCENDING)])

local_collection = collections.defaultdict(list)

run_names = db.metrics.find().distinct('run_name')

buckets = [
    ("0.2.0", [1, 2, 3, 4, 5, 6]),
    ("0.2.1", [7, 8, 9, 10, 11, 12]),
]

for run_name in run_names:
    model_name, run_number = run_name.split('/')
    run_number = int(run_number)

    bucket_number = None
    bucket_name = None

    for idx, (name, contents) in enumerate(buckets):
        if run_number in contents:
            bucket_number = idx
            bucket_name = name

    assert bucket_number is not None

    local_collection[model_name].append({
        'run_name': run_name,
        'run_number': run_number,
        'bucket_name': bucket_name,
        'bucket_number': bucket_number
    })


def safe_mean(data):
    if len(data) > 2:
        return data.sort_values().iloc[1:-1].mean()
    else:
        return data.mean()


fps_aggregation = list(db.metrics.aggregate([{'$group': {"_id": '$run_name', "fps": {"$avg": "$fps"}}}]))
fps_frame = pd.DataFrame(fps_aggregation).set_index('_id').fps.sort_index()

last_entries = []

for name in tqdm.tqdm(run_names):
    item = list(db.metrics.find({'run_name': name}).sort([('epoch_idx', pymongo.DESCENDING)]).limit(1))
    last_entries.append({'run_name': item[0]['run_name'], 'score': item[0]['PMM:episode_rewards']})

score_frame = pd.DataFrame(last_entries).set_index('run_name').score.sort_index()

sorted_names = sorted(local_collection)

for name in sorted_names:
    print(f"======================== {name} ====================")
    contents = local_collection[name]

    model_frame = pd.DataFrame([
        {
            'bucket': element['bucket_name'],
            'fps': fps_frame.loc[element['run_name']],
            'run_name': element['run_name'],
            'score': score_frame.loc[element['run_name']]
        } for element in contents
    ])

    print("FPS:")
    print(model_frame.groupby('bucket').fps.apply(safe_mean))
    print()

    print("Score:")
    print(model_frame.groupby('bucket').score.apply(safe_mean))
    print()

