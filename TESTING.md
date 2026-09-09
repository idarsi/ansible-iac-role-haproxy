# Testing

Molecule uses Podman. The shared local tooling environment is described by the
developer workflow; CI creates an isolated environment from the pinned ranges
in `.github/workflows/ci.yml`.

| Platform/image | Ansible or application versions | Molecule scenarios | Main coverage |
| --- | --- | --- | --- |
| Rocky Linux 9 (`rockylinux:9-ubi-init`) | Distribution HAProxy; current Ansible | `validation`, `baseline`, `guardrails` | Validation, installation, rendering, service, idempotence, destructive-operation guardrails |

## Scenario coverage

### validation

Runs `state: validate` with the minimal blueprint and performs no host change.

### baseline

Converges a frontend/backend configuration and verifies the rendered file.
Run the converge twice to check idempotence.

### guardrails

Creates disposable unmanaged content and verifies `all_absent` refuses to
remove it. It also verifies that a system-root cleanup path is rejected before
any mutation.

## Commands

```bash
export PATH="<shared-ansible-testing-venv>/bin:$PATH"
molecule test -s validation
molecule test -s baseline
molecule test -s guardrails
```

CI runs `yamllint`, syntax check, production-profile `ansible-lint`, and all
three Molecule scenarios on pull requests and pushes to `main`. The automated
matrix currently covers Rocky Linux 9 only; broader platform and lifecycle
coverage is scheduled work.

RHEL 9/10 and Rocky Linux 10 are supported but are not in this automated
matrix. Invalid-input cases should assert the actionable failure text; the
current validation scenario covers the valid mutation-free path. Firewall,
certificate-content, lifecycle, and package-removal behavior are intentional
coverage gaps. `all_absent` is guarded by absolute canonical paths, a root-owned
marker, and an empty-directory check; it must only be used on disposable hosts.
Check mode is supported for package/file/service operations where Ansible can
preview them, while HAProxy's external syntax validation remains an execution
boundary.
