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
PRIMARY_SKILL = TeleportSkill
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
        enemy_hp = get_hp(enemy)
        enemy_block_status = get_block_status(enemy)

        # List of possible moves
        possible_moves = []

        # Defensive moves
        if enemy_block_status:
            possible_moves.append(BLOCK)

        # Offensive moves
        if distance == 1:
            if enemy_hp < 90:
                possible_moves.append(HEAVY)
            elif enemy_hp < 98:
                possible_moves.append(LIGHT)

        # Skill usage based on different conditions
        if enemy_hp < 50:
            possible_moves.append(("skill", SECONDARY))
        if get_hp(player) < 30:
            possible_moves.append(("skill", PRIMARY))

        # Combo moves
        combo_moves = [(LIGHT, LIGHT, HEAVY), (LIGHT, HEAVY, HEAVY), (HEAVY, LIGHT, HEAVY)]
        for combo in combo_moves:
            if all(move in possible_moves for move in combo):
                return combo

        # Movement
        if not possible_moves:
            if distance == 1:
                possible_moves.append(BACK)
            else:
                possible_moves.append(FORWARD)

        # Randomly choose from possible moves
        return choice(possible_moves)
            
