---
name: windows_testing
description: Drive the supplied disposable W10C-Testing guest through the fixed Halo controller. Use for Windows build/test runs, artifact transfer, testing snapshots, or working-baseline promotion; do not use for canonical W10C, Dev, or VM provisioning.
category: substrate
common: false
---

# windows_testing — use the disposable Windows test guest

The controller exposes one guest, `W10C-Testing`, with the same commands from
Halo and Dev. It cannot select another domain or run commands/read files on
Halo. Cash/Jed own installation, guest credentials, the immutable recovery
snapshot, and live provisioning.

## Initialize once per checkout

On Halo:

```bash
sc vm test init local
```

On Dev, use the operator-supplied SSH alias whose key is restricted to the
controller ForceCommand:

```bash
sc vm test init ssh halo-windows-test
```

Initialization changes only the transport. Every later verb is identical. If
the controller or guest is unconfigured, surface the structured error; do not
change SSH, libvirt, networking, credentials, or snapshots to repair it.

## Run one test session

```bash
sc vm test status
sc vm test acquire --owner "<shell/task>"
sc vm test start
sc vm test push <local-file> artifacts/test.zip
sc vm test exec --cwd run --command-file <local-script.ps1>
sc vm test pull results/result.json <local-result>
sc vm test reset working
sc vm test release
```

`acquire` saves an owner-only opaque lease locally; later commands use it
without putting it in argv or logs. Keep the lease for the whole push/exec/pull
and reset sequence. A competing mutation fails rather than joining the active
session. Report the test result and reset/release result separately.

Guest paths are relative to the configured workspace. `exec` always requires
an explicit `--cwd` there and runs PowerShell under the configured
administrator account. Prefer `--command-file` for non-trivial scripts. A
normal test timeout kills the tracked guest process tree. If the SSH result is
instead uncertain, reset and promotion remain blocked; run an explicit stop to
confirm power-off before continuing.

`stop` first requests a graceful Windows shutdown and waits a bounded time.
Use `--force` only when the operator explicitly chooses to hard-stop this
disposable guest; the flag is the confirmation.

## Testing snapshots

```bash
sc vm test snapshot list
sc vm test snapshot create <name>
sc vm test reset <name>
sc vm test snapshot delete <name>
```

Snapshot creation and reset shut the guest down cleanly and leave it powered
off. The controller refuses deletion or replacement of the recovery snapshot
and current working baseline. Snapshot names are simple letters/digits with
dot, underscore, or dash.

After installing and verifying a dependency that should survive later resets:

```bash
sc vm test baseline promote [new-name]
```

Promotion creates and verifies a new offline snapshot before changing the
working-baseline reference. Failure leaves the prior reference selected; a
successful promotion also retains the previous snapshot.

## Installation (Cash/Jed only)

Do not run this section during an ordinary test session. Keep the existing
libvirt NAT network and provision only `W10C-Testing`; verify UUID
`0b314d1a-bd03-47b9-8155-01a6d470f7a9`. Canonical `W10C` and Dev stay out of
scope.

The current dos-arch Windows project targets .NET 8 for Windows on x64. The
guest needs Windows OpenSSH, an SSH account in local Administrators, PowerShell,
the .NET 8 SDK, package restore access, and a writable workspace such as
`C:\\SubfloorTest`. Git is optional when a shell pushes prepared artifacts.
Create the immutable recovery snapshot and initial offline working snapshot as
an operator.

### Disposable guest execution policy

The controller uploads a generated PowerShell script and invokes it with
`powershell.exe -File`. A stock `Restricted` execution policy rejects that
script before the test command starts. For a deliberately disposable test
image, open **Windows PowerShell as Administrator** and configure the image:

```powershell
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy Bypass -Force
Get-ExecutionPolicy -List
Get-ExecutionPolicy
```

Pass = the effective policy printed by the final command is `Bypass`. A
`MachinePolicy` or `UserPolicy` imposed by Group Policy can override the local
setting; do not promote the baseline until the effective-policy check and an
actual controller `exec` both pass.

> **Disposable-image boundary:** machine-wide `Bypass` removes PowerShell's
> script-signing, warning, and prompt guardrails for every account in this
> guest. The controller's SSH identity is also a local Administrator and can
> execute arbitrary privileged code in the guest. Use this posture only for a
> throwaway VM that contains no personal/work data, reusable credentials,
> authenticated browser sessions, host shares, or other secrets. Do not apply
> it to canonical `W10C`, a daily-use VM, or any persistent machine. Snapshot
> reset removes changes made after the snapshot; it does not protect data while
> the VM is running or remove a secret already baked into a baseline.

After installing the toolchain and setting the policy, run a small
push/exec/pull test, compare the source and pulled artifact hashes, promote a
new working baseline, then reset/start/exec once from that baseline. Preserve
the immutable recovery snapshot and the previous working snapshot. Finish
powered off with no active lease.

On Halo, create `~/.config/subfloor/windows-test-controller.json` for `jedi`
with mode `0600` and its parent directory mode `0700`:

```json
{
  "guest": {
    "host": "<W10C-Testing address on libvirt NAT>",
    "port": 22,
    "user": "<Windows administrator account>",
    "key_path": "/home/jedi/.ssh/<guest-key>",
    "workspace": "C:\\SubfloorTest"
  },
  "recovery_snapshot": "<immutable-recovery-name>",
  "initial_working_baseline": "<working-baseline-name>",
  "lease_seconds": 14400
}
```

Keep the guest key owner-only and register its host key for `jedi`; the
controller uses strict host-key checking. It has no daemon and opens no
listener.

For Dev, add a dedicated public key to Halo `jedi` with the reviewed `sc` path
as a ForceCommand. The command has no shell operators and does not depend on
Fish syntax:

```text
restrict,command="/home/jedi/Repos/subfloor/sc vm test serve" ssh-ed25519 <public-key> windows-test-controller
```

Keep the private key on Dev and point an SSH alias such as
`halo-windows-test` at it with `RequestTTY no`. Do not reuse an unrestricted
Halo login key. Verify both init modes with the same small
status/acquire/start/push/exec/pull/reset/release run, then confirm lease
conflicts, protected snapshot refusal, and failed-promotion preservation.

After the reviewed engine revision is installed in active dos-arch, import this
file as a fork-local skill. Every `sc skill` mutation is Planner-owned: the
Admin repins the engine, then a launched Planner shell runs the import and
grants. When no Planner is booted, the Admin asks the FnB to boot one rather
than running these commands from the Admin seat, where they are refused.

```bash
# on a launched Planner shell
sc skill put --file .super-coder/docs/skills/windows_testing/SKILL.md
sc skill grant windows_testing <dev-shortname> <reviewer-shortname>
sc skill list
```

Grant it only to the shells that use this seat.
