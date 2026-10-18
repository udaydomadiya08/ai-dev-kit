---
name: "research"
description: "Conduct evidence-based technical research on APIs, dependencies, and external standards before modifying code."
version: "1.0.0"
tags: ["research", "investigation", "standards"]
---

# Skill: Research Before Implementation

## 1. Purpose
Investigate technical standards, official documentation, library capabilities, and interface specifications before proposing architectural designs or committing code changes.

## 2. When to Use
* Integrating a new third-party library, external API, or protocol.
* Addressing an unfamiliar error or deprecation warning.
* Choosing between architectural patterns or technology choices.

## 3. When NOT to Use
* Performing trivial localized bug fixes where the codebase already establishes clear patterns.
* Making minor typos or formatting adjustments.

## 4. Required Inputs
* Technical query or proposed library name.
* Context of current project runtime, language version, and operating systems.
* Licensing constraints (e.g. permissive vs copyleft).

## 5. Expected Outputs
* Summary of authoritative findings with citation of official documentation or source repos.
* Verified compatibility with current project dependencies.
* Concrete code snippet or interface design demonstrating the pattern.

## 6. Repeatable Procedure
1. **Identify Authoritative Sources**: Query official documentation, specification RFCs, or trusted repository READMEs.
2. **Verify License & Provenance**: Ensure third-party licenses (MIT, Apache-2.0, BSD) are compatible with the repository.
3. **Assess Maturity & Maintenance**: Verify active maintenance, recent releases, and known vulnerability records.
4. **Synthesize Findings**: Document key trade-offs, configuration requirements, and interface constraints.
5. **Formulate Next Steps**: Transition findings into a structured implementation plan.

## 7. Safety Boundaries
* Do not execute arbitrary scripts from unverified web repositories.
* Do not install packages globally on the host machine.
* Do not download proprietary or restricted codebases.

## 8. Verification Criteria
* Research notes cite authoritative URLs or repository sources.
* Findings specify verified version numbers matching the project environment.
* Prototype code passes static syntax checks.

## 9. Example
* **Scenario**: Developer wants to add YAML frontmatter parsing in Python.
* **Procedure**: Research evaluates `pyyaml` vs lightweight manual parsing vs `ruamel.yaml`. Recommends zero-dependency regex/split parser for basic frontmatter to preserve zero-dependency core principle.

## 10. Known Limitations
* Offline environments cannot fetch new web resources and must rely on local documentation and package metadata.
