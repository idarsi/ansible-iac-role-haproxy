# Testing

Molecule uses Podman. These scenarios are defined but were not run during
implementation.

| Platform/image | Ansible or application versions | Molecule scenarios | Main coverage |
| --- | --- | --- | --- |
| Rocky Linux 9 (`rockylinux:9`) | Distribution HAProxy; current Ansible | `validation`, `baseline` | Validation, installation, rendering, service, idempotence |

## Scenario coverage

### validation

Runs `state: validate` with the minimal blueprint and performs no host change.

### baseline

Converges a frontend/backend configuration and verifies the rendered file.
Run the converge twice to check idempotence.

## Commands

```bash
export PATH="/home/arsi/.local/share/venvs/idarsi-ansible-testing/bin:$PATH"
molecule test -s validation
molecule test -s baseline
```

RHEL 9/10 and Rocky Linux 10 are supported but are not in this initial
automated matrix. Firewall and certificate-content behavior are intentional
coverage gaps.
