"""콘솔 입력: 모드 선택, 행렬 입력, 패턴 생성기 입력.

담당 요구사항: 04 §2(모드 1 입력 처리), 04 §10(입력 방식 선택), 05 §2(B2 입력)
관련 문서: 04 §2·§10, 05 §2, 07(입력 검증·재입력), 08(입력 화면 예시), 09 §0-1·§0-5·§0-6, 09 §5 console_input.py
EOFError·KeyboardInterrupt는 이 모듈에서 잡지 않고 main으로 전달한다(09 §5).
"""
from typing import List

from .matrix import Matrix


def read_mode() -> str:
    # TODO: 04 §10: 입력 방식 선택("1" 사용자 입력 3×3, "2" data.json 분석, "3" 패턴 생성기(09 §0-5)), 그 외 입력은 재입력
    raise NotImplementedError("TODO: read_mode")


def parse_row(line: str, n: int) -> List[float]:
    # TODO: 04 §2: 공백 구분 숫자 n개를 float로 반환, 열 수 불일치·숫자 파싱 실패·NaN/Infinity는 오류(09 §6-5)
    raise NotImplementedError("TODO: parse_row")


def read_matrix(title: str, n: int) -> Matrix:
    # TODO: 04 §2: n줄을 한 줄씩 공백 구분으로 입력받아 저장, 행·열 수 불일치·파싱 실패 시 안내 문구 출력 후 재입력
    # TODO: 09 §0-1: 오류 시 해당 행렬 n줄 전체 재입력
    raise NotImplementedError("TODO: read_matrix")


def read_gen_size() -> int:
    # TODO: 05 §2: 생성할 크기 N 입력, 홀수이며 GEN_MIN_SIZE~GEN_MAX_SIZE만 허용, 그 외 재입력(09 §0-6)
    raise NotImplementedError("TODO: read_gen_size")


def read_pattern_kind() -> str:
    # TODO: 05 §2: 생성할 패턴 종류 선택, Cross 또는 X 반환
    raise NotImplementedError("TODO: read_pattern_kind")
