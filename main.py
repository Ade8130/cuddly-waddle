import sys
import numpy as np
import math
import random
import pygame
import gym
import gym_game
from gym_game.envs.observer import Observer
import pickle
import json
import os
import numpy

# Policy take a state and returns an action
def policy(state):
    global epsilon, q_table
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample() # Exploration

    return np.argmax(q_table[state]) # Exploitation

def learn():
    global epsilon, learning_rate, render_detail_move, q_table
    for episode in range(MAX_EPISODES):

        # Init environment
        state = env.reset()
        total_reward = 0

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # Policy is to do random action to learn at begining
            action = policy(state)

            # Do action and get result
            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[state][action]
            best_q = np.max(q_table[next_state])

            # Temporal Difference Method:
            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[state][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw games
            if(render_detail_move == True):
                env.render()

            # When episode is done, print reward

            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                break

            if exit_program:
                return
        
        if(render_detail_move == False):
            env.render()

        epsilon = get_rate(epsilon)
        learning_rate = get_rate(learning_rate)
            
def get_rate(i):
    global epsilon_decay
    return (i * epsilon_decay)

# def get_rate(t, i):
#     return max(i, min(1, 1.0 + math.log10((t+1)/25)))  

def s_key_pressed(key):
    global render_detail_move, exit_program
    if( key ==  pygame.K_s):
        render_detail_move = not render_detail_move
    if( key ==  pygame.K_ESCAPE):
        exit_program = True

if __name__ == "__main__":
    env = gym.make("Babak-v0", observer=Observer(s_key_pressed))
    render_detail_move = False
    MAX_EPISODES = 9999999
    MAX_TRY = 100000
    epsilon_decay = 0.9999
    epsilon = 1
    learning_rate = 0.5

    gamma = 0.8
    exit_program = False
    num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    # Load Q-Table
    if os.path.isfile('q_table.npy'):
        q_table = numpy.load('q_table.npy')
    else:
        q_table = np.zeros(num_box + (env.action_space.n,))
    learn()

    # Save Q-Table
    numpy.save("q_table", q_table)
    
    # Apply learnt knowldge
    exit_program = False
    state = env.reset()
    for t in range(100):
        
        if exit_program:
                break

        action = np.argmax(q_table[state]) # Exploitation
        next_state, reward, done, _ = env.step(action)
        # Set up for the next iteration
        state = next_state
        env.render()
