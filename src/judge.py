"""동점 판단, 판정, PASS/FAIL 평가, 케이스 결과 레코드.

담당 요구사항: 04 §6(점수 비교 정책), 04 §7(판정 및 PASS/FAIL)
관련 문서: 03(epsilon 필요성), 04 §6·§7, 08(출력 예시), 09 §5 judge.py(실패 분류 표), 09 §6-2·§6-3
"""
from dataclasses import dataclass
from typing import Optional, Tuple

from .config import EPSILON
from .labels import UNDECIDED

# 평가 상태
PASS = "PASS"
FAIL = "FAIL"

# 실패 분류(09 §5 실패 분류 표). 주석은 03의 3분류
CATEGORY_SCHEMA = "스키마"    # 데이터/스키마
CATEGORY_SIZE = "크기"        # 데이터/스키마
CATEGORY_LABEL = "라벨"       # 데이터/스키마
CATEGORY_TIE = "동점"         # 수치 비교
CATEGORY_MISMATCH = "불일치"  # 로직 또는 라벨 데이터


def is_tie(a: float, b: float, eps: float = EPSILON) -> bool:
    # 04 §6: abs(a - b) < 1e-9이면 동점(math.isclose 미사용, 09 §6-2)
    return abs(a - b) < eps


def judge(a: float, b: float, label_a: str, label_b: str, eps: float = EPSILON) -> str:
    # 04 §7: 동점이면 UNDECIDED, 아니면 점수가 큰 쪽 라벨(모드 1·2·3 공용, 09 §6-3)
    # 동점 검사를 대소 비교보다 먼저 해야 미세한 오차가 승패를 정하지 않는다
    if is_tie(a, b, eps):
        return UNDECIDED
    return label_a if a > b else label_b


def evaluate(verdict: str, expected: str) -> Tuple[str, Optional[str], Optional[str]]:
    # 04 §7: 판정이 expected와 같으면 PASS, 다르면 FAIL
    # 09 §5: (상태, 분류, 사유) 반환
    if verdict == expected:
        return PASS, None, None
    if verdict == UNDECIDED:
        return FAIL, CATEGORY_TIE, "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
    return FAIL, CATEGORY_MISMATCH, f"판정 {verdict}이(가) expected {expected}와 다름"


@dataclass
class CaseResult:
    """모드 2 케이스 1건의 결과(04 §7·§9, 09 §5)."""

    case_id: str                  # 패턴 키
    size: Optional[int]           # 키에서 추출한 N
    cross_score: Optional[float]  # Cross 필터 점수
    x_score: Optional[float]      # X 필터 점수
    verdict: Optional[str]        # Cross / X / UNDECIDED
    expected: Optional[str]       # 정규화된 expected
    status: str                   # PASS / FAIL
    category: Optional[str]       # 실패 분류(09 §5 실패 분류 표)
    reason: Optional[str]         # 실패 사유
