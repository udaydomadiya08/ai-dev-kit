---
name: "architecture_review"
description: "Review architectural boundaries, design patterns, separation of concerns, and modularity across the codebase."
version: "1.0.0"
tags: ["architecture", "review", "design"]
---

# Skill: Architecture and Design Review

## 1. Purpose
Evaluate proposed or existing software structures against core architectural principles (modularity, loose coupling, high cohesion, determinism, and minimal blast radius).

## 2. When to Use
* Designing a new subsystem, adapter, or engine.
* Reviewing a major PR before merging.
* Refactoring legacy or tightly coupled components.

## 3. When NOT to Use
* Local bug fixes that do not change interfaces or dependencies.

## 4. Required Inputs
* Architectural diagrams, module definitions, or source files.
* Product requirements and non-functional goals (performance, portability).

## 5. Expected Outputs
* Architectural assessment report highlighting strengths, risks, and recommendations.
* Verification of interface boundaries and dependency direction.

## 6. Repeatable Procedure
1. **Analyze Separation of Concerns**: Ensure presentation/CLI layers do not execute database queries or disk I/O directly without engine abstractions.
2. **Review Dependency Direction**: Verify dependencies point inward toward stable core abstractions, not outward toward volatile details.
3. **Check State Management**: Ensure state mutations are centralized and explicit (e.g., manifest managers) rather than scattered.
4. **Evaluate Extensibility**: Confirm that adding a new adapter or profile does not require rewriting core compiler engines.
5. **Formulate Recommendations**: Provide concrete refactoring options with pros and cons.

## 7. Safety Boundaries
* Do not recommend introducing complex distributed frameworks (e.g. Kafka, microservices) for single-binary tools.
* Preserve backward compatibility for existing manifests and configurations.

## 8. Verification Criteria
* Core engine passes tests with all external dependencies mocked or using standard library.
* Circular dependencies are non-existent.

## 9. Example
* Review of UDK generator: Confirmed that `GeneratorEngine` depends on abstract `AgentAdapter`, allowing new adapters to be registered without modifying the generator loop.

## 10. Known Limitations
* Architecture reviews require engineering judgment and cannot be entirely automated by static linters.
