"""Cross/X 패턴 생성기.

담당 요구사항: 05 §2(B2 패턴 생성기), 04 §10(모드 2 성능 분석의 3×3 데이터)
관련 문서: 05 §2, 09 §0-5·§0-6, 09 §3, 09 §5 generator.py, 09 §6-7
"""
from .matrix import Matrix


def make_cross(n: int) -> Matrix:
    # TODO: 05 §2: 가운데 행과 열이 1.0인 n×n 십자가 패턴
    # TODO: 09 §0-6: n이 짝수이거나 3 미만이면 ValueError
    raise NotImplementedError("TODO: make_cross")


def make_x(n: int) -> Matrix:
    # TODO: 05 §2: 두 대각선이 1.0인 n×n X 패턴
    # TODO: 09 §0-6: n이 짝수이거나 3 미만이면 ValueError
    raise NotImplementedError("TODO: make_x")
