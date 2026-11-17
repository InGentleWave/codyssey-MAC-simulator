"""n×n 행렬 데이터 구조.

담당 요구사항: 04 §1(데이터 구조), 05 §1(B1 1차원 변환)
관련 문서: 04 §1·§2·§3, 05 §1, 09 §5 matrix.py, 09 §6-5
"""
from typing import List, Optional, Sequence


class MatrixFormatError(ValueError):
    """행렬 형태·값 검증 실패(사유를 메시지로 가짐)."""


class Matrix:
    """패턴과 필터를 저장하는 n×n 행렬."""

    size: int  # 한 변의 길이 n

    def __init__(self, n: int) -> None:
        # TODO: 04 §1: n×n 행렬 저장, 0.0으로 초기화(n ≥ 1), 3×3·5×5·13×13·25×25 처리
        raise NotImplementedError("TODO: Matrix.__init__")

    def get(self, r: int, c: int) -> float:
        # TODO: 04 §1: 특정 위치의 값 읽기, 0 ≤ r, c < n 범위 밖(음수 포함)은 거부
        raise NotImplementedError("TODO: Matrix.get")

    def set(self, r: int, c: int, v: float) -> None:
        # TODO: 04 §1: 특정 위치에 값 저장, 범위 밖은 거부, 숫자(bool 제외)·유한값만 허용(09 §6-5)
        raise NotImplementedError("TODO: Matrix.set")

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[float]], n: Optional[int] = None) -> "Matrix":
        # TODO: 04 §2·§3: 정사각형이 아니거나 n과 크기가 다르거나 숫자가 아니면 MatrixFormatError(사유)
        raise NotImplementedError("TODO: Matrix.from_rows")

    def to_flat(self) -> List[float]:
        # TODO: 05 §1: 길이 N²의 행 우선 1차원 리스트 반환(인덱스 i×n + j)
        raise NotImplementedError("TODO: Matrix.to_flat")
