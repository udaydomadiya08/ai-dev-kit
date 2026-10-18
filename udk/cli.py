"""
Command Line Interface (CLI) for Universal AI Dev Kit (UDK).
Pure standard library implementation providing init, list, validate,
doctor, diff, update, and remove commands with predictable exit codes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from udk.adapters.registry import (
    get_available_adapter_ids,
    list_adapters,
)
from udk.detector import detect_workspace
from udk.generator.engine import GeneratorEngine
from udk.manifest import ManifestManager
from udk.profiles import get_profile, list_profiles


def cmd_init(args: argparse.Namespace) -> int:
    workspace_root = Path(args.path or ".").resolve()
    engine = GeneratorEngine(workspace_root=workspace_root)

    # Detect workspace if profile or adapter not specified
    det_profile, det_adapters, markers = detect_workspace(workspace_root)
    profile_name = args.profile or det_profile
    adapter_ids = args.agent or det_adapters

    profile = get_profile(profile_name)
    if not profile:
        print(
            f"Error: Unknown profile '{profile_name}'. Run 'udk list profiles' to see available options.",
            file=sys.stderr,
        )
        return 1

    # Validate adapter IDs
    valid_adapters = get_available_adapter_ids()
    for a_id in adapter_ids:
        if a_id not in valid_adapters:
            print(
                f"Error: Unknown agent adapter '{a_id}'. Run 'udk list agents' to see available options.",
                file=sys.stderr,
            )
            return 1

    print("Universal AI Dev Kit — Project Initialization")
    print(f"Workspace: {workspace_root}")
    print(f"Profile:   {profile.name} (`{profile.id}`)")
    print(f"Adapters:  {', '.join(adapter_ids)}")
    if markers:
        print(f"Detected:  {', '.join(f'{k} ({v})' for k, v in markers.items())}")
    print("-" * 60)

    # Compute planned changes
    plan = engine.plan(
        adapter_ids=adapter_ids,
        profile_name=profile.id,
        force=args.force,
    )

    conflicts = [item for item in plan if item.action == "conflict"]
    if conflicts and not args.force:
        print(
            "\n[!] CONFLICTS DETECTED: Existing files were modified or conflict with targets:"
        )
        for c in conflicts:
            print(f"  - {c.path}: {c.reason}")
        print(
            "\nUse --force to overwrite user modifications, or inspect with 'udk diff'."
        )
        return 1

    print("\nPlanned File Operations:")
    for item in plan:
        symbol = {
            "create": "[+] CREATE",
            "update": "[*] UPDATE",
            "unchanged": "[=] UNCHANGED",
            "conflict": "[!] CONFLICT",
        }.get(item.action, "[?]")
        print(f"  {symbol:<14} {item.path} ({item.reason})")

    if args.dry_run:
        print("\n[Dry-run] No changes written to disk.")
        return 0

    # Apply changes
    written = engine.apply(
        plan_items=plan,
        profile_name=profile.id,
        adapter_ids=adapter_ids,
        skills=profile.recommended_skills,
    )

    print("-" * 60)
    print(f"Initialization successful! Created/updated {len(written)} files.")
    print("Run 'udk validate' to verify configuration integrity.")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    category = args.category

    if category in ("agents", "all"):
        print("\nAvailable Agent Adapters:")
        print(f"{'ID':<16} {'NAME':<32} {'DESCRIPTION'}")
        print("-" * 80)
        for a in list_adapters():
            print(f"{a.id:<16} {a.name:<32} {a.description}")

    if category in ("profiles", "all"):
        print("\nAvailable Domain Profiles:")
        print(f"{'ID':<16} {'NAME':<30} {'DESCRIPTION'}")
        print("-" * 80)
        for p in list_profiles():
            print(f"{p.id:<16} {p.name:<30} {p.description}")

    if category in ("skills", "all"):
        engine = GeneratorEngine(workspace_root=Path("."))
        skills = engine.load_canonical_skills()
        print("\nAvailable Canonical Skills (SKILL.md):")
        print(f"{'SKILL':<22} {'SUMMARY':<46} {'TAGS'}")
        print("-" * 85)
        for s_id, s_data in sorted(skills.items()):
            meta = s_data.get("metadata", {})
            name = meta.get("name", s_id)
            desc = meta.get("description", "")
            tags = ", ".join(meta.get("tags", []))
            print(f"{name:<22} {desc[:44]:<46} [{tags}]")

    print()
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    workspace_root = Path(args.path or ".").resolve()
    mgr = ManifestManager(workspace_root)
    manifest = mgr.load()

    if not manifest:
        print(
            f"Error: No UDK installation found in '{workspace_root}'. Run 'udk init' first.",
            file=sys.stderr,
        )
        return 1

    audit = mgr.audit_drift()
    print(f"Universal AI Dev Kit — Drift & Status Inspection: {workspace_root}")
    print(
        f"Installed Profile: {manifest.profile} | Adapters: {', '.join(manifest.adapters)}"
    )
    print("-" * 70)
    print(f"{'FILE PATH':<40} {'STATUS':<15} {'GENERATOR'}")
    print("-" * 70)

    drift_count = 0
    for path, info in sorted(audit.items()):
        status = info["status"]
        if status != "unchanged":
            drift_count += 1
        print(f"{path:<40} {status.upper():<15} {info.get('generator', '')}")

    print("-" * 70)
    if drift_count == 0:
        print("All managed files match manifest records cleanly.")
    else:
        print(f"Found {drift_count} modified or missing files.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    workspace_root = Path(args.path or ".").resolve()
    mgr = ManifestManager(workspace_root)
    manifest = mgr.load()

    if not manifest:
        print(
            f"Error: No UDK installation found in '{workspace_root}'. Run 'udk init' first.",
            file=sys.stderr,
        )
        return 1

    engine = GeneratorEngine(workspace_root=workspace_root)
    plan = engine.plan(
        adapter_ids=manifest.adapters,
        profile_name=manifest.profile,
        selected_skills=manifest.skills,
        force=args.force,
    )

    conflicts = [item for item in plan if item.action == "conflict"]
    if conflicts and not args.force:
        print("\n[!] UPDATE BLOCKED: The following files were customized by the user:")
        for c in conflicts:
            print(f"  - {c.path}")
        print(
            "\nTo overwrite, run 'udk update --force'. To inspect changes, run 'udk diff'."
        )
        return 1

    if args.dry_run:
        print("\n[Dry-run] Planned updates:")
        for item in plan:
            print(f"  {item.action.upper():<10} {item.path}")
        return 0

    written = engine.apply(
        plan_items=plan,
        profile_name=manifest.profile,
        adapter_ids=manifest.adapters,
        skills=manifest.skills,
    )

    print(f"Update complete! Updated {len(written)} files.")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    workspace_root = Path(args.path or ".").resolve()
    mgr = ManifestManager(workspace_root)
    manifest = mgr.load()

    if not manifest:
        print(
            f"Error: No UDK installation found in '{workspace_root}'.", file=sys.stderr
        )
        return 1

    # Check drift before removing
    audit = mgr.audit_drift()
    modified = [p for p, info in audit.items() if info["status"] == "modified"]

    if modified and not args.force:
        print("\n[!] REMOVAL BLOCKED: The following files were customized by the user:")
        for p in modified:
            print(f"  - {p}")
        print("\nTo remove anyway, run 'udk remove --force'.")
        return 1

    print(f"Removing Universal AI Dev Kit managed files from {workspace_root}...")
    removed_count = 0

    for rel_path in sorted(manifest.files.keys(), reverse=True):
        full_path = workspace_root / rel_path
        if full_path.is_file():
            full_path.unlink()
            removed_count += 1
            print(f"  [-] Removed {rel_path}")

        # Clean empty parent directories up to workspace_root
        parent = full_path.parent
        while parent != workspace_root and parent.is_dir():
            if not any(parent.iterdir()):
                try:
                    parent.rmdir()
                    parent = parent.parent
                except OSError:
                    break
            else:
                break

    # Remove manifest directory
    if mgr.manifest_file.is_file():
        mgr.manifest_file.unlink()
    if mgr.manifest_dir.is_dir() and not any(mgr.manifest_dir.iterdir()):
        mgr.manifest_dir.rmdir()

    print(
        f"Removal complete. Removed {removed_count} managed files. User code preserved."
    )
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    from udk.validator.engine import ValidatorEngine

    workspace_root = Path(args.path or ".").resolve()
    validator = ValidatorEngine(workspace_root=workspace_root)
    diagnostics = validator.validate_all()

    print(f"Universal AI Dev Kit — Project Validation: {workspace_root}")
    print("-" * 65)

    errors = 0
    warnings = 0
    for diag in diagnostics:
        if diag.severity == "error":
            errors += 1
        elif diag.severity == "warning":
            warnings += 1
        print(f"  {diag}")

    print("-" * 65)
    if errors > 0:
        print(f"Validation FAILED: {errors} error(s), {warnings} warning(s).")
        return 1
    elif warnings > 0:
        print(f"Validation passed with {warnings} warning(s).")
        return 0
    else:
        print("Validation PASSED: All configuration schemas, files, and links valid.")
        return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    from udk.validator.engine import ValidatorEngine

    workspace_root = Path(args.path or ".").resolve()
    validator = ValidatorEngine(workspace_root=workspace_root)
    report = validator.run_doctor()

    print("Universal AI Dev Kit — Doctor Diagnostic Report")
    print("=" * 65)
    for category, checks in report.items():
        print(f"\n[{category}]")
        for check in checks:
            status_str = (
                "[OK]  "
                if check["status"] == "ok"
                else "[WARN]"
                if check["status"] == "warn"
                else "[FAIL]"
            )
            print(f"  {status_str} {check['title']}: {check['detail']}")

    print("\n" + "=" * 65)
    has_fails = any(
        any(c["status"] == "fail" for c in checks) for checks in report.values()
    )
    return 1 if has_fails else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="udk",
        description="Universal AI Dev Kit: Engineering foundation for AI-assisted development.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # init
    p_init = subparsers.add_parser(
        "init", help="Initialize UDK in a project repository"
    )
    p_init.add_argument(
        "--profile", "-p", help="Target domain profile (e.g. python, web, ai-ml)"
    )
    p_init.add_argument(
        "--agent",
        "-a",
        action="append",
        help="Target agent adapter (can specify multiple)",
    )
    p_init.add_argument(
        "--path",
        default=".",
        help="Project workspace path (default: current directory)",
    )
    p_init.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview planned changes without writing to disk",
    )
    p_init.add_argument(
        "--force", "-f", action="store_true", help="Overwrite conflicting files"
    )
    p_init.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run without interactive confirmation",
    )
    p_init.set_defaults(func=cmd_init)

    # list
    p_list = subparsers.add_parser(
        "list", help="List available adapters, profiles, or skills"
    )
    p_list.add_argument(
        "category",
        nargs="?",
        default="all",
        choices=["agents", "profiles", "skills", "all"],
    )
    p_list.set_defaults(func=cmd_list)

    # diff
    p_diff = subparsers.add_parser("diff", help="Inspect file drift against manifest")
    p_diff.add_argument("--path", default=".", help="Project workspace path")
    p_diff.set_defaults(func=cmd_diff)

    # update
    p_update = subparsers.add_parser(
        "update", help="Update managed files from canonical templates"
    )
    p_update.add_argument("--path", default=".", help="Project workspace path")
    p_update.add_argument("--dry-run", action="store_true", help="Preview updates")
    p_update.add_argument(
        "--force", "-f", action="store_true", help="Force overwrite modified files"
    )
    p_update.set_defaults(func=cmd_update)

    # remove
    p_remove = subparsers.add_parser(
        "remove", help="Safely remove UDK files and manifest"
    )
    p_remove.add_argument("--path", default=".", help="Project workspace path")
    p_remove.add_argument(
        "--force", "-f", action="store_true", help="Force removal even if modified"
    )
    p_remove.set_defaults(func=cmd_remove)

    # validate
    p_validate = subparsers.add_parser(
        "validate", help="Validate project configuration and references"
    )
    p_validate.add_argument("--path", default=".", help="Project workspace path")
    p_validate.set_defaults(func=cmd_validate)

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Run diagnostic health checks")
    p_doctor.add_argument("--path", default=".", help="Project workspace path")
    p_doctor.set_defaults(func=cmd_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.subcommand:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
