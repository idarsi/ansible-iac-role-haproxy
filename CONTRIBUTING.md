# Contributing

Keep `iac_blueprint.haproxy` declarative. Every new field requires validation,
documentation, and scenario coverage. Keep destructive cleanup marker-based;
do not add implicit firewall changes or certificate-content copying.

Use the shared test environment and Podman:

```bash
export PATH="/home/arsi/.local/share/venvs/idarsi-ansible-testing/bin:$PATH"
ansible-playbook --syntax-check -i docs/inventory-minimal.yml docs/playbook-example.yml
ansible-lint --profile production
```

Keep repository text and user-facing messages in English.
