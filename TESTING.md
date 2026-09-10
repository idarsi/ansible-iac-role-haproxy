# Testing

Molecule uses Podman. The shared local tooling environment currently provides
Python 3.12, ansible-core 2.21.4, ansible-lint 26.8.0, yamllint 1.38.0, and
Molecule 26.8.0 (Podman plugin 26.7.15). CI uses direct-version pins for
Ansible Core, ansible-lint, yamllint, Molecule, and the Podman plugin. There is
no constraints/lock file
for transitive dependencies and no hash-based installation, so pip may resolve
those dependencies differently over time. This is not full environment
reproducibility.

| Platform/image | Ansible or application versions | Molecule scenarios | Main coverage |
| --- | --- | --- | --- |
| Rocky Linux 9 (`quay.io/rockylinux/rockylinux`, pinned digest) | Distribution HAProxy; CI pins Ansible Core 2.18.6, ansible-lint 25.1.2, Molecule 25.2.0; shared local environment is newer and not equivalent | `validation`, `baseline`, `guardrails`, `update`, `lifecycle` | Validation, TLS and IPv6 rendering, package identity, installation, service, idempotence, latest-package convergence request, inactive-service reconfiguration, destructive guardrails |

## Scenario coverage

### validation

Runs `state: validate` with the minimal blueprint and performs no host change.
It also rejects newline-bearing server addresses and unknown nested security
keys before mutation.
It also rejects root/arbitrary privilege-drop identities and disabled TLS
verification without its explicit insecure opt-in.
Validation checks the inventory schema only; rendering and IPv6 bracket behavior
are covered by the `baseline` and `update` scenarios. Malformed IPv4 and IPv6
addresses are rejected before mutation.

### baseline

Converges a frontend/backend configuration, verifies secure privilege-drop
defaults, and verifies the rendered file.
It renders a TLS backend with `verify none` only when the explicit opt-in is
enabled.
Run the converge twice to check idempotence.

### guardrails

Creates disposable unmanaged content and verifies `all_absent` refuses to
remove it. It also verifies that a system-root cleanup path is rejected before
any mutation. Actual present and all_absent checks reject symlink parents,
symlink targets, and non-regular managed targets before state operations.
TLS trust guardrails reject symlinked CA parents, non-root-owned CA files, and
CA paths with the wrong type, with exact failure assertions and sentinels,
including global CA-file parents and per-server CA-directory parents.

### update

Requests the latest HAProxy package, converges and validates the configuration,
then verifies the rendered configuration, running service, and installed
package. The Molecule idempotence action repeats convergence. This fixture
cannot force a package change, so it does not verify package replacement or a
package-triggered restart; those behaviors are documented role semantics, not
coverage provided by this scenario.

### lifecycle

Stops HAProxy, changes the rendered configuration, and converges again. It
verifies that an inactive service is started successfully rather than receiving
a reload-only operation.

## Commands

```bash
export PATH="${IDARSI_ANSIBLE_TESTING_VENV:?Set IDARSI_ANSIBLE_TESTING_VENV to the shared test environment}/bin:$PATH"
molecule test -s validation
molecule test -s baseline
molecule test -s guardrails
molecule test -s update
molecule test -s lifecycle
```

CI runs `yamllint`, syntax check, production-profile `ansible-lint`, and all
five Molecule scenarios on pull requests and pushes to `main`. The automated
matrix currently covers Rocky Linux 9 only; broader platform coverage is
scheduled work. The local shared environment has not been used to establish
CI-version equivalence, and the full suite has not been verified locally.

RHEL 9/10 and Rocky Linux 10 are supported but are not in this automated
matrix. Invalid-input cases assert validation failure before mutation. Firewall,
certificate-content and package-removal behavior are intentional coverage gaps.
`all_absent` is guarded by absolute canonical paths, a root-owned
marker, and an empty-directory check; it must only be used on disposable hosts.
The `update` state requests only the latest HAProxy package (`state: latest`) and
converges and validates configuration before restarting HAProxy when the package
changed; it does not perform an operating-system upgrade. An unchanged package
does not restart the service. The scenario verifies the resulting configuration,
package presence, and running service, but cannot prove package replacement or
package-triggered restart because forcing replacement is repository-dependent.
Check mode is
supported for package/file/service operations where Ansible can
preview them, while HAProxy's external syntax validation remains an execution
boundary.
