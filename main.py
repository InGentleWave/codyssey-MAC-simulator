"""Mini NPU Simulator 진입점.

담당 요구사항: 04 §10(실행 흐름: 입력 방식 선택)
관련 문서: 04 §10, 07(제출물 main.py), 09 §5 main.py, 09 §6-9, 09 §7 공통
실행: python main.py [데이터 파일 경로]
"""
import os
import sys
import traceback
from pathlib import Path

from src.config import DATA_FILENAME
from src.console_input import read_mode, wait_enter
from src.modes import run_generator_mode, run_json_mode, run_user_mode
from src.report import print_banner


def main() -> None:
    # 09 §5: 데이터 경로는 실행 인자 우선, 없으면 main.py 위치 기준 data.json(실행 위치와 무관, 09 §6-9)
    # Python 3.8에서는 __file__이 상대 경로일 수 있어 os.path.abspath로 절대 경로를 만든다
    if len(sys.argv) > 1:
        data_path = Path(os.path.abspath(sys.argv[1]))
    else:
        data_path = Path(os.path.abspath(__file__)).parent / DATA_FILENAME

    # 04 §10: 실행 시 입력 방식 선택 후 해당 모드 실행
    print_banner()
    mode = read_mode()
    if mode == "1":
        run_user_mode()
    elif mode == "2":
        run_json_mode(data_path)
    else:
        run_generator_mode()


if __name__ == "__main__":
    # 09 §5: EOFError·KeyboardInterrupt는 종료 안내 후 즉시 종료
    # 09 §5: 그 외 예외는 종류·메시지·traceback 출력, 엔터 입력 후 종료 코드 1로 종료
    # EOFError는 Exception의 하위 클래스이므로 Exception보다 먼저 처리한다
    try:
        main()
    except EOFError:
        print("\n입력이 끝나 프로그램을 종료합니다.")
    except KeyboardInterrupt:
        print("\n사용자가 중단해 프로그램을 종료합니다.")
    except Exception as error:
        print(f"\n예상치 못한 오류: {type(error).__name__}: {error}")
        traceback.print_exc()
        wait_enter()
        sys.exit(1)
