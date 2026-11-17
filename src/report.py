"""콘솔 출력: 배너, 섹션, 점수, 표, 결과 요약.

담당 요구사항: 04 §9(결과 리포트 콘솔 출력), 04 §7(판정·PASS/FAIL 출력), 04 §8(성능 표), 05 §1(B1 비교 표)
관련 문서: 04 §7·§8·§9·§10, 05 §1, 08(출력 예시), 09 §0-8, 09 §5 report.py, 09 §6-8
"""
from typing import Dict, List, Tuple

from .benchmark import BenchRow
from .judge import CaseResult
from .matrix import Matrix


def print_banner() -> None:
    # TODO: 04 §10: 실행 시 프로그램 제목 출력(08 예시 형식)
    raise NotImplementedError("TODO: print_banner")


def print_section(title: str) -> None:
    # TODO: 08: 단계별 섹션 머리글([1]~[4]) 출력
    raise NotImplementedError("TODO: print_section")


def print_matrix(m: Matrix) -> None:
    # TODO: 04 §10: 모드 1 저장 확인용 행렬 출력(04 §1 읽기 기능 사용)
    raise NotImplementedError("TODO: print_matrix")


def format_score(x: float) -> str:
    # TODO: 09 §6-8: 반올림 없는 기본 float 표기
    raise NotImplementedError("TODO: format_score")


def print_pair_result(score_a: float, score_b: float, verdict: str, labels: Tuple[str, str]) -> None:
    # TODO: 04 §7: 두 필터 점수와 판정 출력(모드 1: A/B/판정 불가, 모드 3: Cross/X/UNDECIDED)
    # TODO: 09 §6-8: 동점이면 두 점수의 차이값 함께 출력
    raise NotImplementedError("TODO: print_pair_result")


def print_filter_status(filters: Dict[int, Dict[str, Matrix]], errors: Dict[str, str]) -> None:
    # TODO: 04 §10: 크기별 필터 로드 결과(완료 또는 실패 사유) 출력
    raise NotImplementedError("TODO: print_filter_status")


def print_case(result: CaseResult) -> None:
    # TODO: 04 §7: 케이스별 Cross 점수, X 점수, 판정(Cross/X/UNDECIDED), expected, PASS/FAIL 출력
    # TODO: 04 §3: 검증 실패 케이스는 FAIL과 사유 출력
    raise NotImplementedError("TODO: print_case")


def print_perf_table(rows: List[BenchRow]) -> None:
    # TODO: 04 §8: 크기(N×N) / 평균 시간(ms) / 연산 횟수(N²) 표 출력
    raise NotImplementedError("TODO: print_perf_table")


def print_opt_compare(rows: List[BenchRow]) -> None:
    # TODO: 05 §1: 크기 / 2D(ms) / 1D(ms) / 1D÷2D / 결과 일치 비교 표, 필수 표와 별도 출력(09 §0-8)
    # TODO: 09 §0-7: 2D·1D 결과가 다르면 경고 출력
    raise NotImplementedError("TODO: print_opt_compare")


def print_summary(results: List[CaseResult]) -> None:
    # TODO: 04 §9: 전체 테스트 수·통과 수·실패 수, 실패 케이스 식별자와 사유(요약) 출력
    # TODO: 07: 총 테스트 수 = 통과 수 + 실패 수
    raise NotImplementedError("TODO: print_summary")
