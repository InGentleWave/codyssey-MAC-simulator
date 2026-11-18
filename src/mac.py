"""MAC(Multiply-Accumulate) 연산.

담당 요구사항: 04 §5(MAC 연산), 05 §1(B1 1차원 MAC)
관련 문서: 01(MAC 원리), 04 §5, 05 §1, 07(벡터화 금지), 09 §5 mac.py, 09 §6-1
"""
from typing import List

from .matrix import Matrix


def mac(pattern: Matrix, filt: Matrix) -> float:
    # 04 §5: 위치별 곱의 합을 float로 반환, 반복문으로 직접 구현(09 §6-1)
    if pattern.size != filt.size:
        raise ValueError(
            f"크기 불일치: 패턴 {pattern.size}×{pattern.size}, 필터 {filt.size}×{filt.size}"
        )
    n = pattern.size
    total = 0.0  # 0.0에서 시작해 정수 입력이어도 결과는 float
    # 누적 순서는 행 우선으로 고정한다(B1의 mac_flat과 결과가 같아야 함)
    for i in range(n):
        for j in range(n):
            total += pattern.get(i, j) * filt.get(i, j)
    return total


def mac_flat(a: List[float], b: List[float]) -> float:
    # 05 §1: 1차원 리스트 MAC, 같은 입력에서 mac()과 결과 완전 일치(09 §0-7)
    if len(a) != len(b):
        raise ValueError(f"길이 불일치: {len(a)}, {len(b)}")
    total = 0.0
    for k in range(len(a)):
        total += a[k] * b[k]
    return total
