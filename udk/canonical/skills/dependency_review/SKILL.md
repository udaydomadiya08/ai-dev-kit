---
name: "dependency_review"
description: "Evaluate third-party dependencies for licensing compatibility, security vulnerabilities, bundle size, and maintenance health."
version: "1.0.0"
tags: ["dependencies", "licenses", "audit"]
---

# Skill: Dependency and Compatibility Review

## 1. Purpose
Audit project dependencies to ensure legal compliance (licenses), security hygiene, ecosystem longevity, and cross-platform compatibility.

## 2. When to Use
* Proposing a new external dependency in `pyproject.toml` or `package.json`.
* Routine maintenance and automated dependency updates (Dependabot/Renovate).
* Pre-release governance audits.

## 3. When NOT to Use
* Managing standard library built-in modules.

## 4. Required Inputs
* Proposed package name and version constraint.
* Project license (e.g. Apache-2.0).
* Target platforms and supported runtimes.

## 5. Expected Outputs
* Dependency evaluation report covering license, footprint, security history, and maintenance activity.
* Justification of why standard library solutions are insufficient.

## 6. Repeatable Procedure
1. **Standard Library First**: Confirm whether standard library modules can accomplish the goal with reasonable code size.
2. **License Compatibility Check**: Verify that package license (e.g. MIT, BSD, Apache-2.0) is compatible with the project license. Reject copyleft (GPL) if the project is permissive.
3. **Security Audit**: Check vulnerability databases for reported CVEs on the package.
4. **Maintenance Assessment**: Check release frequency, open issues, and maintainer responsiveness.
5. **Transitive Footprint**: Check how many transitive dependencies the package introduces.
6. **Platform Portability**: Verify whether the package relies on native C extensions that break cross-platform installation.

## 7. Safety Boundaries
* Never pin dependencies to unversioned `*` wildcards or direct git branch heads in production configurations.
* Do not install unverified packages from personal package indices.

## 8. Verification Criteria
* Package installs cleanly on macOS, Linux, and Windows test environments.
* No reported CVEs in selected package version.

## 9. Example
* Review of YAML parsing: Chose built-in parser for frontmatter over adding external `pyyaml` dependency to keep core installation lightweight and zero-dependency.

## 10. Known Limitations
* Transitive vulnerabilities may emerge in downstream dependencies between audit cycles.
