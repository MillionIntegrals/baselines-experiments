#!/usr/bin/env bash

ansible-playbook run_experiments.yaml -i inventory/rl.gcp.yml --vault-id /home/jerry/gcp/vault_password.secret -e @vault/mongo.yaml
