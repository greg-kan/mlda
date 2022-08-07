import numpy as np
import matplotlib.pyplot as plt
import pygame
import gym

env = gym.make('FrozenLake-v1', is_slippery=False)

NUM_STATES = env.observation_space.n
NUM_ACTIONS = env.action_space.n

print('States: {}'.format(NUM_STATES))
print('Actions: {}'.format(NUM_ACTIONS))

lr = 0.8
gamma = 0.95

NUM_EPISODES = 3000
MAX_STEPS = 100
REWARD_AVERAGE_WINDOW = 20

Q = np.zeros([NUM_STATES, NUM_ACTIONS])

pathLenList = []
totalRewardList = []
totalRewardAverageList = []

for i in range(NUM_EPISODES):

    eps = 1.0 - float(i) / NUM_EPISODES

    s = env.reset()

    totalReward = 0
    step = 0

    while step < MAX_STEPS:
        step += 1

        if np.random.rand() < eps:
            a = env.action_space.sample()
        else:
            a = np.argmax(Q[s, :])

        s1, r, done, _ = env.step(a)

        # if r > 0:
        #     print(s, s1, a, r, done)

        if done:
            Q_target = r
        else:
            Q_target = r + gamma * np.max(Q[s1, :])

        Q[s, a] = (1 - lr) * Q[s, a] + lr * Q_target

        totalReward += r
        s = s1

        if done:
            break

    pathLenList.append(step)
    totalRewardList.append(totalReward)

    if i % REWARD_AVERAGE_WINDOW == 0 and i >= REWARD_AVERAGE_WINDOW:
        totalRewardAverage = np.mean(totalRewardList[-REWARD_AVERAGE_WINDOW:])
        totalRewardAverageList.append(totalRewardAverage)
        if i % 100 == 0:
            print('Episode {}: average total reward = {}'.format(i, totalRewardAverage))

print(Q)

plt.plot(pathLenList)
plt.grid()

plt.plot(totalRewardAverageList)
plt.grid()

USE_Q = True

s = env.reset()

for N in range(1000):
    env.render()
    if USE_Q:
        a = np.argmax(Q[s, :])
    else:
        a = env.action_space.sample()

    #     print('a = ', a)
    s, r, done, _ = env.step(a)
    #     print('s, r, done:', s, r, done)
    if done:
        env.render()
        print('Reward = {}'.format(r))
        break

env.close()
