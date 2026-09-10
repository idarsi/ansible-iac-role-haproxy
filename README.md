> **Maturity State: Beta**<br>
> **RC Readiness: 75%**<br>
> **Assessed ref:** `0339bff` plus the current uncommitted working tree<br>
> **Limitations:** Validation, update, baseline, guardrails, and lifecycle passed locally (lifecycle passed after reset); an initial stale lifecycle run failed. Local tool versions differ from CI pins, and the full suite was not rerun. Rocky Linux 9 is the only automated platform evidence.

ANSIBLE-IAC-ROLE-HAPROXY
========================
**COPYRIGHT** 2026 ^(ida|arsi)$ collective  
**LICENSE** MIT License [LICENSE](LICENSE)  
**AUTHORS**
- Arsi Atomi <arsi@atomi.sh>  

Overview
--------

Idarsi-style role for one HAProxy instance on RHEL/Rocky Linux 9 and 10. The
public API is `iac_blueprint.haproxy`; inventory is validated before mutation.

Quick start
-----------

See `docs/inventory-minimal.yml` and `docs/inventory-basic.yml`.

```yaml
iac_blueprint:
  haproxy:
    frontends:
      - name: "web"
        bind: "0.0.0.0"
        port: 80
        default_backend: "apps"
    backends:
      - name: "apps"
        servers:
          - name: "app1"
            address: "127.0.0.1"
            port: 8080
```

An empty mapping is a valid minimal blueprint and produces a secure empty
configuration.

Schema and states
-----------------

The `iac_blueprint.haproxy` mapping accepts `global`, `defaults`, `frontends`,
`backends`, `stats`, and `security`. Defaults are merged into an internal model
before resource validation. HAProxy uses the package-provided global
`user: haproxy` and `group: haproxy` identity for privilege dropping when
those global identities are omitted. Explicit privilege-changing overrides,
including root or arbitrary identities, are rejected before host mutation.
After installation, the role validates that the package-provided accounts
exist and are non-privileged. The role deliberately does not set systemd
`User=`, preserving low-port binding, PID, runtime, and certificate semantics
across vendor units. Unknown top-level keys, wrong types, unsafe paths, invalid
ports, modes, names, references, and non-loopback stats binds are rejected
before host mutation.

Supported states are `validate`, `install`, `update`, `uninstall`, `present`,
`absent`, `all_absent`, `started`, `stopped`, and `restarted`. Validation is
mutation-free. Present/install install and start HAProxy. `update` upgrades
only the HAProxy package to the repository's latest version, then converges
configuration and service state. When the package changes, HAProxy is
restarted after convergence so the running process uses the upgraded binary;
unchanged packages are not restarted. Configuration-only changes use a reload.
Uninstall and
absent remove the package. `all_absent` additionally removes only the
role-marked configuration directory.

Safety and limitations
----------------------

Frontends, backends, ports, modes, references, duplicate names, and stats
binds are validated. Stats are restricted to loopback. Backend TLS verification
is enabled by default; TLS servers must provide `verifyhost` and trust material.
Set `security.backend_tls_ca_file` to an absolute PEM CA bundle, or set
`security.backend_tls_ca_directory` and each TLS server's `ca_file` to a
basename in that directory (no `/`, `..`, or traversal is accepted; per-server
overrides are rejected when a global CA file is configured). HAProxy's
`ca-base` is rendered. Setting `backend_tls_verify: false`
is an insecure opt-in and additionally requires
`haproxy_allow_insecure_backend_tls: true`. Certificate fields are absolute paths
only; certificate contents are never copied. `state: validate` checks blueprint
shape and path safety only. Mutating states additionally require configured CA
files/directories to exist, have the expected type, be readable, root-owned,
non-symlinked, and have canonical parent paths; group/world-writable trust
material is refused. HAProxy syntax is validated before configuration
changes are accepted. Firewall rules are not
managed, and this role does not provision certificates or backend services.
Host trust validation applies to `install`, `present`, and `update`, which
render or use TLS configuration. Service-control states (`started`, `stopped`,
and `restarted`) and removal states do not require unrelated CA paths to be
available; this allows emergency control and uninstall even after trust
material has been removed.

See [TESTING.md](TESTING.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

RHEL/Rocky 9 and 10 are supported; Rocky 9 is currently tested automatically.
The role does not manage firewall rules, certificate contents, backend services,
or arbitrary files. `all_absent` removes only marked role-managed configuration
after ownership checks and refuses unmanaged content, non-regular files, and
symlink paths. It is
not a general-purpose cleanup operation. Check mode previews supported Ansible
operations, but external HAProxy syntax checks are not a dry-run guarantee.
