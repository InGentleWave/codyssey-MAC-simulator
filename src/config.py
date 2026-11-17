"""프로그램 전역 상수.

담당 요구사항: 04 §6(EPSILON), 04 §8(REPEAT, BENCH_SIZES), 04 §2(MODE1_SIZE), 05 §2(GEN_MIN_SIZE, GEN_MAX_SIZE), 04 §3(DATA_FILENAME)
관련 문서: 04 §2·§3·§6·§8·§10, 05 §2, 09 §0-6, 09 §5 config.py, 09 §6-7·§6-9
"""

# 04 §6: 점수 비교 허용오차, abs(a - b) < 1e-9이면 동점
EPSILON = 1e-9

# 04 §8: 크기별 MAC 연산 반복 측정 횟수(최소 10회)
REPEAT = 10

# 04 §2: 모드 1 입력 크기(3×3)
MODE1_SIZE = 3

# 04 §8·§10: 성능 분석 대상 크기(3×3 포함, 5×5/13×13/25×25)
BENCH_SIZES = (3, 5, 13, 25)

# 05 §2, 09 §0-6: 모드 3(패턴 생성기) 입력 범위, 홀수 N만 허용
GEN_MIN_SIZE = 3
GEN_MAX_SIZE = 25

# 04 §3: 기본 데이터 파일 이름(main.py와 같은 폴더, 09 §6-9)
DATA_FILENAME = "data.json"
