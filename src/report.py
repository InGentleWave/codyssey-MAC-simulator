"""콘솔 출력: 배너, 섹션, 점수, 표, 결과 요약.

담당 요구사항: 04 §9(결과 리포트 콘솔 출력), 04 §7(판정·PASS/FAIL 출력), 04 §8(성능 표), 05 §1(B1 비교 표)
관련 문서: 04 §7·§8·§9·§10, 05 §1, 08(출력 예시), 09 §0-8, 09 §0-11, 09 §5 report.py, 09 §6-8
"""
import unicodedata
from typing import Dict, List, Optional, Tuple

from .benchmark import BenchRow
from .config import EPSILON
from .judge import FAIL, PASS, CaseResult
from .labels import CROSS, UNDECIDED, X
from .matrix import Matrix

SECTION_LINE = "#" + "-" * 39


def _width(text: str) -> int:
    """콘솔 표시 폭(한글 등 전각 문자는 2칸)."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def _pad(text: str, width: int, right: bool = False) -> str:
    """표시 폭 기준으로 공백을 채워 정렬한다."""
    gap = " " * max(width - _width(text), 0)
    return gap + text if right else text + gap


def print_banner() -> None:
    # 04 §10: 실행 시 프로그램 제목 출력(08 예시 형식)
    print("=== Mini NPU Simulator ===")


def print_section(title: str) -> None:
    # 08: 단계별 섹션 머리글([1]~[4]) 출력
    print()
    print(SECTION_LINE)
    print(f"# {title}")
    print(SECTION_LINE)


def print_matrix(m: Matrix) -> None:
    # 04 §10: 모드 1 저장 확인용 행렬 출력(04 §1 읽기 기능 get 사용)
    for r in range(m.size):
        print(" ".join(format_score(m.get(r, c)) for c in range(m.size)))


def format_score(x: float) -> str:
    # 09 §6-8: 반올림 없는 기본 float 표기(0.9와 0.8999999999999999를 구분)
    return repr(float(x))


def print_pair_result(
    score_a: float,
    score_b: float,
    verdict: str,
    labels: Tuple[str, str],
    undecided_text: str = UNDECIDED,
    expected: Optional[str] = None,
    status: Optional[str] = None,
) -> None:
    # 04 §7: 두 필터 점수와 판정 출력(모드 1: A/B/판정 불가, 모드 3: Cross/X/UNDECIDED)
    # 09 §0-11: undecided_text는 동점 표시 문구, expected·status는 모드 3의 PASS/FAIL 표시용
    label_a, label_b = labels
    print(f"{label_a} 점수: {format_score(score_a)}")
    print(f"{label_b} 점수: {format_score(score_b)}")
    if verdict == UNDECIDED:
        # 09 §6-8: 동점이면 두 점수의 차이값 함께 출력
        diff = abs(score_a - score_b)
        text = f"{undecided_text} (|{label_a}-{label_b}| = {diff:.3g} < {EPSILON:g})"
    else:
        text = verdict
    line = f"판정: {text}"
    if expected is not None:
        line += f" | expected: {expected} | {status}"
    print(line)


def print_filter_status(filters: Dict[int, Dict[str, Matrix]], errors: Dict[str, str]) -> None:
    # 04 §10: 크기별 필터 로드 결과(완료 또는 실패 사유) 출력
    for n in filters:
        print(f"{_pad(f'size_{n}', 8)}필터 로드 완료 ({CROSS}, {X})")
    for key, reason in errors.items():
        print(f"{_pad(key, 8)}필터 로드 실패: {reason}")
    if not filters and not errors:
        print("로드할 필터가 없습니다.")


def print_case(result: CaseResult) -> None:
    # 04 §7: 케이스별 Cross 점수, X 점수, 판정(Cross/X/UNDECIDED), expected, PASS/FAIL 출력
    # 04 §3: 검증 실패 케이스는 FAIL과 사유 출력
    print(f"--- {result.case_id} ---")
    if result.cross_score is not None and result.x_score is not None:
        print(f"Cross 점수: {format_score(result.cross_score)}")
        print(f"X 점수: {format_score(result.x_score)}")
        print(f"판정: {result.verdict} | expected: {result.expected} | {result.status}")
    else:
        print(result.status)
    if result.status == FAIL:
        print(f"사유: [{result.category}] {result.reason}")


def print_perf_table(rows: List[BenchRow]) -> None:
    # 04 §8: 크기(N×N) / 평균 시간(ms) / 연산 횟수(N²) 표 출력
    widths = (10, 16, 14)
    header = (
        _pad("크기(N×N)", widths[0])
        + _pad("평균 시간(ms)", widths[1], right=True)
        + _pad("연산 횟수(N²)", widths[2], right=True)
    )
    print(header)
    print("-" * sum(widths))
    for row in rows:
        print(
            _pad(f"{row.size}×{row.size}", widths[0])
            + _pad(f"{row.ms_2d:.4f}", widths[1], right=True)
            + _pad(str(row.ops), widths[2], right=True)
        )


def print_opt_compare(rows: List[BenchRow]) -> None:
    # 05 §1: 크기 / 2D(ms) / 1D(ms) / 1D÷2D / 결과 일치 비교 표, 필수 표와 별도 출력(09 §0-8)
    # 09 §0-7: 2D·1D 결과가 다르면 경고 출력
    print()
    print("[B1] 최적화 전후 비교(동일 입력, 동일 반복 횟수)")
    widths = (10, 12, 12, 10, 12)
    print(
        _pad("크기", widths[0])
        + _pad("2D(ms)", widths[1], right=True)
        + _pad("1D(ms)", widths[2], right=True)
        + _pad("1D÷2D", widths[3], right=True)
        + _pad("결과 일치", widths[4], right=True)
    )
    print("-" * sum(widths))
    for row in rows:
        ratio = f"{row.ms_1d / row.ms_2d:.2f}" if row.ms_2d > 0 else "-"
        print(
            _pad(f"{row.size}×{row.size}", widths[0])
            + _pad(f"{row.ms_2d:.4f}", widths[1], right=True)
            + _pad(f"{row.ms_1d:.4f}", widths[2], right=True)
            + _pad(ratio, widths[3], right=True)
            + _pad("일치" if row.same_result else "불일치", widths[4], right=True)
        )
    if not all(row.same_result for row in rows):
        print("경고: 2D와 1D의 MAC 결과가 다른 크기가 있습니다(1차원 인덱스 계산 확인 필요).")


def print_summary(results: List[CaseResult]) -> None:
    # 04 §9: 전체 테스트 수·통과 수·실패 수, 실패 케이스 식별자와 사유(요약) 출력
    # 07: 총 테스트 수 = 통과 수 + 실패 수
    total = len(results)
    passed = sum(1 for result in results if result.status == PASS)
    failed = sum(1 for result in results if result.status == FAIL)
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")
    if total != passed + failed:
        print(f"경고: 총 테스트 수({total})와 통과+실패({passed + failed})가 다릅니다.")
    print()
    failures = [result for result in results if result.status == FAIL]
    if not failures:
        print("실패 케이스: 없음")
        return
    print("실패 케이스:")
    for result in failures:
        print(f"- {result.case_id}: [{result.category}] {result.reason}")
