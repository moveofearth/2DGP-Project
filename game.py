import pico2d
import config
import time

from Scenes.sceneManager import SceneManager
from Player.player import Player
from ioManager import IOManager
from spriteManager import SpriteManager
from handle_collision import CollisionHandler


class Game:

    def __init__(self):
        self.running = True
        self.sceneManager = SceneManager()
        self.playerLeft = Player('left')
        self.playerRight = Player('right')
        self.ioManager = IOManager()
        self.spriteManager = SpriteManager()
        self.last_time = 0
        self.target_fps = 60  # 60fps로 조정
        self.frame_time = 1.0 / self.target_fps
        self.game_over = False
        self.max_delta_time = 1.0 / 30.0  # 최대 deltaTime 제한 (30fps 이하로 떨어지지 않도록)
        self.round_end_timer = 0.0  # 라운드 종료 타이머 추가

    def initialize(self):
        pico2d.open_canvas(config.windowWidth, config.windowHeight)
        self.sceneManager.initialize()
        self.playerLeft.initialize()
        self.playerRight.initialize()
        # 초기 스폰 시 플레이어가 겹치지 않도록 보정
        CollisionHandler.prevent_overlap_on_spawn(self.playerLeft, self.playerRight)
        self.spriteManager.load_sprites()
        self.spriteManager.set_player_references(self.playerLeft, self.playerRight)
        self.last_time = time.time()

    def check_collision(self):
        """플레이어 간 충돌 및 공격 판정 - 공격 범위 기반"""
        # Player1이 공격 중이고 타격 처리 가능한 상태인지 확인
        if (self.playerLeft.is_attacking and
            hasattr(self.playerLeft, 'can_process_hit') and
            self.playerLeft.can_process_hit and
            self.playerLeft.can_hit_target()):

            # PlayerRight가 down 상태일 때 Lower 계열 공격은 히트 가능하도록 허용
            attacker_state = (self.playerLeft.state or '').lower()
            target = self.playerRight
            # 대상의 현재 hit_type 확인 (down 또는 airborne일 때 특별 처리 허용)
            target_hit_type = getattr(target.character, 'hit_type', None) if hasattr(target, 'character') else None
            target_is_down = (target_hit_type == 'down')
            target_is_airborne = (target_hit_type == 'airborne') and not target.is_grounded
            target_is_hit = target.is_in_hit_state()

            # 충돌 조건을 더 유연하게 수정
            # 1. 일반적으로 피격 상태가 아니면 히트 가능
            # 2. Lower 계열 공격은 down 상태에도 히트 가능
            # 3. 공중(airborne) 상태는 항상 히트 가능 (에어 콤보)
            allow_hit_on_down = ('lower' in attacker_state) and target_is_down
            allow_hit_on_airborne = target_is_airborne

            # 히트 판정: 피격 상태가 아니거나 특수 조건 만족 시
            can_hit = (not target_is_hit) or allow_hit_on_down or allow_hit_on_airborne

            # 디버그: down 상태 충돌 판정 로그
            if target_is_down and 'lower' in attacker_state:
                print(f"[DEBUG] Player1 Lower attack on DOWN Player2: can_hit={can_hit}, target_is_down={target_is_down}, target_hit_type={target_hit_type}")

            if can_hit:

                # Player1의 공격 범위에 Player2가 있는지 확인
                if self.playerLeft.is_in_attack_range(self.playerRight):
                    # 타격음(swoosh)은 공격 범위에 들어왔을 때 항상 재생
                    if not self.playerLeft.attack_sound_played and hasattr(self.playerLeft, 'swoosh_sound') and self.playerLeft.swoosh_sound:
                        self.playerLeft.swoosh_sound.play()
                        self.playerLeft.attack_sound_played = True

                    # 공중 상태(airborne)일 때는 가드 불가 - 무조건 히트
                    if target_is_airborne:
                        # 공중에서는 가드 불가 - 데미지 적용
                        damage = self.calculate_damage(self.playerLeft.state)
                        # 공격자 참조 전달 (포물선 방향 계산용)
                        self.playerRight.take_damage(damage, self.playerLeft.state, attacker=self.playerLeft)
                        print(f"[AIRBORNE HIT] Player2 took {damage} damage from {self.playerLeft.state} while airborne! HP: {self.playerRight.get_hp()}")
                    else:
                        # 지상 상태에서는 가드 판정 확인
                        can_guard = self.playerRight.can_guard_against_attack(self.playerLeft.state)

                        if can_guard:
                            # 가드 성공 - 데미지 없음, 가드 시작 또는 연장
                            self.playerRight.start_guard()
                            print(f"[GUARD SUCCESS] Player2 guarded {self.playerLeft.state}! Position: {self.playerRight.position_state}, is_attacking: {self.playerRight.is_attacking}, is_hit: {self.playerRight.is_hit}")
                            # 가드 성공 직후, 현재 입력으로 즉시 반격 가능한지 체크
                            self._try_trigger_counterattack_from_input(self.playerRight, is_player2=True)
                        else:
                            # 가드 실패 - 데미지 적용
                            damage = self.calculate_damage(self.playerLeft.state)
                            # 공격자 참조 전달 (포물선 방향 계산용)
                            actual_state = self.playerLeft.state  # 원본 state 유지
                            self.playerRight.take_damage(damage, actual_state, attacker=self.playerLeft)
                            print(f"[HIT] Player2 took {damage} damage from {actual_state}! HP: {self.playerRight.get_hp()}, Position: {self.playerRight.position_state}, is_attacking: {self.playerRight.is_attacking}, is_hit: {self.playerRight.is_hit}")

                    # 타격 처리 완료 마킹
                    self.playerLeft.mark_attack_hit_processed()
                    self.playerLeft.can_process_hit = False

        # Player2가 공격 중이고 타격 처리 가능한 상태인지 확인
        if (self.playerRight.is_attacking and
            hasattr(self.playerRight, 'can_process_hit') and
            self.playerRight.can_process_hit and
            self.playerRight.can_hit_target()):

            # PlayerLeft가 down 상태일 때 Lower 계열 공격은 히트 가능하도록 허용
            attacker_state = (self.playerRight.state or '').lower()
            target = self.playerLeft
            target_hit_type = getattr(target.character, 'hit_type', None) if hasattr(target, 'character') else None
            target_is_down = (target_hit_type == 'down') and target.is_grounded
            target_is_airborne = (target_hit_type == 'airborne') and not target.is_grounded
            target_is_hit = target.is_in_hit_state()

            # Lower 공격인지 확인
            is_lower_attack = 'lower' in attacker_state

            # 충돌 조건을 더 유연하게 수정
            # 1. 일반적으로 피격 상태가 아니면 히트 가능
            # 2. Lower 계열 공격은 down 상태에도 히트 가능
            # 3. 공중(airborne) 상태는 항상 히트 가능 (에어 콤보)
            allow_hit_on_down = is_lower_attack and target_is_down
            allow_hit_on_airborne = target_is_airborne

            # 히트 판정: 피격 상태가 아니거나 특수 조건 만족 시
            can_hit = (not target_is_hit) or allow_hit_on_down or allow_hit_on_airborne

            # 디버그: down 상태 충돌 판정 로그
            if is_lower_attack:
                print(f"[DEBUG] Player2 Lower attack: target_is_down={target_is_down}, target_is_hit={target_is_hit}, target_hit_type={target_hit_type}, can_hit={can_hit}, target_grounded={target.is_grounded}")

            if can_hit:

                # Player2의 공격 범위에 Player1이 있는지 확인
                if self.playerRight.is_in_attack_range(self.playerLeft):
                    # 타격음(swoosh)은 공격 범위에 들어왔을 때 항상 재생
                    if not self.playerRight.attack_sound_played and hasattr(self.playerRight, 'swoosh_sound') and self.playerRight.swoosh_sound:
                        self.playerRight.swoosh_sound.play()
                        self.playerRight.attack_sound_played = True

                    # 공중 상태(airborne)일 때는 가드 불가 - 무조건 히트
                    if target_is_airborne:
                        # 공중에서는 가드 불가 - 데미지 적용
                        damage = self.calculate_damage(self.playerRight.state)
                        # 공격자 참조 전달 (포물선 방향 계산용)
                        self.playerLeft.take_damage(damage, self.playerRight.state, attacker=self.playerRight)
                        print(f"[AIRBORNE HIT] Player1 took {damage} damage from {self.playerRight.state} while airborne! HP: {self.playerLeft.get_hp()}")
                    else:
                        # 지상 상태에서는 가드 판정 확인
                        can_guard = self.playerLeft.can_guard_against_attack(self.playerRight.state)

                        if can_guard:
                            # 가드 성공 - 데미지 없음, 가드 시작 또는 연장
                            self.playerLeft.start_guard()
                            print(f"[GUARD SUCCESS] Player1 guarded {self.playerRight.state}! Position: {self.playerLeft.position_state}, is_attacking: {self.playerLeft.is_attacking}, is_hit: {self.playerLeft.is_hit}")
                            # 가드 성공 직후, 현재 입력으로 즉시 반격 가능한지 체크
                            self._try_trigger_counterattack_from_input(self.playerLeft, is_player2=False)
                        else:
                            # 가드 실패 - 데미지 적용
                            damage = self.calculate_damage(self.playerRight.state)
                            # 공격자 참조 전달 (포물선 방향 계산용)
                            actual_state = self.playerRight.state  # 원본 state 유지
                            self.playerLeft.take_damage(damage, actual_state, attacker=self.playerRight)
                            print(f"[HIT] Player1 took {damage} damage from {actual_state}! HP: {self.playerLeft.get_hp()}, Position: {self.playerLeft.position_state}, is_attacking: {self.playerLeft.is_attacking}, is_hit: {self.playerLeft.is_hit}")

                    # 타격 처리 완료 마킹
                    self.playerRight.mark_attack_hit_processed()
                    self.playerRight.can_process_hit = False

    def calculate_damage(self, attack_state):
        """공격 상태에 따른 데미지 계산"""
        # fast 공격들은 모두 10데미지
        if 'fast' in attack_state.lower():
            return 10
        # strong 공격들은 모두 20데미지
        elif 'strong' in attack_state.lower():
            return 20
        # rage 스킬은 특별히 30데미지
        elif 'rage' in attack_state.lower():
            return 30
        else:
            # 기본 데미지 (혹시 모를 다른 공격들)
            return 5

    def update(self, deltaTime):
        # deltaTime 제한 - 너무 큰 값이 들어오면 제한
        deltaTime = min(deltaTime, self.max_delta_time)

        events = pico2d.get_events()

        # F1 키로 바운딩 박스 토글
        if self.ioManager.checkF1Toggle(events):
            config.SHOW_BOUNDING_BOX = not config.SHOW_BOUNDING_BOX
            print(f"[DEBUG] Bounding Box Display: {'ON' if config.SHOW_BOUNDING_BOX else 'OFF'}")

        # ESC 키로 종료 처리
        if self.ioManager.checkEscape(events):
            self.running = False
            return

        # 종료 이벤트 처리
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                self.running = False

        # 타이틀 씬에서는 스페이스바로 캐릭터 선택으로 전환
        if self.sceneManager.is_title_scene():
            # 씬 매니저 업데이트 호출 (애니메이션이 있을 경우를 대비)
            self.sceneManager.update(deltaTime)
            if self.ioManager.handleSpaceInput(events):
                self.sceneManager.change_to_character_select()
            return

        # 캐릭터 선택 씬 처리
        if self.sceneManager.is_character_select_scene():
            char_select = self.sceneManager.get_character_select_scene()
            char_select.handle_input(events)

            # 씬 매니저 업데이트 호출 (애니메이션 재생을 위해)
            self.sceneManager.update(deltaTime)

            # 두 플레이어 모두 선택 완료시 플레이 씬으로 전환
            if char_select.is_both_selected():
                p1_char, p2_char = char_select.get_selected_characters()
                # 플레이어 캐릭터 설정
                self.playerLeft.change_character(p1_char)
                self.playerRight.change_character(p2_char)

                # 플레이어 초기 위치 설정
                self.playerLeft.x = config.windowWidth * 0.35
                self.playerRight.x = config.windowWidth * 0.65
                self.playerLeft.y = config.GROUND_Y
                self.playerRight.y = config.GROUND_Y

                # 플레이어 방향 설정
                self.playerLeft.dir = 1
                self.playerRight.dir = -1
                self.playerLeft.facing_right = True
                self.playerRight.facing_right = False

                # spriteManager 캐릭터 타입 즉시 업데이트
                self.spriteManager.player1_character_type = p1_char
                self.spriteManager.player2_character_type = p2_char

                # spriteManager 위치 및 상태 동기화
                self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
                self.spriteManager.update_player2_position(self.playerRight.x, self.playerRight.y)
                self.spriteManager.update_player1_direction(self.playerLeft.dir)
                self.spriteManager.update_player2_direction(self.playerRight.dir)

                # 플레이어 상태를 Idle로 초기화하고 spriteManager에 반영
                self.playerLeft.state = 'Idle'
                self.playerRight.state = 'Idle'
                self.spriteManager.player1_state = 'Idle'
                self.spriteManager.player2_state = 'Idle'
                self.spriteManager.player1_frame = 0
                self.spriteManager.player2_frame = 0
                self.spriteManager.frame_timer = 0.0
                self.spriteManager.player2_frame_timer = 0.0

                # 플레이 씬으로 전환
                self.sceneManager.change_to_play_scene()
            return

        # 씬 전환 중일 때는 씬 매니저 업데이트만 하고 게임 로직 멈춤
        if self.sceneManager.check_is_transitioning():
            self.sceneManager.update(deltaTime)
            return

        # 게임 오버 상태면 스페이스바로 타이틀 복귀
        if self.game_over:
            if self.ioManager.handleSpaceInput(events):
                # 타이틀로 돌아가기
                self.reset_to_title()
            return

        # 카운트다운 중일 때는 플레이씬 업데이트만 하고 게임 로직은 멈춤
        play_scene = self.sceneManager.play_scene
        if play_scene.countdown_active:
            play_scene.update(deltaTime)
            return

        # 플레이어 입력 처리 - HP가 0 이하면 입력 무시
        if self.playerLeft.get_hp() > 0:
            player1_move_input = self.ioManager.handleMoveInputPlayer1(events)
            player1_atk_input = self.ioManager.handleATKInputPlayer1(events)
            player1_char_change = self.ioManager.handleCharacterChangePlayer1(events)
            player1_position_state = self.ioManager.get_player1_position_state()
            player1_getup_input = self.ioManager.check_player1_getup_input()  # 기상 입력 추가
            player1_combo = self.ioManager.check_player1_combo_input(self.playerLeft.state)
        else:
            # HP가 0 이하면 입력 무시
            player1_move_input = None
            player1_atk_input = None
            player1_char_change = None
            player1_position_state = self.playerLeft.position_state
            player1_getup_input = False
            player1_combo = False

        if self.playerRight.get_hp() > 0:
            player2_move_input = self.ioManager.handleMoveInputPlayer2(events)
            player2_atk_input = self.ioManager.handleATKInputPlayer2(events)
            player2_position_state = self.ioManager.get_player2_position_state()
            player2_getup_input = self.ioManager.check_player2_getup_input()  # 기상 입력 추가
            player2_combo = self.ioManager.check_player2_combo_input(self.playerRight.state)
        else:
            # HP가 0 이하면 입력 무시
            player2_move_input = None
            player2_atk_input = None
            player2_position_state = self.playerRight.position_state
            player2_getup_input = False
            player2_combo = False

        # 플레이어 업데이트 (기상 입력 포함)
        self.playerLeft.update(deltaTime, player1_move_input, player1_atk_input, player1_combo, player1_char_change, self.playerRight, player1_position_state, player1_getup_input)
        self.playerRight.update(deltaTime, player2_move_input, player2_atk_input, player2_combo, None, self.playerLeft, player2_position_state, player2_getup_input)

        # 충돌 및 공격 판정
        self.check_collision()

        # 플레이씬의 라운드 체크 (3판 2선승제)
        play_scene = self.sceneManager.play_scene
        play_scene.check_round_end(self.playerLeft.get_hp(), self.playerRight.get_hp())

        # 라운드 종료 시 처리
        if play_scene.is_round_over() and not play_scene.is_game_over():
            # 라운드 종료 후 1.5초 대기 후 다음 라운드 시작
            self.round_end_timer += deltaTime

            # 1.5초 대기 후 다음 라운드 시작
            if self.round_end_timer >= 1.8:
                self.reset_round()
                self.round_end_timer = 0.0

        # 게임 전체 종료 체크
        if play_scene.is_game_over():
            self.game_over = True

        # SpriteManager에 플레이어 상태 전달 - 플레이어 업데이트 후에 실행
        self.spriteManager.update_player1_state(self.playerLeft.state, deltaTime)
        self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
        self.spriteManager.update_player1_direction(self.playerLeft.dir)

        self.spriteManager.update_player2_state(self.playerRight.state, deltaTime)
        self.spriteManager.update_player2_position(self.playerRight.x, self.playerRight.y)
        self.spriteManager.update_player2_direction(self.playerRight.dir)

    def render(self):
        pico2d.clear_canvas()

        # 플레이씬으로 전환 중이거나 플레이 씬일 때
        is_play_or_transitioning = (
            (not self.sceneManager.is_title_scene() and not self.sceneManager.is_character_select_scene()) or
            self.sceneManager.is_transitioning_to_play()
        )

        # 전환 중일 때는 sceneManager가 render 처리
        if self.sceneManager.is_transitioning:
            self.sceneManager.render()
        # 플레이 씬에서는 HP 정보를 전달하여 렌더링
        elif not self.sceneManager.is_title_scene() and not self.sceneManager.is_character_select_scene():
            play_scene = self.sceneManager.play_scene
            play_scene.render(
                player1_hp=self.playerLeft.get_hp(),
                player1_max_hp=self.playerLeft.max_hp,
                player2_hp=self.playerRight.get_hp(),
                player2_max_hp=self.playerRight.max_hp
            )
        else:
            self.sceneManager.render()

        # 플레이 씬이거나 플레이씬으로 전환 중일 때 플레이어 렌더링
        if is_play_or_transitioning:
            self.spriteManager.render()
            # 바운딩 박스 렌더링을 위해 플레이어 render 호출 (HP는 플레이씬에서 렌더링)
            self.playerLeft.render()
            self.playerRight.render()


        pico2d.update_canvas()

    def run(self):
        current_time = time.time()
        deltaTime = current_time - self.last_time

        # 첫 프레임에서 deltaTime이 너무 크지 않도록 제한
        if self.last_time == 0:
            deltaTime = self.frame_time

        # 프레임 제한 - 너무 빠르면 대기
        if deltaTime < self.frame_time:
            time.sleep(self.frame_time - deltaTime)
            current_time = time.time()
            deltaTime = current_time - self.last_time

        self.last_time = current_time

        self.update(deltaTime)
        self.render()

    def _try_trigger_counterattack_from_input(self, target_player, is_player2=False):
        """가드 성공 직후 현재 입력으로 즉시 반격 시작 시도
        - target_player: 가드를 성공한 플레이어 객체
        - is_player2: True면 player2 키맵 사용, False면 player1 키맵 사용
        """
        # 입력 키 상태 참조
        if is_player2:
            keys = self.ioManager.player2_keys
        else:
            keys = self.ioManager.player1_keys

        # 우선순위: fast(slash for P2, f for P1), strong(shift for P2, g for P1)
        candidate_attack = None

        # fast / strong 분기
        if (is_player2 and keys.get('slash')) or (not is_player2 and keys.get('f')):
            # up/down 조합 확인
            if (is_player2 and keys.get('up')) or (not is_player2 and keys.get('w')):
                candidate_attack = 'fastUpperATK'
            elif (is_player2 and keys.get('down')) or (not is_player2 and keys.get('s')):
                candidate_attack = 'fastLowerATK'
            else:
                candidate_attack = 'fastMiddleATK'
        elif (is_player2 and keys.get('shift')) or (not is_player2 and keys.get('g')):
            if (is_player2 and keys.get('up')) or (not is_player2 and keys.get('w')):
                candidate_attack = 'strongUpperATK'
            elif (is_player2 and keys.get('down')) or (not is_player2 and keys.get('s')):
                candidate_attack = 'strongLowerATK'
            else:
                candidate_attack = 'strongMiddleATK'

        # 후보 공격이 있는 경우 처리
        if candidate_attack:
            # 사용 가능한 공격인지 확인
            if hasattr(target_player, 'can_use_attack') and target_player.can_use_attack(candidate_attack):
                # 현재 공격 중이 아니어야 함
                if not target_player.is_attacking:
                    # 가드 상태 해제 및 공격 시작
                    target_player.is_guarding = False
                    if hasattr(target_player, 'can_attack_after_guard'):
                        target_player.can_attack_after_guard = False
                    if hasattr(target_player, 'guard_counter_timer'):
                        target_player.guard_counter_timer = 0.0
                    if hasattr(target_player, 'guard_animation_reset'):
                        target_player.guard_animation_reset = False

                    target_player.state = candidate_attack
                    target_player.character.state = candidate_attack  # Character 상태도 동기화
                    target_player.is_attacking = True
                    if hasattr(target_player, 'reset_attack_hit_flag'):
                        target_player.reset_attack_hit_flag()

                    # 연계 가능 설정 (기존 로직과 동일)
                    if candidate_attack in ['fastMiddleATK', 'strongMiddleATK', 'strongUpperATK']:
                        target_player.can_combo = True
                    else:
                        target_player.can_combo = False

                    target_player.combo_reserved = False

                    print(f"Counterattack triggered immediately after guard: {candidate_attack} (Player {'2' if is_player2 else '1'})")
                    return True
                else:
                    print(f"Cannot counterattack while already attacking (Player {'2' if is_player2 else '1'})")
            else:
                print(f"Cannot use attack {candidate_attack} for current character (Player {'2' if is_player2 else '1'})")

        return False

    def reset_round(self):
        """라운드 리셋 - 플레이어 위치 및 HP 초기화"""
        # 플레이어 HP 리셋
        self.playerLeft.hp = self.playerLeft.max_hp
        self.playerRight.hp = self.playerRight.max_hp

        # Character HP도 동기화
        self.playerLeft.character.hp = self.playerLeft.max_hp
        self.playerRight.character.hp = self.playerRight.max_hp

        # 플레이어 위치 리셋
        self.playerLeft.x = config.windowWidth * 0.35
        self.playerRight.x = config.windowWidth * 0.65
        self.playerLeft.y = config.GROUND_Y
        self.playerRight.y = config.GROUND_Y

        # 플레이어 상태 리셋
        self.playerLeft.state = 'Idle'
        self.playerRight.state = 'Idle'
        self.playerLeft.is_attacking = False
        self.playerRight.is_attacking = False
        self.playerLeft.is_hit = False
        self.playerRight.is_hit = False
        self.playerLeft.is_grounded = True
        self.playerRight.is_grounded = True
        self.playerLeft.velocity_x = 0.0
        self.playerRight.velocity_x = 0.0
        self.playerLeft.velocity_y = 0.0
        self.playerRight.velocity_y = 0.0

        # 추가 플레이어 상태 리셋
        self.playerLeft.position_state = 'Middle'
        self.playerRight.position_state = 'Middle'
        self.playerLeft.hit_recovery_input = False
        self.playerRight.hit_recovery_input = False
        self.playerLeft.can_combo = False
        self.playerRight.can_combo = False
        self.playerLeft.combo_reserved = False
        self.playerRight.combo_reserved = False
        self.playerLeft.is_guarding = False
        self.playerRight.is_guarding = False
        self.playerLeft.attack_hit_processed = False
        self.playerRight.attack_hit_processed = False
        self.playerLeft.can_process_hit = False
        self.playerRight.can_process_hit = False
        self.playerLeft.can_attack_after_guard = False
        self.playerRight.can_attack_after_guard = False
        self.playerLeft.guard_counter_timer = 0.0
        self.playerRight.guard_counter_timer = 0.0

        # 플레이어 방향 리셋
        self.playerLeft.dir = 1
        self.playerRight.dir = -1
        self.playerLeft.facing_right = True
        self.playerRight.facing_right = False

        # 캐릭터 피격 상태 리셋
        self.playerLeft.character.is_hit = False
        self.playerRight.character.is_hit = False
        self.playerLeft.character.hit_type = None
        self.playerRight.character.hit_type = None
        self.playerLeft.character.can_get_up = False
        self.playerRight.character.can_get_up = False
        self.playerLeft.character.state = 'Idle'
        self.playerRight.character.state = 'Idle'
        self.playerLeft.character.frame = 0
        self.playerRight.character.frame = 0
        self.playerLeft.character.velocity_y = 0.0
        self.playerRight.character.velocity_y = 0.0
        self.playerLeft.character.is_grounded = True
        self.playerRight.character.is_grounded = True

        # 캐릭터 위치 동기화
        self.playerLeft.character.x = self.playerLeft.x
        self.playerLeft.character.y = self.playerLeft.y
        self.playerRight.character.x = self.playerRight.x
        self.playerRight.character.y = self.playerRight.y

        # spriteManager 상태 동기화
        self.spriteManager.player1_state = 'Idle'
        self.spriteManager.player2_state = 'Idle'
        self.spriteManager.player1_frame = 0
        self.spriteManager.player2_frame = 0
        self.spriteManager.frame_timer = 0.0
        self.spriteManager.player2_frame_timer = 0.0
        self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
        self.spriteManager.update_player2_position(self.playerRight.x, self.playerRight.y)
        self.spriteManager.update_player1_direction(self.playerLeft.dir)
        self.spriteManager.update_player2_direction(self.playerRight.dir)

        # 플레이씬의 라운드 리셋
        self.sceneManager.play_scene.reset_round()

        # 겹침 방지
        CollisionHandler.prevent_overlap_on_spawn(self.playerLeft, self.playerRight)

        print("Round reset! New round starting...")

    def reset_to_title(self):
        """게임을 초기화하고 타이틀 화면으로 돌아가기"""
        # 게임 상태 초기화
        self.game_over = False
        self.round_end_timer = 0.0

        # 플레이씬 초기화
        self.sceneManager.play_scene.reset_game()

        # 플레이어 초기화
        self.playerLeft.hp = self.playerLeft.max_hp
        self.playerRight.hp = self.playerRight.max_hp
        self.playerLeft.character.hp = self.playerLeft.max_hp
        self.playerRight.character.hp = self.playerRight.max_hp

        # 플레이어 위치 리셋
        self.playerLeft.x = config.windowWidth * 0.35
        self.playerRight.x = config.windowWidth * 0.65
        self.playerLeft.y = config.GROUND_Y
        self.playerRight.y = config.GROUND_Y

        # spriteManager 위치 업데이트
        self.spriteManager.update_player1_position(self.playerLeft.x, self.playerLeft.y)
        self.spriteManager.update_player2_position(self.playerRight.x, self.playerRight.y)

        # 플레이어 상태 리셋
        self.playerLeft.state = 'Idle'
        self.playerRight.state = 'Idle'
        self.playerLeft.is_attacking = False
        self.playerRight.is_attacking = False
        self.playerLeft.is_hit = False
        self.playerRight.is_hit = False

        # 캐릭터 상태 리셋
        self.playerLeft.character.state = 'Idle'
        self.playerRight.character.state = 'Idle'
        self.playerLeft.character.is_hit = False
        self.playerRight.character.is_hit = False

        # spriteManager 상태 리셋
        self.spriteManager.player1_state = 'Idle'
        self.spriteManager.player2_state = 'Idle'
        self.spriteManager.player1_frame = 0
        self.spriteManager.player2_frame = 0
        self.spriteManager.frame_timer = 0.0
        self.spriteManager.player2_frame_timer = 0.0

        # 타이틀 씬으로 전환
        self.sceneManager.current_scene = 'title'

        print("Game reset! Returning to title screen...")

        print("Returning to title screen...")

