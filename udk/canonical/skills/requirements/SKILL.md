---
name: "requirements"
description: "Clarify ambiguous user requests, extract functional constraints, and define verifiable acceptance criteria."
version: "1.0.0"
tags: ["planning", "specification", "requirements"]
---

# Skill: Requirements Clarification and Planning

## 1. Purpose
Transform broad or underspecified user objectives into concrete, verifiable functional requirements, non-functional constraints, and phased implementation plans.

## 2. When to Use
* Starting a new feature, project profile, or major refactor.
* User requests contain ambiguity, conflicting goals, or missing edge case definitions.
* The blast radius of the work impacts multiple modules.

## 3. When NOT to Use
* Resolving clear, atomic tasks (e.g. "change port 8080 to 9000").
* Immediate hotfixes where the defect is already reproduced and isolated.

## 4. Required Inputs
* User prompt or issue description.
* Current project architecture, codebase state, and test suites.

## 5. Expected Outputs
* Structured task plan with phases, scope, and non-goals.
* Specific acceptance criteria checklist.
* Risk assessment and regression prevention strategy.

## 6. Repeatable Procedure
1. **Deconstruct Request**: Break prompt into functional objectives and implicit constraints.
2. **Context Discovery**: Scan codebase for existing conventions or precedents matching the request.
3. **Draft Acceptance Criteria**: Formulate measurable, testable gates (e.g. "CLI command `udk doctor` exits 0 and reports all passing checks").
4. **Identify Non-Goals**: Explicitly document out-of-scope items to prevent scope creep.
5. **Phase Sequencing**: Order work dependencies so that core modules are tested before higher-level facades.

## 7. Safety Boundaries
* Do not make assumptions on high-risk operations (e.g. database schema migrations or data deletion) without user validation.
* Do not invent requirements that contradict explicit project principles.

## 8. Verification Criteria
* Plan includes at least one negative or boundary test case.
* Acceptance criteria are executable or observable.

## 9. Example
* **User Request**: "Add support for mobile profile."
* **Clarified Output**: Scope defined as React Native / Flutter conventions; generates appropriate `AGENTS.md` and test commands; non-goal: building a full native mobile simulator.

## 10. Known Limitations
* Relies on developer feedback if business goals have fundamental architectural contradictions.
