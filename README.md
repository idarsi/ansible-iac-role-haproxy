> **Maturity State: Beta**<br>
> **RC Readiness: 69%**

# HAProxy Ansible Role

Idarsi-style role for one HAProxy instance on RHEL/Rocky Linux 9 and 10. The
public API is `iac_blueprint.haproxy`; inventory is validated before mutation.

## Quick start

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

## Schema and states

The `iac_blueprint.haproxy` mapping accepts `global`, `defaults`, `frontends`,
`backends`, and `stats`. Defaults are merged into an internal model before
resource validation. Unknown top-level keys, wrong types, unsafe paths, invalid
ports, modes, names, references, and non-loopback stats binds are rejected
before host mutation.

Supported states are `validate`, `install`, `update`, `uninstall`, `present`,
`absent`, `all_absent`, `started`, `stopped`, and `restarted`. Validation is
mutation-free. Present/install/update install and start HAProxy. Uninstall and
absent remove the package. `all_absent` additionally removes only the
role-marked configuration directory.

## Safety and limitations

Frontends, backends, ports, modes, references, duplicate names, and stats
binds are validated. Stats are restricted to loopback. Certificate fields are
absolute paths only; certificate contents are never copied. HAProxy syntax is
validated before configuration changes are accepted. Firewall rules are not
managed, and this role does not provision certificates or backend services.

See [TESTING.md](TESTING.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

RHEL/Rocky 9 and 10 are supported; Rocky 9 is currently tested automatically.
The role does not manage firewall rules, certificate contents, backend services,
or arbitrary files. `all_absent` removes only marked role-managed configuration
after ownership checks and refuses unmanaged content and symlink paths. It is
not a general-purpose cleanup operation. Check mode previews supported Ansible
operations, but external HAProxy syntax checks are not a dry-run guarantee.
