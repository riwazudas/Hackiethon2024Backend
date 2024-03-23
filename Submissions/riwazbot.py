# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN
from random import randint, random

# Define your Q-Learning agent class
class QLearningAgent:
    def __init__(self, num_actions, num_states, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.num_actions = num_actions
        self.num_states = num_states
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = [[0] * num_actions for _ in range(num_states)]

    def choose_action(self, state):
        if random() < self.epsilon:
            return randint(0, self.num_actions - 1)  
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        return self.q_table[state].index(max(self.q_table[state]))

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = self.get_best_action(next_state)
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

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
CANCEL = ("skill_cancel", )

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)


agent = QLearningAgent(num_actions=12, num_states=2) 

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
        # Assuming your state space has 2 states (for demonstration)
        # You need to define your own state representation
        # Example: state = 0 if player's health is higher else 1
        state = 0 if get_hp(player) > get_hp(enemy) else 1

        # Choose action using Q-Learning agent
        action = agent.choose_action(state)

        # Execute action based on chosen action
        if action == 0:
            move = FORWARD
        elif action == 1:
            move = BACK
        elif action == 2:
            move = LIGHT
        elif action == 3:
            move = HEAVY
        elif action == 4:
            move = BLOCK
        elif action == 5:
            move = JUMP
        elif action == 6:
            move = JUMP_BACKWARD
        elif action == 7:
            move = JUMP_FORWARD
        elif action == 8:
            move = PRIMARY
        elif action == 9:
            move = SECONDARY
        elif action ==10:
            move = CANCEL
        else:
            move = NOMOVE

        # Update Q-table if this is not the first move
        if get_landed(player):
            reward +=1  # Define your own reward mechanism based on game state
            agent.update_q_table(self.previous_state, self.previous_action, reward, state)

        # Store current state and action as previous state and action for the next iteration
        self.previous_state = state
        self.previous_action = action

        return move