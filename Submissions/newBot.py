# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = SuperSaiyanSkill

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
CANCEL = ("skill_cancel", )

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
        hp_player = get_hp(player)
        hp_enemy = get_hp(enemy)
        
        enemy_distance=get_distance(player,enemy)

        my_skills = [get_primary_skill(player), get_secondary_skill(player)]
        enemy_skills = [get_primary_skill(enemy), get_secondary_skill(enemy)]

        if enemy_projectiles:
            if get_projectile_type(enemy_projectiles[0])==Grenade:
                if get_distance(player,enemy)<3:
                    return JUMP_BACKWARD
            else:
                return JUMP_FORWARD
        if enemy_distance<3 :
            return JUMP_BACKWARD
        if enemy_distance>3 and not secondary_on_cooldown:
            return SECONDARY
        
        if enemy_distance<5 and not primary_on_cooldown:
            return PRIMARY

        if enemy_distance<2 and not heavy_on_cooldown:
            return HEAVY
            
        if get_distance(player,enemy)==1:
            return LIGHT

        return LIGHT
            


        
        
