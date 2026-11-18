"""모드별 실행 흐름.

담당 요구사항: 04 §10(실행 흐름), 05 §2(B2 모드 3)
관련 문서: 04 §10, 05 §2, 07(재현성), 08(실행 예시), 09 §0-5·§0-9·§0-11, 09 §5 modes.py, 09 §6-3·§6-4·§6-7, 09 §7
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import console_input, data_loader, generator, report
from .benchmark import run_benchmark
from .config import BENCH_SIZES, MODE1_SIZE, REPEAT
from .judge import FAIL, CaseResult, evaluate, judge
from .labels import CROSS, UNDECIDED, X
from .mac import mac
from .matrix import Matrix


def run_user_mode() -> None:
    # 04 §10: 필터 A, B 입력 → 저장 확인 → 패턴 입력 → MAC 연산 → 결과 판정 → 성능 분석(3×3) 출력
    report.print_section("[1] 필터 입력")
    filter_a = console_input.read_matrix("필터 A", MODE1_SIZE)
    print()
    filter_b = console_input.read_matrix("필터 B", MODE1_SIZE)

    # 저장 확인: 저장된 값을 get()으로 다시 읽어 출력(04 §1)
    print()
    print("저장 확인 - 필터 A")
    report.print_matrix(filter_a)
    print("저장 확인 - 필터 B")
    report.print_matrix(filter_b)

    report.print_section("[2] 패턴 입력")
    pattern = console_input.read_matrix("패턴", MODE1_SIZE)

    run_pair_pipeline(filter_a, filter_b, pattern, ("A", "B"), undecided_text="판정 불가")


def _case_size(case_id: str) -> Optional[int]:
    """검증에 실패한 케이스도 키에서 N을 알 수 있으면 기록한다."""
    try:
        return data_loader.parse_pattern_key(case_id)[0]
    except data_loader.SchemaError:
        return None


def run_json_mode(path: Path) -> None:
    # 04 §10: 필터 로드 → 패턴 로드/검증 → MAC 연산/판정/PASS-FAIL 출력
    #         → 성능 분석(3×3 포함, 5×5/13×13/25×25) → 결과 요약
    # 07: 스키마·크기 불일치가 있어도 중단 없이 케이스 단위 FAIL
    try:
        raw = data_loader.load_json(path)
    except data_loader.DataLoadError as error:
        print()
        print(f"데이터 로드 실패: {error}")
        console_input.wait_enter()
        return

    report.print_section("[1] 필터 로드")
    filters, errors = data_loader.load_filters(raw)
    report.print_filter_status(filters, errors)

    report.print_section("[2] 패턴 분석 (라벨 정규화 적용)")
    patterns = raw.get("patterns")
    if not isinstance(patterns, dict):
        print("patterns 항목이 없거나 객체가 아니어서 분석할 케이스가 없습니다.")
        patterns = {}

    results: List[CaseResult] = []
    bench_pairs: Dict[int, Tuple[Matrix, Matrix]] = {}
    for case_id, entry in patterns.items():
        try:
            n, pattern, pair, expected = data_loader.build_case(case_id, entry, filters, errors)
        except data_loader.SchemaError as error:
            result = CaseResult(
                case_id=case_id, size=_case_size(case_id), cross_score=None, x_score=None,
                verdict=None, expected=None, status=FAIL,
                category=error.category, reason=error.reason,
            )
        else:
            cross_score = mac(pattern, pair[CROSS])
            x_score = mac(pattern, pair[X])
            verdict = judge(cross_score, x_score, CROSS, X)
            status, category, reason = evaluate(verdict, expected)
            result = CaseResult(
                case_id=case_id, size=n, cross_score=cross_score, x_score=x_score,
                verdict=verdict, expected=expected, status=status,
                category=category, reason=reason,
            )
            # 성능 측정용: 크기별 첫 유효 패턴 + Cross 필터(09 §6-7)
            if n not in bench_pairs:
                bench_pairs[n] = (pattern, pair[CROSS])
        results.append(result)
        report.print_case(result)

    report.print_section(f"[3] 성능 분석 (평균/{REPEAT}회)")
    pairs: Dict[int, Tuple[Matrix, Matrix]] = {}
    generated: List[int] = []
    for n in BENCH_SIZES:
        if n in bench_pairs:
            pairs[n] = bench_pairs[n]
        else:
            # 3×3은 data.json에 없으므로, 데이터가 무효한 크기도 생성 패턴으로 측정한다
            pairs[n] = (generator.make_cross(n), generator.make_cross(n))
            generated.append(n)
    rows = run_benchmark(pairs)
    report.print_perf_table(rows)
    if generated:
        sizes = ", ".join(f"{n}×{n}" for n in generated)
        print(f"※ 생성 패턴으로 측정한 크기: {sizes}")
    report.print_opt_compare(rows)

    report.print_section("[4] 결과 요약")
    report.print_summary(results)


def run_generator_mode() -> None:
    # 05 §2: 크기 N 입력 → Cross/X 필터·패턴 생성 → 모드 1 처리 파이프라인 재사용(09 §0-5)
    # 09 §0-9: 선택한 패턴 종류를 expected로 PASS/FAIL 표시
    report.print_section("[1] 크기 입력")
    n = console_input.read_gen_size()
    filter_a = generator.make_cross(n)
    filter_b = generator.make_x(n)
    print()
    print(f"저장 확인 - 필터 A ({CROSS})")
    report.print_matrix(filter_a)
    print(f"저장 확인 - 필터 B ({X})")
    report.print_matrix(filter_b)

    report.print_section("[2] 패턴 선택")
    kind = console_input.read_pattern_kind()
    pattern = generator.make_cross(n) if kind == CROSS else generator.make_x(n)
    print(f"{kind} 패턴 생성 완료 ({n}×{n})")

    run_pair_pipeline(filter_a, filter_b, pattern, (CROSS, X), expected=kind)


def run_pair_pipeline(
    filter_a: Matrix,
    filter_b: Matrix,
    pattern: Matrix,
    labels: Tuple[str, str],
    expected: Optional[str] = None,
    undecided_text: str = UNDECIDED,
) -> None:
    # 09 §5: 모드 1·3 공용, MAC → 판정 → (expected가 있으면 PASS/FAIL) → 성능 표 → B1 비교 표
    # 09 §0-11: undecided_text는 동점 표시 문구(모드 1은 "판정 불가")
    report.print_section("[3] MAC 결과")
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    verdict = judge(score_a, score_b, labels[0], labels[1])
    status = None
    if expected is not None:
        status, _, _ = evaluate(verdict, expected)
    report.print_pair_result(
        score_a, score_b, verdict, labels,
        undecided_text=undecided_text, expected=expected, status=status,
    )

    report.print_section(f"[4] 성능 분석 (평균/{REPEAT}회)")
    rows = run_benchmark({pattern.size: (pattern, filter_a)})
    report.print_perf_table(rows)
    report.print_opt_compare(rows)
