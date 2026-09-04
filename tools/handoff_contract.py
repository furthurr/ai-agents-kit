#!/usr/bin/env python3
"""Parse and validate portable Markdown handoffs used by the agent kit."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


REQUIRED_HANDOFF_FIELDS = {
    "handoff_id",
    "source",
    "target",
    "action",
    "handoff_reason",
    "project_root",
    "scope",
    "context_refs",
    "write_scope",
    "requires_confirmation",
    "status",
}
OPTIONAL_HANDOFF_FIELDS = {"gate_state"}
TARGET_SCOPES = {
    "project-navigator": ".navigator/",
    "architecture": ".architecture/",
    "data-api": ".data/",
    "ui-design": ".design/",
    "code-quality": ".quality/",
    "security": ".security/",
}
ACTIONS = {"inspect", "bootstrap", "sync", "audit-documentation"}
HANDOFF_ID = re.compile(r"^HND-\d{8}-\d{3,}$")


def parse_markdown_fields(block: str) -> dict[str, Any]:
    """Parse ``- key: value`` fields and indented list values from a block."""
    result: dict[str, Any] = {}
    list_key: str | None = None
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line or line in {"## Handoff", "## Handoff Result"}:
            continue
        field = re.match(r"^- ([a-z_]+):(?:\s*(.*))?$", line)
        if field:
            key, value = field.groups()
            if key in result:
                raise ValueError(f"Campo duplicado: {key}")
            if value:
                result[key] = _parse_scalar(value)
                list_key = None
            else:
                result[key] = []
                list_key = key
            continue
        item = re.match(r"^\s{2,}- (.+)$", line)
        if item and list_key:
            result[list_key].append(item.group(1).strip())
            continue
        raise ValueError(f"Línea no admitida en handoff: {line}")
    return result


def extract_first_markdown_block(document: str, heading: str) -> str:
    """Return the first fenced Markdown block after ``heading``."""
    section = document.split(heading, maxsplit=1)
    if len(section) != 2:
        raise ValueError(f"Falta la sección {heading!r}")
    match = re.search(r"```markdown\n(.*?)\n```", section[1], re.DOTALL)
    if not match:
        raise ValueError(f"Falta bloque Markdown después de {heading!r}")
    return match.group(1)


def validate_handoff(
    data: dict[str, Any], workspace_root: Path, *, check_exists: bool = True
) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_HANDOFF_FIELDS - data.keys())
    if missing:
        errors.append(f"Faltan campos obligatorios: {', '.join(missing)}")
        return errors
    unknown = sorted(data.keys() - REQUIRED_HANDOFF_FIELDS - OPTIONAL_HANDOFF_FIELDS)
    if unknown:
        errors.append(f"Campos no admitidos: {', '.join(unknown)}")

    if not _valid_handoff_id(data["handoff_id"]):
        errors.append("handoff_id no cumple HND-YYYYMMDD-NNN")
    if data["source"] != "documentation-orchestrator":
        errors.append("source debe ser documentation-orchestrator")
    target = data["target"]
    if not isinstance(target, str) or target not in TARGET_SCOPES:
        errors.append("target no admitido")
    if not isinstance(data["action"], str) or data["action"] not in ACTIONS:
        errors.append("action no admitida")
    if not isinstance(data["handoff_reason"], str) or not data["handoff_reason"].strip():
        errors.append("handoff_reason no puede estar vacío")
    if not isinstance(data["status"], str) or data["status"] != "pending":
        errors.append("un handoff emitido debe tener status pending")
    if "gate_state" in data and not isinstance(data["gate_state"], list):
        errors.append("gate_state debe ser una lista")

    project_root = _resolve_safe_path(
        workspace_root, data["project_root"], "project_root", errors, check_exists=True
    )
    expected_scope = TARGET_SCOPES.get(target) if isinstance(target, str) else None
    if expected_scope and data["scope"] != expected_scope:
        errors.append(f"scope debe ser {expected_scope} para target {data['target']}")

    refs = data["context_refs"]
    if not isinstance(refs, list) or not refs:
        errors.append("context_refs debe ser una lista no vacía")
    elif project_root:
        for reference in refs:
            _resolve_safe_path(project_root, reference, "context_refs", errors, check_exists=check_exists)

    if data["action"] == "inspect":
        if data["write_scope"] != "none":
            errors.append("inspect requiere write_scope none")
        if data["requires_confirmation"] is not False:
            errors.append("inspect requiere requires_confirmation false")
    else:
        if expected_scope and data["write_scope"] != expected_scope:
            errors.append(f"{data['action']} requiere write_scope {expected_scope}")
        if data["requires_confirmation"] is not True:
            errors.append("una acción con escritura requiere requires_confirmation true")

    if project_root and expected_scope:
        _resolve_safe_path(
            project_root,
            expected_scope,
            "scope",
            errors,
            check_exists=check_exists and data["action"] != "bootstrap",
        )
    return errors


def validate_result(
    data: dict[str, Any],
    workspace_root: Path,
    *,
    expected_handoff: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    required = {"handoff_id", "status", "result_summary"}
    missing = sorted(required - data.keys())
    if missing:
        return [f"Faltan campos obligatorios: {', '.join(missing)}"]
    if expected_handoff is None:
        errors.append("expected_handoff es obligatorio para validar correlación y scope")
    else:
        handoff_errors = validate_handoff(expected_handoff, workspace_root)
        if handoff_errors:
            errors.append("expected_handoff no es válido: " + "; ".join(handoff_errors))
    unknown = sorted(data.keys() - required - {"evidence"})
    if unknown:
        errors.append(f"Campos no admitidos: {', '.join(unknown)}")
    if not _valid_handoff_id(data["handoff_id"]):
        errors.append("handoff_id no cumple HND-YYYYMMDD-NNN")
    expected_handoff_id = expected_handoff.get("handoff_id") if expected_handoff else None
    if expected_handoff_id and data["handoff_id"] != expected_handoff_id:
        errors.append("handoff_id no coincide con la emisión")
    status = data["status"]
    if not isinstance(status, str) or status not in {"delivered", "blocked"}:
        errors.append("status de resultado no admitido")
    if not isinstance(data["result_summary"], str) or not data["result_summary"].strip():
        errors.append("result_summary no puede estar vacío")
    evidence = data.get("evidence", [])
    if "evidence" in data and not isinstance(evidence, list):
        errors.append("evidence debe ser una lista")
    if status == "delivered" and (not isinstance(evidence, list) or not evidence):
        errors.append("delivered requiere evidence no vacío")
    if status == "blocked" and "evidence" in data:
        errors.append("blocked debe omitir evidence")
    project_root = expected_handoff.get("project_root", ".") if expected_handoff else "."
    evidence_root = _resolve_safe_path(
        workspace_root, project_root, "project_root", errors, check_exists=True
    )
    scope_root: Path | None = None
    if expected_handoff and evidence_root and status == "delivered":
        scope = expected_handoff.get("scope")
        scope_root = _resolve_safe_path(
            evidence_root, scope, "scope", errors, check_exists=True
        )
    if isinstance(evidence, list) and evidence_root:
        for reference in evidence:
            resolved = _resolve_safe_path(
                evidence_root, reference, "evidence", errors, check_exists=True
            )
            if resolved and not resolved.is_file():
                errors.append(f"evidence debe ser un archivo: {reference}")
            if resolved and scope_root and resolved != scope_root and scope_root not in resolved.parents:
                errors.append(f"evidence sale del scope: {reference}")
    return errors


def _valid_handoff_id(value: Any) -> bool:
    if not isinstance(value, str) or not HANDOFF_ID.fullmatch(value):
        return False
    try:
        datetime.strptime(value[4:12], "%Y%m%d")
    except ValueError:
        return False
    return True


def _parse_scalar(value: str) -> Any:
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        return [] if not body else [item.strip() for item in body.split(",")]
    return value


def _resolve_safe_path(
    base: Path,
    raw_value: Any,
    field: str,
    errors: list[str],
    *,
    check_exists: bool,
) -> Path | None:
    if not isinstance(raw_value, str) or not raw_value:
        errors.append(f"{field} debe ser una ruta no vacía")
        return None
    if "#" in raw_value:
        errors.append(f"{field} no admite fragmentos #")
        return None
    candidate = PurePosixPath(raw_value)
    windows_candidate = PureWindowsPath(raw_value)
    if (
        "\\" in raw_value
        or candidate.is_absolute()
        or windows_candidate.is_absolute()
        or windows_candidate.drive
        or ".." in candidate.parts
    ):
        errors.append(f"{field} debe ser relativa y sin ..")
        return None
    base_resolved = base.resolve()
    resolved = (base_resolved / Path(*candidate.parts)).resolve()
    if resolved != base_resolved and base_resolved not in resolved.parents:
        errors.append(f"{field} escapa del proyecto")
        return None
    if check_exists and not resolved.exists():
        errors.append(f"{field} no existe: {raw_value}")
    return resolved
