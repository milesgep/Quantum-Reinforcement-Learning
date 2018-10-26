import random
import gym
import math
import numpy as np
from collections import deque
from collections import defaultdict
from qiskit import QuantumProgram

import warnings

import groverIteration as GI

class QuantumSpaceShipSolver():
    def __init__(self, n_episodes=1000, n_win_ticks=195, max_env_steps=None, quiet=False, alpha=0.4, alpha_decay=0.0, discount_factor = 0.5):
        #self.memory = deque(maxlen=100000)
        self.memory = defaultdict(list)
        self.env = gym.make('LunarLander-v2')
        self.n_episodes = n_episodes
        self.n_win_ticks = n_win_ticks # carried over from example
        self.quiet = quiet # carried over from example
        self.alpha = alpha # carried over from example
        self.alpha_decay = alpha_decay # carried over from example
        self.discount_factor = discount_factor
        if max_env_steps is not None: self.env._max_episode_steps = max_env_steps # carried over from example

    def remember(self, eigenState, action, stateValue, nextEigenState, reward):
        self.memory[eigenState] = (action, stateValue, nextEigenState, reward)

    ### determines the action to make, collapses/measures the eigenAction into a move to make
    def collapseActionSelectionMethod(self, Q_program, eigenAction, qr, cr):
        eigenAction.measure(qr, cr)
        result = Q_program.execute(["superposition"], backend='local_qasm_simulator', shots=1)
        classical_state = result.get_data("superposition")['classical_state']

        return classical_state

    ### will determine L -> how many times the eigenAction need to be amplified according to the reward and the next eigenState
    def groverIteration(self, Q_program, eigenAction, qr, action, reward, nextStateValue):
        L = int(0.2*(reward+nextStateValue)) #reward + value of the nextState, k is .3 which is arbitrary
        if(L > 1):
            L = 1

        if L < 1:
            return eigenAction, qr

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

    def run(self):
        scores = deque(maxlen=100)

        for e in range(self.n_episodes):
            eigenState = self.env.reset()          
            done = False
            i = 0
            eigenState = repr(np.round(eigenState, decimals=0))
            while not done:
                #self.env.render()
                if eigenState in self.memory:
                    memList = self.memory[eigenState]
                    action = memList[0]
                    stateValue = memList[1]
                    nextState = memList[2]

                    if nextState in self.memory:
                        nextStateValue = self.memory[nextState][1]
                    else:
                        nextStateValue = 1.0
                    reward = memList[3]

                    Q_program = QuantumProgram()
                    qr = Q_program.create_quantum_register("qr", 2)
                    cr = Q_program.create_classical_register("cr", 2)
                    eigenAction = Q_program.create_circuit("superposition", [qr], [cr])
                    eigenAction.h(qr)
                    eigenAction, qr = self.groverIteration(Q_program, eigenAction, qr, action, reward, nextStateValue)

                else:
                    #################### Prepare the n-qubit registers #########################################
                    Q_program = QuantumProgram() 
                    qr = Q_program.create_quantum_register("qr", 2)
                    cr = Q_program.create_classical_register("cr", 2)
                    eigenAction = Q_program.create_circuit("superposition", [qr], [cr])
                    eigenAction.h(qr)
                    ############################################################################################

                    stateValue = 0.0


                action = self.collapseActionSelectionMethod(Q_program, eigenAction, qr, cr)

                nextEigenState, reward, done, _ = self.env.step(action)
                if done:
                    print(reward)

                nextEigenState = repr(np.round(nextEigenState, decimals=0))


                if nextEigenState in self.memory:
                    memList = self.memory[nextEigenState]
                    nextStateValue = memList[1]
                else:
                    nextStateValue = 0.0

                #Update state value
                stateValue = stateValue + self.alpha*(reward + (self.discount_factor * nextStateValue) - stateValue)

                self.remember(eigenState, action, stateValue, nextEigenState, reward)
                eigenState = nextEigenState
                i += 1

            scores.append(i)
            mean_score = np.mean(scores)
            if mean_score >= self.n_win_ticks and e >= 100:
                if not self.quiet: print('Ran {} episodes. Solved after {} trials ✔'.format(e, e - 100))
                return e - 100
            if e % 100 == 0 and not self.quiet:
                print('[Episode {}] - Mean survival time over last 100 episodes was {} ticks.'.format(e, mean_score))

        #Update alpha
        #self.alpha = self.alpha - self.alpha_decay
        
        if not self.quiet: print('Did not solve after {} episodes 😞'.format(e))
        return e


if __name__ == '__main__':

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    agent = QuantumSpaceShipSolver()
    agent.run()