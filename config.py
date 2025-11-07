import pathlib

global windowWidth
global windowHeight

windowWidth = 1280
windowHeight = 720

# 캐릭터별 이동속도 (픽셀/초)
# priest: 200.0 픽셀/초
# thief: 270.0 픽셀/초
# fighter: 270.0 픽셀/초

# 동작별 스프라이트 프레임/초 (fps)
# 기본 동작 (Idle, Walk, BackWalk): 12 fps (0.083초 간격)
# Fast 공격 (fastMiddleATK, fastLowerATK, fastUpperATK): 10 fps (0.1초 간격)
# Strong 공격 (strongMiddleATK, strongUpperATK, strongLowerATK): 6.67 fps (0.15초 간격)
# Rage 스킬 (rageSkill): 18 fps (0.056초 간격) - 1초 동안 18프레임 재생
#
# 동작별 상세 프레임 수:
# priest:
#   - Idle: 4프레임, Walk: 8프레임, BackWalk: 8프레임
#   - fastMiddleATK: 6프레임, strongMiddleATK: 6+8프레임 (연계시)
#   - strongUpperATK: 12프레임, strongLowerATK: 9프레임
#   - rageSkill: 18프레임
# thief:
#   - Idle: 6프레임, Walk: 6프레임, BackWalk: 7프레임
#   - fastMiddleATK: 6+6+6프레임 (3단 연계), strongMiddleATK: 5+5프레임 (연계시)
#   - strongUpperATK: 5+5프레임 (연계시), strongLowerATK: 4프레임
# fighter:
#   - Idle: 4프레임, Walk: 8프레임, BackWalk: 5프레임
#   - fastMiddleATK: 4+3+3프레임 (3단 연계), fastLowerATK: 4프레임, fastUpperATK: 6프레임
#   - strongMiddleATK: 5프레임, strongUpperATK: 4+4프레임 (연계시), strongLowerATK: 5프레임
