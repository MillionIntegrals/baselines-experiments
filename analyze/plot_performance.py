import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

from pymongo import MongoClient


mongodb_url = os.environ['MONGODB_URL']

# name = 'beamrider'
# title = "Beam Rider"

# name = 'spaceinvaders'
# title = "Space Invaders"

name = 'breakout'
title = "Breakout"

client = MongoClient(mongodb_url)
db = client.deep_learning


def save_metric(name, title):
    # Just get all metrics
    metrics = list(db.metrics.find({'model_name': {'$regex': '^' + name}}, ['frames', 'run_name', 'PMM:episode_rewards']))

    data_frame = pd.DataFrame(metrics)

    run_performance = (
        data_frame
        .drop('_id', axis=1)
        .sort_values(['run_name', 'frames'])
        .set_index(['run_name', 'frames'])['PMM:episode_rewards']
    )

    run_names = sorted(set(run_performance.index.get_level_values(0)))
    model_names = sorted(set(x.split('/')[0] for x in run_names if 'trpo_oai' not in x))

    result_names = []
    results = []

    for model_name in model_names:
        relevant_run_names = [x for x in run_names if x.startswith(model_name)]

        local_results = []

        for rn in relevant_run_names:
            super_local = run_performance.loc[rn]
            super_local = super_local.loc[~super_local.index.duplicated(keep='first')]
            local_results.append(super_local)

        local_frame = pd.concat(local_results, axis=1).fillna(method='ffill').fillna(0.0)
        local_frame = local_frame.loc[~local_frame.index.duplicated(keep='first')]
        local_frame = local_frame.loc[local_frame.index < 10_000_000]

        result_names.append(model_name)
        results.append(pd.DataFrame({'mean': local_frame.mean(axis=1), 'std': local_frame.std(axis=1)}))

    common_index = sorted({y for x in results for y in x.index})

    final_frame = (
        pd.concat([x.reindex(common_index) for x in results], axis=1, keys=result_names)
        .interpolate().fillna(0.0).swaplevel(0, 1, axis=1)
    )

    seaborn.set('poster')

    fig, ax = plt.subplots(1, 1, figsize=(15, 10), dpi=80)
    ax.set_title(title)
    ax.set_xlabel("Frames")
    ax.set_ylabel("Score")

    for model_name in model_names:
        label = model_name.split('_')[1]

        if label in {'cheetah', 'pendulum'}:
            label = model_name.split('_')[2]

        if label in {'double'}:
            label = model_name.split('_')[3]

        result = plt.plot(
            final_frame.index,
            final_frame['mean', model_name],
            label=label.upper()
        )

        color = result[0]._color

        plt.fill_between(
            final_frame.index,
            final_frame['mean', model_name] - final_frame['std', model_name],
            final_frame['mean', model_name] + final_frame['std', model_name],
            color=color,
            alpha=0.5
        )

    plt.legend()

    plt.tight_layout()
    plt.savefig(name + ".png")
    # plt.show()


def main():
    metrics = [
        # ('beamrider', 'Beam Rider'),
        ('se.quest', 'SeaQuest'),
        # ('breakout', 'Breakout'),
        # ('enduro', 'Enduro'),
        # ('spaceinvaders', 'Space Invaders'),
        # ('qbert', 'Qbert'),
        # ('pong', 'Pong'),
        # ('half_cheetah', 'Half Cheetah'),
        # ('hopper', 'Hopper'),
        # ('inverted_pendulum', 'Inverted Pendulum'),
        # ('inverted_double_pendulum', 'Inverted Double Pendulum'),
        # ('swimmer', 'Swimmer'),
        # ('reacher', 'Reacher'),
        # ('walker2d', 'Walker2d'),

    ]

    for a, b in metrics:
        save_metric(a, b)


if __name__ == '__main__':
    main()
