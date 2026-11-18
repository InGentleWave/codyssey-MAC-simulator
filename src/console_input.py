"""콘솔 입력: 모드 선택, 행렬 입력, 패턴 생성기 입력.

담당 요구사항: 04 §2(모드 1 입력 처리), 04 §10(입력 방식 선택), 05 §2(B2 입력)
관련 문서: 04 §2·§10, 05 §2, 07(입력 검증·재입력), 08(입력 화면 예시), 09 §0-1·§0-5·§0-6, 09 §5 console_input.py
EOFError·KeyboardInterrupt는 이 모듈에서 잡지 않고 main으로 전달한다(09 §5).
단, 종료 직전 대기용 wait_enter()는 예외를 삼킨다.
"""
import math
from typing import List

from .config import GEN_MAX_SIZE, GEN_MIN_SIZE
from .labels import CROSS, X
from .matrix import Matrix


def read_mode() -> str:
    # 04 §10: 입력 방식 선택("1" 사용자 입력 3×3, "2" data.json 분석, "3" 패턴 생성기(09 §0-5))
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("3. 패턴 생성기 (N×N)")
    while True:
        choice = input("선택: ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print("1, 2, 3 중 하나를 입력하세요.")


def parse_row(line: str, n: int) -> List[float]:
    # 04 §2: 공백 구분 숫자 n개를 float로 반환, 열 수 불일치·숫자 파싱 실패·NaN/Infinity는 오류(09 §6-5)
    tokens = line.split()
    if len(tokens) != n:
        raise ValueError(f"숫자 {len(tokens)}개 입력됨(필요 {n}개)")
    values: List[float] = []
    for token in tokens:
        try:
            value = float(token)
        except ValueError:
            raise ValueError(f"'{token}'은(는) 숫자가 아님") from None
        # float()는 'nan', 'inf' 같은 문자열도 변환하므로 따로 거른다
        if not math.isfinite(value):
            raise ValueError(f"'{token}'은(는) 유한한 숫자가 아님")
        values.append(value)
    return values


def read_matrix(title: str, n: int) -> Matrix:
    # 04 §2: n줄을 한 줄씩 공백 구분으로 입력받아 저장, 오류 시 안내 문구 출력 후 재입력
    # 09 §0-1: n줄을 모두 받은 뒤 검증하고, 오류가 있으면 행렬 n줄 전체를 다시 입력받는다
    #          (여러 줄을 붙여넣었을 때 남은 줄이 다음 입력으로 밀리지 않게 하기 위함)
    while True:
        print(f"{title} ({n}줄 입력, 공백 구분)")
        lines = [input() for _ in range(n)]
        rows: List[List[float]] = []
        problems: List[str] = []
        for number, line in enumerate(lines, start=1):
            try:
                rows.append(parse_row(line, n))
            except ValueError as error:
                problems.append(f"  - {number}번째 줄: {error}")
        if not problems:
            return Matrix.from_rows(rows, n)
        print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
        for problem in problems:
            print(problem)
        print(f"{title}의 {n}줄 전체를 다시 입력하세요.")
        print()


def read_gen_size() -> int:
    # 05 §2: 생성할 크기 N 입력, 홀수이며 GEN_MIN_SIZE~GEN_MAX_SIZE만 허용(09 §0-6)
    while True:
        text = input(f"크기 N 입력(홀수, {GEN_MIN_SIZE}~{GEN_MAX_SIZE}): ").strip()
        try:
            n = int(text)
        except ValueError:
            print("정수를 입력하세요.")
            continue
        if not GEN_MIN_SIZE <= n <= GEN_MAX_SIZE:
            print(f"{GEN_MIN_SIZE} 이상 {GEN_MAX_SIZE} 이하로 입력하세요.")
            continue
        if n % 2 == 0:
            print("홀수만 입력할 수 있습니다(짝수는 중심선이 한 줄로 정해지지 않음).")
            continue
        return n


def read_pattern_kind() -> str:
    # 05 §2: 생성할 패턴 종류 선택, Cross 또는 X 반환
    print("패턴 종류: 1. Cross / 2. X")
    while True:
        choice = input("선택: ").strip()
        if choice == "1":
            return CROSS
        if choice == "2":
            return X
        print("1 또는 2를 입력하세요.")


def wait_enter(message: str = "엔터를 누르면 종료합니다.") -> None:
    """오류 안내 후 종료 전에 엔터 입력을 기다린다(대기 중 EOF·Ctrl+C는 무시)."""
    try:
        input(message)
    except (EOFError, KeyboardInterrupt):
        print()
