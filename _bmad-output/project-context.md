---
project_name: 'iMaotai'
user_name: 'Cc'
date: '2026-02-18'
sections_completed: ['technology_stack', 'language_rules', 'testing_rules', 'quality_rules', 'critical_rules']
status: 'complete'
rule_count: 18
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Python:** 3.9+ (strictly verified with type hints)
- **OCR:** `paddleocr>=2.7.0` (PP-OCRv3/v4 Mobile models)
- **Deep Learning:** `paddlepaddle>=2.5.0`
- **ADB:** `pure-python-adb>=0.3.0`
- **Vision:** `opencv-python`
- **Stealth Math:** `scipy`, `numpy`
- **Connectivity:** Local ADB Server (port 5037)

## Critical Implementation Rules

### Language-Specific Rules (Python)

- **Type Safety:** All public functions MUST include complete Type Hints.
- **Concurrency:** Prefer `threading` for screenshot streaming over `asyncio` due to PPADB blocking nature.
- **Coordinate Format:** Strictly avoid `list` or `tuple` for coordinate exchange. Use `TypedDict` for `{"x": int, "y": int}`.
- **Resource Management:** Ensure all image Mat objects and ADB connections are handled with context managers or explicit `close()` logic.

### Testing Rules

- **Co-location:** Test files `test_*.py` MUST be placed in the same directory as the source code.
- **OCR Mocking:** Unit tests MUST use pre-stored images from `data/templates/`; establishing real ADB connections during unit tests is forbidden.
- **Retry Logic:** Methods involving vision matching MUST utilize the `@retry_on_failure` decorator.

### Code Quality & Style Rules

- **Naming Convention:** Strictly follow `snake_case` for functions, variables, and file names.
- **JSON Schema:** Use `snake_case` for all keys in configuration files (no `camelCase`).
- **Logging:** Every OCR recognition result and its confidence score must be logged for traceability.

### Critical Don't-Miss Rules

- **ANTI-PATTERN:** Never hardcode physical pixel coordinates. All inputs must undergo normalization conversion based on screen resolution.
- **PRIVACY:** Screenshots and recognized text must never be written outside the designated `logs/` or `temp/` directories.
- **EDGE CASE:** Always handle scenarios where OCR returns an empty list to prevent index out of range errors.
- **STEALTH:** All touch actions at Level 2 or higher must include randomized `pressure` and `size` parameters to bypass behavioral detection.

---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code.
- Follow ALL rules exactly as documented.
- When in doubt, prefer the more restrictive option.
- Update this file if new patterns emerge during development.

**For Humans:**
- Keep this file lean and focused on agent needs.
- Update when the technology stack or core architecture changes.
- Review periodically to remove rules that have become "obvious" to the agents.

Last Updated: 2026-02-18
