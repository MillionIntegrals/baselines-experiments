# baselines-experiments
Infra setup to run reinforcement learning baselines in a cloud deployment.


# Steps

1. Create GCP instances to run the experiments

```bash
bash ./scripts/gcp-create-instances.sh
```

2. Set up ansible inventory file. Example for GCP below

```yaml
plugin: gcp_compute
projects:
  - projectname
auth_kind: serviceaccount
groups:
  rl: true
filters:
  - any filters you may want
service_account_file: /home/yourdir/gcp/serviceaccount.json

```

3. Install ansible galaxy roles

```bash
ansible-galaxy install geerlingguy.docker geerlingguy.pip
```

4. Set up experiment environment on all machines

```bash
bash ./scripts/ansible-full-setup.sh
```

5. Start running the experiments

```bash
bash ./scripts/ansible-run-experiments.sh
```
