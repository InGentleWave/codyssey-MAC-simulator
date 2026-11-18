"""MAC 연산 시간 측정.

담당 요구사항: 04 §8(성능 분석), 05 §1(B1 최적화 전후 비교)
관련 문서: 03(O(N²) 설명), 04 §8, 05 §1, 09 §0-7, 09 §5 benchmark.py, 09 §6-6·§6-7
"""
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

from .config import REPEAT
from .mac import mac, mac_flat
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
    # 04 §8: MAC 1회 평균 시간(ms), 10회 이상 반복 측정, I/O 제외(09 §6-6)
    # 반복 전체를 한 구간으로 재고 반복 횟수로 나눈다
    if repeat < 1:
        raise ValueError("repeat는 1 이상이어야 함")
    start = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filt)
    elapsed = time.perf_counter() - start
    return elapsed / repeat * 1000.0


def measure_mac_flat_ms(a: List[float], b: List[float], repeat: int = REPEAT) -> float:
    # 05 §1: 1D MAC 평균 시간(ms), measure_mac_ms와 같은 반복 횟수·측정 조건
    if repeat < 1:
        raise ValueError("repeat는 1 이상이어야 함")
    start = time.perf_counter()
    for _ in range(repeat):
        mac_flat(a, b)
    elapsed = time.perf_counter() - start
    return elapsed / repeat * 1000.0


def run_benchmark(pairs: Dict[int, Tuple[Matrix, Matrix]]) -> List[BenchRow]:
    # 04 §8: 크기별 평균 시간(ms)과 연산 횟수(N²)
    # 05 §1: 같은 입력·같은 반복 횟수로 2D·1D 비교, 1차원 변환은 측정 구간 밖(09 §0-7)
    rows: List[BenchRow] = []
    for n in sorted(pairs):
        pattern, filt = pairs[n]
        ms_2d = measure_mac_ms(pattern, filt)
        flat_pattern = pattern.to_flat()
        flat_filter = filt.to_flat()
        ms_1d = measure_mac_flat_ms(flat_pattern, flat_filter)
        # 누적 순서가 같으므로 두 결과는 완전히 같아야 한다(다르면 인덱스 계산 오류)
        same = mac(pattern, filt) == mac_flat(flat_pattern, flat_filter)
        rows.append(BenchRow(size=n, ops=n * n, ms_2d=ms_2d, ms_1d=ms_1d, same_result=same))
    return rows
