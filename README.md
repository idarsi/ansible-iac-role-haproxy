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

## States

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
