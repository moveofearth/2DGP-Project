import pathlib

global windowWidth
global windowHeight

windowWidth = 1920
windowHeight = 1080

# 물리 상수
GRAVITY = 9.8 * 100  # 중력 가속도 (픽셀/초²) - 화면 크기에 맞게 조정
GROUND_Y = 300 * 1.5  # 그라운드 Y 좌표 (450픽셀) - 1.5배 스케일링 적용

# 캐릭터별 이동속도 (픽셀/초)
# priest: 250.0 픽셀/초
# thief: 290.0 픽셀/초
# fighter: 290.0 픽셀/초

# 동작별 스프라이트 프레임/초 (fps)
# 기본 동작 (Idle, Walk, BackWalk): 12 fps (0.083초 간격)
# Fast 공격: 프레임 간격 0.08초 (FAST_FRAME_TIME)
# Strong 공격: 프레임 간격 0.13초 (STRONG_FRAME_TIME)
#
# 동작별 상세 프레임 수:
# priest:
#   - Idle: 4프레임, Walk: 8프레임, BackWalk: 8프레임
#   - fastMiddleATK: 6프레임, strongMiddleATK: 6+8프레임 (연계시)
#   - strongUpperATK: 12프레임, strongLowerATK: 9프레임
#   - rageSkill: 18프레임
#   - guard: 2프레임 (0.45초 + 0.45초 = 0.9초 총 재생시간)
# thief:
#   - Idle: 6프레임, Walk: 6프레임, BackWalk: 7프레임
#   - fastMiddleATK: 6+6+6프레임 (3단 연계), strongMiddleATK: 5+5프레임 (연계시)
#   - strongUpperATK: 5+5프레임 (연계시), strongLowerATK: 4프레임
#   - guard: 2프레임 (thief도 동일한 가드 시스템)
# fighter:
#   - Idle: 4프레임, Walk: 8프레임, BackWalk: 5프레임
#   - fastMiddleATK: 4+3+3프레임 (3단 연계), fastLowerATK: 4프레임, fastUpperATK: 6프레임
#   - strongMiddleATK: 5프레임, strongUpperATK: 4+4프레임 (연계시), strongLowerATK: 5프레임
#   - guard: 2프레임 (fighter도 동일한 가드 시스템)

# 프레임 간격 상수 (초)
FAST_FRAME_TIME = 0.08  # 0.8초 -> 0.08초로 수정
STRONG_FRAME_TIME = 0.13  # 0.13초 유지
