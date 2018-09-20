"""
PYTHON EXPERIMENT RUNNER

Features - pidfile
"""
import os
import sys
import yaml
import shelve

from daemonize import Daemonize


pid = "/tmp/run_experiment.pid"


EXPERIMENT_DICTIONARY = {
    "beamrider_a2c": "atari/a2c/beamrider_a2c.yaml",
    "breakout_a2c": "atari/a2c/breakout_a2c.yaml",
    "qbert_a2c": "atari/a2c/qbert_a2c.yaml",
    "enduro_a2c": "atari/a2c/enduro_a2c.yaml",
    "pong_a2c": "atari/a2c/pong_a2c.yaml",
    "seaquest_a2c": "atari/a2c/seaquest_a2c.yaml",
    "spaceinvaders_a2c": "atari/a2c/spaceinvaders_a2c.yaml",

    "beamrider_ppo": "atari/ppo/beamrider_ppo.yaml",
    "breakout_ppo": "atari/ppo/breakout_ppo.yaml",
    "qbert_ppo": "atari/ppo/qbert_ppo.yaml",
    "enduro_ppo": "atari/ppo/enduro_ppo.yaml",
    "pong_ppo": "atari/ppo/pong_ppo.yaml",
    "seaquest_ppo": "atari/ppo/seaquest_ppo.yaml",
    "spaceinvaders_ppo": "atari/ppo/spaceinvaders_ppo.yaml",

    "beamrider_acer": "atari/acer/beamrider_acer.yaml",
    "breakout_acer": "atari/acer/breakout_acer.yaml",
    "qbert_acer": "atari/acer/qbert_acer.yaml",
    "enduro_acer": "atari/acer/enduro_acer.yaml",
    "pong_acer": "atari/acer/pong_acer.yaml",
    "seaquest_acer": "atari/acer/seaquest_acer.yaml",
    "spaceinvaders_acer": "atari/acer/spaceinvaders_acer.yaml",

    "beamrider_trpo_jrx": "atari/trpo_jrx/beamrider_trpo_jrx.yaml",
    "breakout_trpo_jrx": "atari/trpo_jrx/breakout_trpo_jrx.yaml",
    "qbert_trpo_jrx": "atari/trpo_jrx/qbert_trpo_jrx.yaml",
    "enduro_trpo_jrx": "atari/trpo_jrx/enduro_trpo_jrx.yaml",
    "pong_trpo_jrx": "atari/trpo_jrx/pong_trpo_jrx.yaml",
    "seaquest_trpo_jrx": "atari/trpo_jrx/seaquest_trpo_jrx.yaml",
    "spaceinvaders_trpo_jrx": "atari/trpo_jrx/spaceinvaders_trpo_jrx.yaml",

    "beamrider_trpo_oai": "atari/trpo_oai/beamrider_trpo_oai.yaml",
    "breakout_trpo_oai": "atari/trpo_oai/breakout_trpo_oai.yaml",
    "qbert_trpo_oai": "atari/trpo_oai/qbert_trpo_oatrpo_oaiyaml",
    "enduro_trpo_oai": "atari/trpo_oai/enduro_trpo_oai.yaml",
    "pong_trpo_oai": "atari/trpo_oai/pong_trpo_oai.yaml",
    "seaquest_trpo_oai": "atari/trpo_oai/seaquest_trpo_oai.yaml",
    "spaceinvaders_trpo_oai": "atari/trpo_oai/spaceinvaders_trpo_oai.yaml",

    "beamrider_dqn": "atari/dqn/beamrider_dqn.yaml",
    "breakout_dqn": "atari/dqn/breakout_dqn.yaml",
    "qbert_dqn": "atari/dqn/qbert_dqn.yaml",
    "enduro_dqn": "atari/dqn/enduro_dqn.yaml",
    "pong_dqn": "atari/dqn/pong_dqn.yaml",
    "seaquest_dqn": "atari/dqn/seaquest_dqn.yaml",
    "spaceinvaders_dqn": "atari/dqn/spaceinvaders_dqn.yaml",
}


def handle_experiment(path, number):
    cmdline = 'bash ./scripts/docker-run-experiment.sh {} train -r {} --seed {}'.format(
        EXPERIMENT_DICTIONARY[path], number, number
    )
    print(">>> {}".format(cmdline))
    os.system(cmdline)


def handle_halt():
    os.system("halt")


HANDLERS = {
    'experiment': handle_experiment,
    'halt': handle_halt
}


def execute_task(datastore, task):
    key = str(sorted(tuple(task.items())))

    if datastore.get(key, False):
        print("Task", task, "is done")
        return

    task = task.copy()
    name = task['name']
    del task['name']

    HANDLERS[name](**task)

    datastore[key] = True


def main():
    with open(sys.argv[1]) as fp:
        task_file = yaml.safe_load(fp)

    datastore = shelve.open('shelve')

    for task in task_file.get('tasks', []):
        execute_task(datastore, task)


if __name__ == '__main__':
    dirname = os.path.dirname(sys.argv[0])

    if not dirname:
        dirname = os.getcwd()

    if len(sys.argv) < 2:
        print("Need one argument")
    else:
        daemon = Daemonize(app="run_experiment", pid=pid, action=main, chdir=dirname)
        daemon.start()

