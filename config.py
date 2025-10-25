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

