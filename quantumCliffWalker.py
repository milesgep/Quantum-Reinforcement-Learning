import gym
import itertools
import matplotlib
import numpy as np
import pandas as pd
import sys

import warnings

import groverIteration as GI
from qiskit import QuantumProgram

if "../" not in sys.path:
  sys.path.append("../") 

from collections import defaultdict
from lib.envs.cliff_walking import CliffWalkingEnv
from lib import plotting

matplotlib.style.use('ggplot')

### will determine L -> how many times the eigenAction need to be amplified according to the reward and the next eigenState
def groverIteration(Q_program, eigenAction, qr, action, reward, nextStateValue):

    #if L < 2:
    L = int(.2*(reward+nextStateValue)) #reward + value of the nextState, k is .3 which is arbitrary

    if(L > 2):
     	L = 2

    if(L > 0):
    	print("L is greater than 0")

    if(action == 0):
      	for x in range(L):
            eigenAction, qr = GI.gIteration00(eigenAction, qr)
    elif(action == 1):
       	for x in range(L):
            eigenAction, qr = GI.gIteration01(eigenAction, qr)
    elif(action == 2):
       	for x in range(L):
       	    eigenAction, qr = GI.gIteration10(eigenAction, qr)
    elif(action == 3):
       	for x in range(L):
       	    eigenAction, qr = GI.gIteration11(eigenAction, qr)

    return eigenAction, qr

def remember(eigenState, Q_program, quantumRegister, classicRegister, quantumCircuit, stateValue, done):
    memory[eigenState].append([Q_program, quantumRegister, classicRegister, quantumCircuit, stateValue, done])

    ### determines the action to make, collapses/measures the eigenAction into a move to make
def collapseActionSelectionMethod(Q_program, eigenAction, qr, cr):
    eigenAction.measure(qr, cr)
    result = Q_program.execute(["superposition"], backend='local_qasm_simulator', shots=1)
    classical_state = result.get_data("superposition")['classical_state']

    return classical_state

def q_learning(env, num_episodes, discount_factor=0.9, alpha=0.8):#, epsilon=0.1):
    """
    Q-Learning algorithm: Off-policy TD control. Finds the optimal greedy policy
    while following an epsilon-greedy policy
    
    Args:
        env: OpenAI environment.
        num_episodes: Number of episodes to run for.
        discount_factor: Gamma discount factor.
        alpha: TD learning rate.
        epsilon: Chance the sample a random action. Float betwen 0 and 1.
    
    Returns:
        A tuple (Q, episode_lengths).
        Q is the optimal action-value function, a dictionary mapping state -> action values.
        stats is an EpisodeStats object with two numpy arrays for episode_lengths and episode_rewards.
    """
    
    # The final action-value function.
    # A nested dictionary that maps state -> (action -> action-value).
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    memory = defaultdict(list)

    # Keeps track of useful statistics
    stats = plotting.EpisodeStats(
        episode_lengths=np.zeros(num_episodes),
        episode_rewards=np.zeros(num_episodes))    
    
    # The policy we're following
    #policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)
    
    for i_episode in range(num_episodes):
        # Print out which episode we're on, useful for debugging.
        #print("Episode ", i_episode)
        if (i_episode + 1) % 100 == 0:
            print("\rEpisode {}/{}.".format(i_episode + 1, num_episodes), end="")
            #sys.stdout.flush()
        
        # Reset the environment and pick the first action
        eigenState = env.reset()

        # One step in the environment
        # total_reward = 0.0
        for t in itertools.count():
            if eigenState in memory:
                memList = memory[eigenState]
                action = memList[0]
                stateValue = memList[1]
                nextState = memList[2]

                if nextState in memory:
                    nextStateValue = memory[nextState][1]
                else:
                    nextStateValue = 0.0
                reward = memList[3]

                Q_program = QuantumProgram()
                qr = Q_program.create_quantum_register("qr", 2)
                cr = Q_program.create_classical_register("cr", 2)
                eigenAction = Q_program.create_circuit("superposition", [qr], [cr])
                eigenAction.h(qr)
                eigenAction, qr = groverIteration(Q_program, eigenAction, qr, action, reward, nextStateValue)

            else:
                #################### Prepare the n-qubit registers #########################################
                Q_program = QuantumProgram() 
                qr = Q_program.create_quantum_register("qr", 2)
                cr = Q_program.create_classical_register("cr", 2)
                eigenAction = Q_program.create_circuit("superposition", [qr], [cr])
                eigenAction.h(qr)
                ############################################################################################

                stateValue = 0.0

            action = collapseActionSelectionMethod(Q_program, eigenAction, qr, cr)
            nextEigenState, reward, done, _ = env.step(action)
            #if done:
            #    print(reward)
            #reward += 1

            if nextEigenState in memory:
                memList = memory[nextEigenState]
                nextStateValue = memList[1]
            else:
                nextStateValue = 0.0

            #Update state value
            stateValue = stateValue + alpha*(reward + (discount_factor * nextStateValue) - stateValue)

            memory[eigenState] = (action, stateValue, nextEigenState, reward)

            stats.episode_rewards[i_episode] += (discount_factor ** t) * reward
            stats.episode_lengths[i_episode] = t
            
            if done:
                break
                
            eigenState = nextEigenState
    
    return Q, stats, memory


warnings.simplefilter("ignore", DeprecationWarning)

env = CliffWalkingEnv()

matplotlib.style.use('ggplot')
Q, stats, memory = q_learning(env, 500)

for state in memory:
    print(memory[state])

plotting.plot_episode_stats(stats)