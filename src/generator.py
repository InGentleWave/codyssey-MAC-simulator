"""Cross/X 패턴 생성기.

담당 요구사항: 05 §2(B2 패턴 생성기), 04 §10(모드 2 성능 분석의 3×3 데이터)
관련 문서: 05 §2, 09 §0-5·§0-6, 09 §3, 09 §5 generator.py, 09 §6-7
"""
from .matrix import Matrix


def _check_size(n: int) -> None:
    # 09 §0-6: 홀수만 허용(짝수는 중심선이 한 줄로 정해지지 않음), 3 이상
    if isinstance(n, bool) or not isinstance(n, int) or n < 3 or n % 2 == 0:
        raise ValueError(f"패턴 크기는 3 이상의 홀수여야 함({n!r})")


def make_cross(n: int) -> Matrix:
    # 05 §2: 가운데 행과 열이 1.0인 n×n 십자가 패턴
    _check_size(n)
    matrix = Matrix(n)
    center = n // 2
    for i in range(n):
        matrix.set(center, i, 1.0)
        matrix.set(i, center, 1.0)
    return matrix


def make_x(n: int) -> Matrix:
    # 05 §2: 두 대각선이 1.0인 n×n X 패턴
    _check_size(n)
    matrix = Matrix(n)
    for i in range(n):
        matrix.set(i, i, 1.0)
        matrix.set(i, n - 1 - i, 1.0)
    return matrix
