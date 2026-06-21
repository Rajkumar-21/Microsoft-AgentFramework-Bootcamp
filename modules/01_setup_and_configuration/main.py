"""
Module 01 — Setup & Configuration
=================================

Scenario: "Atlas" platform readiness check
------------------------------------------
You are the platform engineer onboarding a new team onto *Atlas*, an internal
agent platform built on the Microsoft Agent Framework. Before anyone writes an
agent, every workstation and CI runner must pass a readiness gate.

This module is a production-style pre-flight validator. It checks:
  * Python runtime (Agent Framework requires 3.10+, this bootcamp targets 3.13+)
  * The `agent-framework` package and its installed version
  * Required Azure OpenAI configuration
  * Optional Azure AI Foundry + observability configuration
  * Emits a machine-readable summary (exit code 0 = ready, 1 = blocked)

It never calls a model, so it is safe to run in CI:

    python main.py
"""

from __future__ import annotations

import importlib.metadata as metadata
import os
import sys
from dataclasses import dataclass, field


MIN_PYTHON = (3, 10)
RECOMMENDED_PYTHON = (3, 13)


@dataclass
class CheckResult:
    """Outcome of a single readiness check."""

    name: str
    ok: bool
    detail: str
    blocking: bool = True


@dataclass
class Report:
    results: list[CheckResult] = field(default_factory=list)

    def add(self, result: CheckResult) -> None:
        self.results.append(result)

    @property
    def blockers(self) -> list[CheckResult]:
        return [r for r in self.results if r.blocking and not r.ok]

    @property
    def is_ready(self) -> bool:
        return not self.blockers


def _mask(value: str) -> str:
    """Mask secrets so they never land in CI logs."""
    if len(value) <= 8:
        return "***"
    return f"{value[:6]}…{value[-2:]}"


def check_python(report: Report) -> None:
    current = sys.version_info[:2]
    if current < MIN_PYTHON:
        report.add(
            CheckResult(
                "Python runtime",
                ok=False,
                detail=f"Found {current[0]}.{current[1]}, need >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}",
            )
        )
    else:
        note = "" if current >= RECOMMENDED_PYTHON else "  (3.13+ recommended)"
        report.add(
            CheckResult("Python runtime", ok=True, detail=f"{current[0]}.{current[1]}{note}")
        )


def check_package(report: Report) -> None:
    try:
        version = metadata.version("agent-framework")
        report.add(CheckResult("agent-framework", ok=True, detail=f"v{version}"))
    except metadata.PackageNotFoundError:
        report.add(
            CheckResult(
                "agent-framework",
                ok=False,
                detail="not installed — run `uv add agent-framework` or `pip install agent-framework`",
            )
        )


def check_env(report: Report) -> None:
    required = {
        "AZURE_OPENAI_ENDPOINT": "Azure OpenAI resource URL (https://<name>.openai.azure.com)",
        "AZURE_OPENAI_API_KEY": "Azure OpenAI API key",
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": "Chat model deployment name (e.g. gpt-4o)",
    }
    optional = {
        "AZURE_AI_PROJECT_ENDPOINT": "Azure AI Foundry project endpoint",
        "AZURE_AI_MODEL_DEPLOYMENT_NAME": "Foundry model deployment name",
        "APPLICATIONINSIGHTS_CONNECTION_STRING": "OpenTelemetry / App Insights export",
    }

    for var, desc in required.items():
        value = os.environ.get(var)
        report.add(
            CheckResult(var, ok=bool(value), detail=_mask(value) if value else f"missing — {desc}")
        )

    for var, desc in optional.items():
        value = os.environ.get(var)
        report.add(
            CheckResult(
                var,
                ok=bool(value),
                detail=_mask(value) if value else f"not set — {desc}",
                blocking=False,
            )
        )


def render(report: Report) -> None:
    print("=" * 64)
    print("  Atlas platform readiness check")
    print("=" * 64)
    for r in report.results:
        icon = "✓" if r.ok else ("✗" if r.blocking else "○")
        print(f"  {icon} {r.name:<38} {r.detail}")
    print("-" * 64)
    if report.is_ready:
        print("  ✓ READY — environment passed all blocking checks.")
    else:
        names = ", ".join(b.name for b in report.blockers)
        print(f"  ✗ BLOCKED — fix: {names}")
    print("=" * 64)


def main() -> int:
    report = Report()
    check_python(report)
    check_package(report)
    check_env(report)
    render(report)
    return 0 if report.is_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
