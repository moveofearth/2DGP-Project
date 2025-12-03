"""
충돌 처리 전용 모듈
플레이어 간 충돌, 화면 경계 충돌을 안정적으로 처리
"""
import config


class CollisionHandler:
    """충돌 처리를 담당하는 클래스"""

    @staticmethod
    def get_aabb(player):
        """플레이어의 AABB 바운딩 박스 반환"""
        return player.get_bb()

    @staticmethod
    def check_aabb_collision(bb1, bb2):
        """두 AABB 바운딩 박스의 충돌 검사"""
        return (bb1[0] < bb2[2] and bb1[2] > bb2[0] and
                bb1[1] < bb2[3] and bb1[3] > bb2[1])

    @staticmethod
    def get_overlap(bb1, bb2):
        """두 바운딩 박스의 겹침 정도 계산
        Returns: (overlap_x, overlap_y) - 양수면 겹침
        """
        overlap_x = min(bb1[2], bb2[2]) - max(bb1[0], bb2[0])
        overlap_y = min(bb1[3], bb2[3]) - max(bb1[1], bb2[1])
        return overlap_x, overlap_y

    @staticmethod
    def check_player_collision(player1, player2):
        """두 플레이어 간 충돌 검사"""
        if not player1 or not player2:
            return False

        bb1 = CollisionHandler.get_aabb(player1)
        bb2 = CollisionHandler.get_aabb(player2)

        return CollisionHandler.check_aabb_collision(bb1, bb2)

    @staticmethod
    def resolve_player_collision(player1, player2):
        """두 플레이어 간 충돌 해결 - 양방향으로 밀어냄

        더 안정적인 충돌 해결:
        1. 겹친 양만큼 양쪽으로 균등하게 분배
        2. 피격 중인 플레이어는 밀리지 않음 (물리 계산으로 이미 날아가는 중)
        3. 공격 중인 플레이어 우선권 부여
        4. 화면 경계 고려
        """
        if not player1 or not player2:
            return

        bb1 = CollisionHandler.get_aabb(player1)
        bb2 = CollisionHandler.get_aabb(player2)

        if not CollisionHandler.check_aabb_collision(bb1, bb2):
            return  # 충돌하지 않음

        # 겹침 계산
        overlap_x, overlap_y = CollisionHandler.get_overlap(bb1, bb2)

        if overlap_x <= 0 or overlap_y <= 0:
            return  # 실제로 겹치지 않음

        # 피격 중인 플레이어는 물리 계산으로 이동하므로 충돌 해결에서 제외
        player1_is_hit = getattr(player1, 'is_hit', False)
        player2_is_hit = getattr(player2, 'is_hit', False)

        # 공중에 떠있는 플레이어 체크
        player1_is_airborne = not getattr(player1, 'is_grounded', True)
        player2_is_airborne = not getattr(player2, 'is_grounded', True)

        # 양쪽 다 피격 중이거나 공중에 있으면 충돌 무시 (서로 날아가는 중)
        if (player1_is_hit and player2_is_hit) or (player1_is_airborne and player2_is_airborne):
            return

        # 한쪽만 피격 중이면 피격되지 않은 쪽만 밀어냄
        if player1_is_hit or player1_is_airborne:
            # player1이 피격/공중 -> player2만 밀어냄
            if player1.x < player2.x:
                player2.x += overlap_x
            else:
                player2.x -= overlap_x
            # 화면 경계 보정
            CollisionHandler.clamp_to_screen(player2)
            return

        if player2_is_hit or player2_is_airborne:
            # player2가 피격/공중 -> player1만 밀어냄
            if player1.x < player2.x:
                player1.x -= overlap_x
            else:
                player1.x += overlap_x
            # 화면 경계 보정
            CollisionHandler.clamp_to_screen(player1)
            return

        # 양쪽 다 정상 상태 -> 균등하게 밀어냄
        push_distance = overlap_x / 2.0

        # 공격 중인 플레이어는 덜 밀림 (우선권)
        player1_attacking = getattr(player1, 'is_attacking', False)
        player2_attacking = getattr(player2, 'is_attacking', False)

        if player1_attacking and not player2_attacking:
            # player1이 공격 중 -> player2를 더 많이 밀어냄
            push_ratio = 0.2  # player1은 20%만 밀림
        elif player2_attacking and not player1_attacking:
            # player2가 공격 중 -> player1을 더 많이 밀어냄
            push_ratio = 0.8  # player1은 80% 밀림
        else:
            # 둘 다 공격 중이거나 둘 다 평상시 -> 균등하게
            push_ratio = 0.5

        # 위치 관계에 따라 밀어내기
        if player1.x < player2.x:
            # player1이 왼쪽에 있음
            player1.x -= push_distance * push_ratio * 2
            player2.x += push_distance * (1.0 - push_ratio) * 2
        else:
            # player1이 오른쪽에 있음
            player1.x += push_distance * push_ratio * 2
            player2.x -= push_distance * (1.0 - push_ratio) * 2

        # 양쪽 모두 화면 경계 보정
        CollisionHandler.clamp_to_screen(player1)
        CollisionHandler.clamp_to_screen(player2)

    @staticmethod
    def clamp_to_screen(player, margin=60):
        """플레이어를 화면 경계 내로 제한

        Args:
            player: 플레이어 객체
            margin: 화면 가장자리 여백 (바운딩 박스 반폭 + 여유)
        """
        if not player:
            return

        # 왼쪽 경계
        if player.x < margin:
            player.x = margin
        # 오른쪽 경계
        elif player.x > config.windowWidth - margin:
            player.x = config.windowWidth - margin

    @staticmethod
    def clamp_position(x, margin=60):
        """위치값을 화면 경계 내로 제한

        Args:
            x: x 좌표
            margin: 화면 가장자리 여백

        Returns:
            제한된 x 좌표
        """
        if x < margin:
            return margin
        elif x > config.windowWidth - margin:
            return config.windowWidth - margin
        return x

    @staticmethod
    def safe_move_player(player, new_x, other_player=None, margin=60):
        """안전하게 플레이어 이동 (충돌 및 경계 검사 포함)

        Args:
            player: 이동할 플레이어
            new_x: 새로운 x 좌표
            other_player: 충돌 검사할 상대 플레이어
            margin: 화면 가장자리 여백

        Returns:
            실제로 이동한 x 좌표
        """
        if not player:
            return player.x if player else 0

        # 이전 위치 저장
        old_x = player.x

        # 화면 경계 먼저 체크
        new_x = CollisionHandler.clamp_position(new_x, margin)

        # 새 위치로 임시 이동
        player.x = new_x

        # 다른 플레이어와 충돌 검사
        if other_player and CollisionHandler.check_player_collision(player, other_player):
            # 충돌 발생 - 양방향 해결
            CollisionHandler.resolve_player_collision(player, other_player)
            # resolve_player_collision에서 이미 위치를 조정했으므로
            # 현재 player.x가 최종 위치
            return player.x

        # 충돌 없음 - 새 위치 유지
        return player.x

    @staticmethod
    def prevent_overlap_on_spawn(player1, player2, min_distance=120):
        """스폰 시 플레이어가 겹치지 않도록 보정

        Args:
            player1, player2: 플레이어 객체들
            min_distance: 최소 유지 거리 (픽셀)
        """
        if not player1 or not player2:
            return

        distance = abs(player1.x - player2.x)

        if distance < min_distance:
            # 거리가 너무 가까움 - 밀어내기
            shortage = min_distance - distance

            if player1.x < player2.x:
                # player1이 왼쪽
                player1.x -= shortage / 2
                player2.x += shortage / 2
            else:
                # player1이 오른쪽
                player1.x += shortage / 2
                player2.x -= shortage / 2

            # 화면 경계 보정
            CollisionHandler.clamp_to_screen(player1)
            CollisionHandler.clamp_to_screen(player2)


# 편의 함수들
def check_collision(player1, player2):
    """두 플레이어 충돌 검사 (편의 함수)"""
    return CollisionHandler.check_player_collision(player1, player2)


def resolve_collision(player1, player2):
    """두 플레이어 충돌 해결 (편의 함수)"""
    CollisionHandler.resolve_player_collision(player1, player2)


def safe_move(player, new_x, other_player=None):
    """안전한 플레이어 이동 (편의 함수)"""
    return CollisionHandler.safe_move_player(player, new_x, other_player)


def clamp_to_screen(player):
    """화면 경계 제한 (편의 함수)"""
    CollisionHandler.clamp_to_screen(player)

