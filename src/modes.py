"""모드별 실행 흐름.

담당 요구사항: 04 §10(실행 흐름), 05 §2(B2 모드 3)
관련 문서: 04 §10, 05 §2, 07(재현성), 08(실행 예시), 09 §0-5·§0-9, 09 §5 modes.py, 09 §6-3·§6-4·§6-7, 09 §7
"""
from pathlib import Path
from typing import Optional, Tuple

from .matrix import Matrix


def run_user_mode() -> None:
    """사용자 입력 모드 실행"""
    # TODO: 04 §10: 필터 A, B 입력 → 저장 확인 → 패턴 입력 → MAC 연산 → 결과 판정 → 성능 분석(3×3) 출력
    raise NotImplementedError("TODO: run_user_mode")


def run_json_mode(path: Path) -> None:
    # TODO: 04 §10: 필터 로드 → 패턴 로드/검증 → MAC 연산/판정/PASS-FAIL 출력 → 성능 분석(3×3 포함, 5×5/13×13/25×25) → 결과 요약
    # TODO: 07: 스키마·크기 불일치가 있어도 중단 없이 케이스 단위 FAIL
    raise NotImplementedError("TODO: run_json_mode")


def run_generator_mode() -> None:
    # TODO: 05 §2: 크기 N 입력 → Cross/X 필터·패턴 생성 → 모드 1 처리 파이프라인 재사용(09 §0-5)
    # TODO: 09 §0-9: 선택한 패턴 종류를 expected로 PASS/FAIL 표시
    raise NotImplementedError("TODO: run_generator_mode")


def run_pair_pipeline(
    filter_a: Matrix,
    filter_b: Matrix,
    pattern: Matrix,
    labels: Tuple[str, str],
    expected: Optional[str] = None,
) -> None:
    # TODO: 09 §5: 모드 1·3 공용, MAC → 판정 → (expected가 있으면 PASS/FAIL) → 성능 표 → B1 비교 표
    raise NotImplementedError("TODO: run_pair_pipeline")
