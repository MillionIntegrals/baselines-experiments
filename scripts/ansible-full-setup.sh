#!/usr/bin/env bash

ansible-playbook full_setup.yaml -i inventory/rl.gcp.yml --vault-id /home/jerry/gcp/vault_password.secret -e @vault/mongo.yaml
