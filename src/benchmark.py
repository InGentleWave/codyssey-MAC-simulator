"""MAC 연산 시간 측정.

담당 요구사항: 04 §8(성능 분석), 05 §1(B1 최적화 전후 비교)
관련 문서: 03(O(N²) 설명), 04 §8, 05 §1, 09 §0-7, 09 §5 benchmark.py, 09 §6-6·§6-7
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple

from .config import REPEAT
from .matrix import Matrix


@dataclass
class BenchRow:
    """크기 1개의 측정 결과(성능 표 1행, 09 §5)."""

    size: int          # N
    ops: int           # 연산 횟수 N²
    ms_2d: float       # 2D MAC 평균 시간(ms)
    ms_1d: float       # 1D MAC 평균 시간(ms, B1)
    same_result: bool  # 2D·1D 결과 일치 여부(B1)


def measure_mac_ms(pattern: Matrix, filt: Matrix, repeat: int = REPEAT) -> float:
    # TODO: 04 §8: MAC 1회 평균 시간(ms), 10회 이상 반복 측정, I/O 제외(09 §6-6)
    raise NotImplementedError("TODO: measure_mac_ms")


def measure_mac_flat_ms(a: List[float], b: List[float], repeat: int = REPEAT) -> float:
    # TODO: 05 §1: 1D MAC 평균 시간(ms), measure_mac_ms와 같은 반복 횟수·측정 조건
    raise NotImplementedError("TODO: measure_mac_flat_ms")


def run_benchmark(pairs: Dict[int, Tuple[Matrix, Matrix]]) -> List[BenchRow]:
    # TODO: 04 §8: 크기별 평균 시간(ms)과 연산 횟수(N²)
    # TODO: 05 §1: 같은 입력·같은 반복 횟수로 2D·1D 비교, 1차원 변환은 측정 구간 밖, 결과 일치 여부 기록(09 §0-7)
    raise NotImplementedError("TODO: run_benchmark")
