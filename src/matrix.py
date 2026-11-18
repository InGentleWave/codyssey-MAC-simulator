"""n×n 행렬 데이터 구조.

담당 요구사항: 04 §1(데이터 구조), 05 §1(B1 1차원 변환)
관련 문서: 04 §1·§2·§3, 05 §1, 09 §5 matrix.py, 09 §6-5
"""
import math
from typing import List, Optional, Sequence


class MatrixFormatError(ValueError):
    """행렬 형태·값 검증 실패(사유를 메시지로 가짐)."""


def _to_valid_float(value: object, where: str) -> float:
    """숫자(bool 제외)이면서 유한값이면 float로 바꿔 반환한다(09 §6-5)."""
    # bool은 int의 하위 타입이라 isinstance(True, int)가 참이므로 먼저 걸러낸다
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise MatrixFormatError(f"{where}: 숫자가 아님({value!r})")
    if not math.isfinite(value):
        raise MatrixFormatError(f"{where}: 유한한 숫자가 아님({value!r})")
    return float(value)


class Matrix:
    """패턴과 필터를 저장하는 n×n 행렬."""

    size: int  # 한 변의 길이 n

    def __init__(self, n: int) -> None:
        # 04 §1: n×n 행렬 저장, 0.0으로 초기화(n ≥ 1)
        if isinstance(n, bool) or not isinstance(n, int) or n < 1:
            raise MatrixFormatError(f"행렬 크기는 1 이상의 정수여야 함({n!r})")
        self.size = n
        # 행마다 별도 리스트를 만든다([[0.0] * n] * n은 모든 행이 같은 리스트를 공유함)
        self._data = [[0.0] * n for _ in range(n)]

    def _check_index(self, r: int, c: int) -> None:
        # 파이썬 리스트는 음수 인덱스를 뒤에서부터 읽으므로 범위를 직접 검사한다
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise IndexError(f"위치 ({r}, {c})가 범위(0~{self.size - 1})를 벗어남")

    def get(self, r: int, c: int) -> float:
        # 04 §1: 특정 위치의 값 읽기
        self._check_index(r, c)
        return self._data[r][c]

    def set(self, r: int, c: int, v: float) -> None:
        # 04 §1: 특정 위치에 값 저장(숫자·유한값만 허용)
        self._check_index(r, c)
        self._data[r][c] = _to_valid_float(v, f"({r}, {c}) 위치")

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[float]], n: Optional[int] = None) -> "Matrix":
        # 04 §2·§3: 2차원 리스트를 검증해 Matrix로 만든다(모드 1 입력, data.json 공용)
        if not isinstance(rows, (list, tuple)):
            raise MatrixFormatError("행렬이 리스트가 아님")
        size = len(rows)
        if size == 0:
            raise MatrixFormatError("행이 하나도 없음")
        if n is not None and size != n:
            raise MatrixFormatError(f"행 수 {size}개(필요 {n}개)")
        for i, row in enumerate(rows, start=1):
            if not isinstance(row, (list, tuple)):
                raise MatrixFormatError(f"{i}번째 행이 리스트가 아님")
            if len(row) != size:
                raise MatrixFormatError(f"{i}번째 행의 열 수 {len(row)}개(필요 {size}개)")
        matrix = cls(size)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                matrix.set(i, j, value)
        return matrix

    def to_flat(self) -> List[float]:
        # 05 §1: 행 우선 1차원 리스트(길이 n², (i, j) 위치 → 인덱스 i×n + j)
        flat: List[float] = []
        for row in self._data:
            flat.extend(row)
        return flat
