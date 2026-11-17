"""MAC(Multiply-Accumulate) 연산.

담당 요구사항: 04 §5(MAC 연산), 05 §1(B1 1차원 MAC)
관련 문서: 01(MAC 원리), 04 §5, 05 §1, 07(벡터화 금지), 09 §5 mac.py, 09 §6-1
"""
from typing import List

from .matrix import Matrix


def mac(pattern: Matrix, filt: Matrix) -> float:
    # TODO: 04 §5: 위치별 곱의 합을 float로 반환, 외부 라이브러리 없이 반복문으로 직접 구현(09 §6-1)
    # TODO: 09 §5: 두 행렬 크기가 다르면 ValueError
    raise NotImplementedError("TODO: mac")


def mac_flat(a: List[float], b: List[float]) -> float:
    # TODO: 05 §1: 1차원 리스트 MAC, 같은 입력에서 mac()과 결과 완전 일치(09 §0-7)
    # TODO: 09 §5: 두 리스트 길이가 다르면 ValueError
    raise NotImplementedError("TODO: mac_flat")
