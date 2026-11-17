"""data.json 로드, 키 파싱, 필터·케이스 검증.

담당 요구사항: 04 §3(JSON 로드 및 스키마 검증), 04 §4(라벨 정규화 적용)
관련 문서: 03(실패 원인 분류), 04 §3·§4, 07(케이스 단위 FAIL·중단 금지), 09 §3, 09 §5 data_loader.py, 09 §6-4·§6-5·§6-9
"""
from pathlib import Path
from typing import Any, Dict, Tuple

from .matrix import Matrix


class SchemaError(ValueError):
    """필터·케이스 검증 실패. 분류와 사유를 가진다(09 §5)."""

    def __init__(self, category: str, reason: str) -> None:
        # TODO: 09 §5: 분류(스키마·크기·라벨)와 사유를 함께 보관
        raise NotImplementedError("TODO: SchemaError.__init__")


class DataLoadError(Exception):
    """파일 없음, JSON 문법 오류, 최상위가 객체가 아닌 경우(09 §5)."""


def load_json(path: Path) -> Dict[str, Any]:
    # TODO: 04 §3: data.json 읽기(utf-8-sig, 09 §6-9), 파일 없음·문법 오류·최상위 비객체는 DataLoadError(중단 금지)
    raise NotImplementedError("TODO: load_json")


def parse_filter_key(key: str) -> int:
    # TODO: 04 §3: 필터 키 size_{N}에서 N 추출, 형식 오류는 SchemaError
    raise NotImplementedError("TODO: parse_filter_key")


def parse_pattern_key(key: str) -> Tuple[int, int]:
    # TODO: 04 §3: 패턴 키 size_{N}_{idx}에서 (N, idx) 추출, 형식 오류는 SchemaError
    raise NotImplementedError("TODO: parse_pattern_key")


def load_filters(raw: Dict[str, Any]) -> Tuple[Dict[int, Dict[str, Matrix]], Dict[str, str]]:
    # TODO: 04 §3: filters의 size_5·size_13·size_25 로드, 크기별 N×N 검증
    # TODO: 04 §4: 하위 키 'cross' → Cross, 'x' → X 정규화, 누락·중복은 오류
    # TODO: 07: 실패한 크기는 errors에 사유를 남기고 나머지는 계속 처리
    raise NotImplementedError("TODO: load_filters")


def build_case(
    case_id: str,
    entry: Any,
    filters: Dict[int, Dict[str, Matrix]],
    errors: Dict[str, str],
) -> Tuple[int, Matrix, Dict[str, Matrix], str]:
    # TODO: 04 §3: 키에서 추출한 N으로 size_N 필터 선택, 필터·패턴 크기 불일치는 SchemaError(사유)
    # TODO: 04 §4: expected '+' → Cross, 'x' → X 정규화
    # TODO: 09 §5: 실패 분류는 스키마·크기·라벨(실패 분류 표)
    raise NotImplementedError("TODO: build_case")
