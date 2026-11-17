"""라벨 정규화: 외부 표기를 표준 라벨(Cross, X)로 통일.

담당 요구사항: 04 §4(라벨 정규화)
관련 문서: 03(라벨 정규화 이유), 04 §4·§7, 09 §5 labels.py
"""
from typing import Any, Dict

# 표준 라벨(04 §4)
CROSS = "Cross"
X = "X"

# 동점 판정값(04 §7)
UNDECIDED = "UNDECIDED"

# 별칭표: 외부 표기 → 표준 라벨(09 §5: 이 파일 한 곳에서만 관리)
LABEL_ALIASES: Dict[str, str] = {
    "+": CROSS,
    "cross": CROSS,
    "x": X,
}


class LabelError(ValueError):
    """문자열이 아니거나 별칭표에 없는 라벨."""


def normalize_label(raw: Any) -> str:
    # TODO: 04 §4: '+'·'cross' → Cross, 'x' → X(앞뒤 공백·대소문자 무시), 그 외는 LabelError
    raise NotImplementedError("TODO: normalize_label")
