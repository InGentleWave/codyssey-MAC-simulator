"""Mini NPU Simulator 진입점.

담당 요구사항: 04 §10(실행 흐름: 입력 방식 선택)
관련 문서: 04 §10, 07(제출물 main.py), 09 §5 main.py, 09 §6-9, 09 §7 공통
"""
from pathlib import Path

from src.console_input import read_mode
from src.modes import run_user_mode, run_json_mode, run_generator_mode

def main() -> None:
    # 04 §10: 실행 시 입력 방식 선택(사용자 입력 3×3 / data.json 분석 / 패턴 생성기(09 §0-5)) 후 해당 모드 실행
    while True:
        mode = read_mode()
        if mode == "1":
            # 실행 모드 1
            run_user_mode()
        elif mode == "2":
            # 실행 모드 2
            run_json_mode(Path("data.json"))
        elif mode == "3":
            # 실행 모드 3
            run_generator_mode()
    # 09 §5: 데이터 경로는 실행 인자 우선, 없으면 main.py 위치 기준 data.json(실행 위치와 무관, 09 §6-9)

if __name__ == "__main__":
    # 09 §5: EOFError·KeyboardInterrupt는 종료 안내 후 즉시 종료
    # 09 §5: 그 외 예외는 종류·메시지·traceback 출력, 엔터 입력 후 종료 코드 1로 종료
    try:
        main()
    
    except (NotImplementedError) as e:
        print(f"\n{e}")
        input("\n엔터를 눌러 종료합니다.")
        exit(1)
    except (EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")
    except (KeyboardInterrupt):
        print("\n사용자에 의해 프로그램이 종료되었습니다.")
    except Exception as e:
        import traceback

        print(f"\n예외 발생: {type(e).__name__}: {e}")
        traceback.print_exc()
        input("\n엔터를 눌러 종료합니다.")
        exit(1)
