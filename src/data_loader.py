"""data.json 로드, 키 파싱, 필터·케이스 검증.

담당 요구사항: 04 §3(JSON 로드 및 스키마 검증), 04 §4(라벨 정규화 적용)
관련 문서: 03(실패 원인 분류), 04 §3·§4, 07(케이스 단위 FAIL·중단 금지), 09 §3, 09 §5 data_loader.py, 09 §6-4·§6-5·§6-9
"""
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .judge import CATEGORY_LABEL, CATEGORY_SCHEMA, CATEGORY_SIZE
from .labels import CROSS, X, LabelError, normalize_label
from .matrix import Matrix, MatrixFormatError

# 키 형식: 필터 size_{N}, 패턴 size_{N}_{idx}
FILTER_KEY_RE = re.compile(r"size_(\d+)")
PATTERN_KEY_RE = re.compile(r"size_(\d+)_(\d+)")


class SchemaError(ValueError):
    """필터·케이스 검증 실패. 분류와 사유를 가진다(09 §5)."""

    def __init__(self, category: str, reason: str) -> None:
        # 09 §5: 분류(스키마·크기·라벨)와 사유를 함께 보관
        super().__init__(reason)
        self.category = category
        self.reason = reason


class DataLoadError(Exception):
    """파일 없음, JSON 문법 오류, 최상위가 객체가 아닌 경우(09 §5)."""


def load_json(path: Path) -> Dict[str, Any]:
    # 04 §3: data.json 읽기. utf-8-sig는 BOM이 있어도 읽힌다(09 §6-9)
    try:
        with open(path, encoding="utf-8-sig") as file:
            raw = json.load(file)
    except FileNotFoundError:
        raise DataLoadError(f"파일을 찾을 수 없음: {path}") from None
    except json.JSONDecodeError as error:
        raise DataLoadError(f"JSON 문법 오류: {error}") from None
    except UnicodeDecodeError:
        raise DataLoadError(f"UTF-8로 읽을 수 없는 파일: {path}") from None
    except OSError as error:
        raise DataLoadError(f"파일을 읽을 수 없음: {error}") from None
    if not isinstance(raw, dict):
        raise DataLoadError("최상위 값이 JSON 객체가 아님")
    return raw


def parse_filter_key(key: str) -> int:
    # 04 §3: 필터 키 size_{N}에서 N 추출
    match = FILTER_KEY_RE.fullmatch(key) if isinstance(key, str) else None
    if match is None:
        raise SchemaError(CATEGORY_SCHEMA, f"필터 키 형식 오류({key!r}, 필요 형식 size_N)")
    return int(match.group(1))


def parse_pattern_key(key: str) -> Tuple[int, int]:
    # 04 §3: 패턴 키 size_{N}_{idx}에서 (N, idx) 추출
    match = PATTERN_KEY_RE.fullmatch(key) if isinstance(key, str) else None
    if match is None:
        raise SchemaError(CATEGORY_SCHEMA, f"패턴 키 형식 오류({key!r}, 필요 형식 size_N_idx)")
    return int(match.group(1)), int(match.group(2))


def _load_filter_pair(n: int, value: Any) -> Dict[str, Matrix]:
    """크기 n의 필터 묶음 하나를 검증해 {Cross: Matrix, X: Matrix}로 반환한다."""
    if not isinstance(value, dict):
        raise SchemaError(CATEGORY_SCHEMA, "필터 값이 객체가 아님")
    pair: Dict[str, Matrix] = {}
    for sub_key, rows in value.items():
        try:
            label = normalize_label(sub_key)
        except LabelError as error:
            raise SchemaError(CATEGORY_LABEL, f"필터 라벨 오류: {error}") from None
        if label in pair:
            raise SchemaError(CATEGORY_LABEL, f"정규화 후 중복된 필터 라벨({label})")
        try:
            pair[label] = Matrix.from_rows(rows, n)
        except MatrixFormatError as error:
            raise SchemaError(CATEGORY_SIZE, f"{label} 필터: {error}") from None
    missing = [label for label in (CROSS, X) if label not in pair]
    if missing:
        raise SchemaError(CATEGORY_SCHEMA, f"필터 누락: {', '.join(missing)}")
    return pair


def load_filters(raw: Dict[str, Any]) -> Tuple[Dict[int, Dict[str, Matrix]], Dict[str, str]]:
    # 04 §3: filters의 크기별 필터 로드와 N×N 검증
    # 04 §4: 하위 키 'cross' → Cross, 'x' → X 정규화, 누락·중복은 오류
    # 07: 실패한 크기는 errors에 사유를 남기고 나머지는 계속 처리
    filters: Dict[int, Dict[str, Matrix]] = {}
    errors: Dict[str, str] = {}
    section = raw.get("filters")
    if not isinstance(section, dict):
        errors["filters"] = "filters 항목이 없거나 객체가 아님"
        return filters, errors
    for key, value in section.items():
        try:
            n = parse_filter_key(key)
            if n in filters:
                raise SchemaError(CATEGORY_SCHEMA, f"크기 {n}의 필터가 중복됨")
            filters[n] = _load_filter_pair(n, value)
        except SchemaError as error:
            errors[str(key)] = error.reason
    return filters, errors


def _shape_text(rows: List[Any]) -> str:
    """input의 모양을 'R×C' 또는 'R행(열 수 제각각)'으로 표기한다."""
    widths = {len(row) for row in rows}
    if len(widths) == 1:
        return f"{len(rows)}×{widths.pop()}"
    return f"{len(rows)}행(열 수 {sorted(widths)})"


def build_case(
    case_id: str,
    entry: Any,
    filters: Dict[int, Dict[str, Matrix]],
    errors: Dict[str, str],
) -> Tuple[int, Matrix, Dict[str, Matrix], str]:
    # 04 §3: 키에서 추출한 N으로 size_N 필터 선택, 필터·패턴 크기 불일치는 SchemaError(사유)
    # 04 §4: expected '+' → Cross, 'x' → X 정규화
    # 09 §5: 실패 분류는 스키마·크기·라벨(실패 분류 표)
    n, _ = parse_pattern_key(case_id)
    if n not in filters:
        cause = errors.get(f"size_{n}") or errors.get("filters")
        detail = f" (로드 실패: {cause})" if cause else ""
        raise SchemaError(CATEGORY_SCHEMA, f"size_{n} 필터 없음{detail}")
    if not isinstance(entry, dict):
        raise SchemaError(CATEGORY_SCHEMA, "패턴 항목이 객체가 아님")
    missing = [field for field in ("input", "expected") if field not in entry]
    if missing:
        raise SchemaError(CATEGORY_SCHEMA, f"필드 누락: {', '.join(missing)}")
    rows = entry["input"]
    if not isinstance(rows, list) or not all(isinstance(row, list) for row in rows):
        raise SchemaError(CATEGORY_SCHEMA, "input이 2차원 리스트가 아님")
    if len(rows) != n or any(len(row) != n for row in rows):
        shape = _shape_text(rows) if rows else "0행"
        raise SchemaError(CATEGORY_SIZE, f"크기 불일치: 필터 {n}×{n}, 패턴 {shape}")
    try:
        pattern = Matrix.from_rows(rows, n)
    except MatrixFormatError as error:
        raise SchemaError(CATEGORY_SCHEMA, f"input 값 오류: {error}") from None
    try:
        expected = normalize_label(entry["expected"])
    except LabelError as error:
        raise SchemaError(CATEGORY_LABEL, f"expected {error}") from None
    return n, pattern, filters[n], expected
