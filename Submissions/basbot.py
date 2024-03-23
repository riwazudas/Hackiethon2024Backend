# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN
from random import choice

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Hadoken

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        enemystun_time = abs(get_stun_duration(enemy))
        lastmove = get_last_move(enemy)
        enemyhp = abs(get_hp(enemy))
        ourhp = abs(get_hp(player))
        enemyblockstatus = get_block_status(enemy)
        enemyprojpos = get_proj_pos(enemy)[0]

        # Define a list of possible moves to choose from
        possible_moves = []

        # Defensive moves
        if enemyblockstatus:
            possible_moves.append(BLOCK)
        elif distance == 1 and enemy == JUMP:
            possible_moves.append(BLOCK)

        # Offensive moves
        if distance == 1:
            if lastmove == LIGHT and ourhp < 90:
                possible_moves.append(HEAVY)
            elif lastmove == LIGHT and ourhp < 98:
                possible_moves.append(LIGHT)
            elif enemystun_time >= 1:
                possible_moves.append(HEAVY)
            elif enemy == JUMP:
                possible_moves.append(self.primary)
            elif enemy == LIGHT:
                possible_moves.append(BLOCK)

        # Skill usage based on different conditions
        if enemyhp < 50:
            possible_moves.append(SECONDARY)
        if ourhp < 30:
            possible_moves.append(PRIMARY)
        # Combination of Dash Attack Skill
        combodashattack = [BACK, JUMP_BACKWARD, SECONDARY]
        combodashattack_index = 0
           # Check if combo move can be executed
        if distance <= 5 and not enemyblockstatus:
            possible_moves.extend(combodashattack)
        # Movement
        if not possible_moves:
            if distance == 1:
                possible_moves.append(BACK)
            else:
                possible_moves.append(FORWARD)

        # Combo move: Light attack, Heavy attack, Secondary skill
        combo_sequence = [LIGHT, HEAVY, SECONDARY]
        combo_index = 0

        # Check if the next move in the combo sequence is available
        if len(possible_moves) > 0 and possible_moves[0] in combo_sequence:
            if possible_moves[0] == combo_sequence[combo_index]:
                combo_index += 1
                if combo_index == len(combo_sequence):
                    # Execute the combo move
                    return combo_sequence
            else:
                # Reset combo index if the sequence is broken
                combo_index = 0

        # Randomly choose from possible moves if combo is not available or completed
        return choice(possible_moves)
            
