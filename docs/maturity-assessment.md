# HAProxy role maturity assessment

Assessed on 2026-11-15: `6d15b97` plus the scenario-prefix changes on
`update/haproxy-backend-scenario-prefixes` (uncommitted working tree).
The boundary is the existing README contract, including all public states and
RHEL/Rocky 9 and 10. This naming-only change does not improve runtime coverage.

**RC Readiness: 77%; score-based and final state: Beta.** The prior README's
77% is retained. The scorecard below makes the evidence and remaining gaps
explicit; historical local passes are not fresh results for this ref.

Scores use only 0, half, or full credit per criterion.

| Category / criterion | Score | Evidence and limitation |
| --- | ---: | --- |
| Scope: purpose and boundaries | 3/3 | README identifies one instance and excludes firewall, PKI provisioning, and backends. |
| Scope: inputs and states | 2.5/5 | README, defaults and state files agree; no complete field/type reference. |
| Scope: support contract | 4/4 | Defaults and metadata enumerate platforms and minimum Core; TESTING names image and tool pins. |
| **Scope subtotal** | **9.5/12** | |
| Function: core convergence | 8/8 | Present renders syntax-validated configuration, installs package, starts service; historical baseline pass and observable verification. |
| Function: applicable lifecycle | 3/6 | State implementations exist; lifecycle test covers inactive-service reconfiguration, not every removal/control transition. |
| Function: platform and dependencies | 1.5/3 | Vendor packages and generic modules; only Rocky 9 runtime evidence. |
| Function: failure and rerun | 1.5/3 | Actionable assertions and template validation; interrupted-run recovery not demonstrated. |
| **Function subtotal** | **14/20** | |
| Safety: preflight | 6/6 | Root/type/path and inventory validation precede state dispatch; negative fixtures cover identities, addresses and TLS. |
| Safety: secure behavior | 6/6 | Non-privileged identity, TLS opt-in, loopback stats, host trust checks and restrictive marker permissions. |
| Safety: destructive guardrails | 5/5 | Canonical paths, root-owned marker and unmanaged-content refusal; guardrail fixtures verify refusals and preservation. |
| Safety: check and diff | 1.5/3 | Native modules and documented external syntax-check limitation; no representative preview test. |
| **Safety subtotal** | **18.5/20** | |
| Convergence: idempotence | 5/5 | Baseline and update include Molecule idempotence; prior TESTING records local passes. |
| Convergence: transitions | 2/4 | Stop/reconfigure/start verified; successful removal and repeated reverse transitions missing. |
| Convergence: recovery | 2/4 | Running-service reload versus inactive-service start; package-triggered restart implemented but not forced in tests. |
| **Convergence subtotal** | **9/13** | |
| Testing: static checks | 3/3 | CI configures syntax, yamllint and production-profile ansible-lint across role-owned code. |
| Testing: input validation | 4/4 | Accepted inputs, actionable rejection assertions, and absence of managed files verified. |
| Testing: functional outcomes | 3/6 | Configuration, package, permissions and service assertions; not the complete public contract. |
| Testing: idempotence | 4/4 | Explicit baseline/update idempotence actions and recorded historical passes. |
| Testing: lifecycle and guardrails | 2/4 | Strong refusal tests; successful destructive lifecycle remains uncovered. |
| Testing: platform matrix | 1.5/3 | Rocky 9 only; RHEL 9/10 and Rocky 10 lack evidence. |
| Testing: CI enforcement | 0.5/1 | PR/push checks configured; current result and branch-protection enforcement unavailable. |
| **Testing subtotal** | **18/25** | |
| Documentation: operator guidance | 4/4 | README examples, state semantics, ownership and TLS limitations match implementation. |
| Documentation: tests and limitations | 2/2 | TESTING lists actual matrix, renamed commands, historical evidence and coverage gaps. |
| Documentation: contribution contract | 1/2 | Validation/docs/scenario impact required; example-update policy not explicit. |
| Documentation: release metadata | 1/2 | MIT license and role metadata present; rolling image and unlocked transitive tooling dependencies limit reproducibility. |
| **Documentation subtotal** | **8/10** | |
| **Total** | **77/100** | |

## RC blockers and next steps

- Materially untested support claims cap maturity at **Beta**: obtain baseline
  evidence for RHEL 9/10 and Rocky 10, or explicitly narrow support separately.
- Add successful removal, repeated transitions, forced package replacement,
  recovery, and representative check/diff coverage before claiming completeness.
- Document every public field and make contribution/example impact explicit.
- Confirm required CI enforcement and green results at the eventual commit;
  no CI success is inferred from configuration alone.
- Rerun renamed scenarios through the tester. Historical evidence in TESTING
  predates this rename and uses a rolling image tag.

No production-readiness approval or long-term production evidence was supplied.
This assessment is not a production certification or a new runtime test result.

## Checks for this change

Using the existing shared `ansible-current` environment (Core 2.20.8,
yamllint 1.38.0), the following passed:

```bash
yamllint .github/workflows/ci.yml molecule/podman-*/molecule.yml
ansible-playbook --syntax-check -i docs/inventory-minimal.yml docs/playbook-example.yml
git -c core.whitespace=-blank-at-eol diff --check HEAD
```

A read-only comparison against `HEAD` also confirmed that all ten converge
and verify playbooks are byte-identical and each Molecule configuration differs
only in its platform identity; all five new IDs match the Podman driver and
CI/documented commands. Plain `git diff --check HEAD` reports only the README's
intentional Markdown hard-break spaces. No runtime or full-suite checks ran.
The installed Core version differs from both CI's 2.18.6 and the older local
2.21.4 description in TESTING; these checks do not establish version equivalence.
