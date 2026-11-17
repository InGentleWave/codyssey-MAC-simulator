"""동점 판단, 판정, PASS/FAIL 평가, 케이스 결과 레코드.

담당 요구사항: 04 §6(점수 비교 정책), 04 §7(판정 및 PASS/FAIL)
관련 문서: 03(epsilon 필요성), 04 §6·§7, 08(출력 예시), 09 §5 judge.py(실패 분류 표), 09 §6-2·§6-3
"""
from dataclasses import dataclass
from typing import Optional, Tuple

from .config import EPSILON


def is_tie(a: float, b: float, eps: float = EPSILON) -> bool:
    # TODO: 04 §6: abs(a - b) < 1e-9이면 동점(math.isclose 미사용, 09 §6-2)
    raise NotImplementedError("TODO: is_tie")


def judge(a: float, b: float, label_a: str, label_b: str, eps: float = EPSILON) -> str:
    # TODO: 04 §7: 동점이면 UNDECIDED, 아니면 점수가 큰 쪽 라벨(모드 1·2·3 공용, 09 §6-3)
    raise NotImplementedError("TODO: judge")


def evaluate(verdict: str, expected: str) -> Tuple[str, Optional[str], Optional[str]]:
    # TODO: 04 §7: 판정이 expected와 같으면 PASS, 다르면 FAIL
    # TODO: 09 §5: (상태, 분류, 사유) 반환, FAIL 분류는 동점(UNDECIDED) 또는 불일치
    raise NotImplementedError("TODO: evaluate")


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
