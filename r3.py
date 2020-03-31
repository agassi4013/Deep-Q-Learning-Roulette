import numpy as np
import random
from IPython.display import clear_output

import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Embedding, Reshape, LSTM, SimpleRNN
from tensorflow.keras.optimizers import Adam

rd = open('rawdata.txt', 'r')
rdata = rd.readlines()
rd.close()

game_num = []
game_color = []
for i in range(len(rdata)):
    k = ''.join([x for x in rdata[i] if x.isdigit()])
    k = int(k)
    if 'red' in rdata[i]:
        c = 'red'
    elif 'black' in rdata[i]:
        c = 'black'
    else:
        c = 'green'
    game_num.append(k)
    game_color.append(c)
#print(game_num[50],game_color[50])

def onetwo_react(act, step_num, bet):
    if game_num[step_num] == 0:
        return -bet
    elif act == 0:
        if game_num[step_num]>18:
            return bet
        else:
            return -bet
    elif act == 1:
        if game_num[step_num]<=18:
            return bet
        else:
            return -bet
    elif act == 2:
        if game_num[step_num]%2==1:
            return bet
        else:
            return -bet
    elif act == 3:
        if game_num[step_num]%2==0:
            return bet
        else:
            return -bet
    elif act == 4:
        if game_color[step_num]=='red':
            return bet
        else:
            return -bet
    elif act == 5:
        if game_color[step_num]=='black':
            return bet
        else:
            return -bet
    elif act == 6:
        return 0

def onethird_react(act, step_num, bet):
    if game_num[step_num] == 0:
        return -bet
    elif act == 0:
        if game_num[step_num]<13:
            return bet*2
        else:
            return -bet
    elif act == 1:
        if game_num[step_num]<25:
            return bet*2
        else:
            return -bet
    elif act == 2:
        if game_num[step_num]>=25:
            return bet*2
        else:
            return -bet
    elif act == 3:
        if game_num[step_num]%3==1:
            return bet*2
        else:
            return -bet
    elif act == 4:
        if game_num[step_num]%3==2:
            return bet*2
        else:
            return -bet
    elif act == 5:
        if game_num[step_num]%3==0:
            return bet*2
        else:
            return -bet
    elif act == 6:
        return 0

def single_react(act, step_num, bet):
    if act == game_num[step_num]:
        return bet*35
    elif act == 37:
        return 0
    else:
        return -bet

class HalfAgent:
    def __init__(self, optimizer):
        
        # Initialize atributes
        self._state_size = 1
        self._action_size = 7
        self._optimizer = optimizer
        
        # Initialize discount and exploration rate
        self.gamma = 0.6
        self.epsilon = 0.1
        
        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.alighn_target_model()
    #def store(self, state, action, reward, next_state, terminated):
    #    self.expirience_replay.append((state, action, reward, next_state, terminated))
        
    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())
        
    def _build_compile_model(self):
        model = Sequential()
        #model.add(LSTM(units = 40, input_shape = (20, 1),return_sequences=True))
        model.add(Embedding(observation_size, 40, input_length=20))
        model.add(SimpleRNN(40))
        #model.add(Reshape((40,)))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self._action_size, activation='linear'))
        
        model.compile(loss='mse', optimizer=self._optimizer)
        return model
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice(actions)
        
        q_values = self.q_network.predict(state)
        return np.argmax(q_values[0])
    def retrain(self, batch_size, reward, bet):
        minibatch = random.sample(game_num[:90000], batch_size+1)
        
        terminated = False
        
        r = reward
        
        for b in range(20, batch_size-1):
            state = np.array(minibatch[b:b+20]).reshape((1, 20))
            pred = self.q_network.predict(state)
            action = np.argmax(pred[0])
            r += onetwo_react(action, minibatch[b+20], bet)
            
            if r<-1000:
                terminated = True
            elif r>2000:
                terminated = True
            if b+20 == batch_size:
                terminated = True
            
            if terminated:
                pred[0][action] = r
            else:
                next_state = np.array(minibatch[b+1:b+21]).reshape((1, 20))
                t = self.target_network.predict(next_state)
                pred[0][action] = r + self.gamma * np.amax(t)
            
            self.q_network.fit(state, pred, epochs=1, verbose=0)
            
            if terminated:
                self.alighn_target_model()
                return r


class OneThirdAgent:
    def __init__(self, optimizer):
        
        # Initialize atributes
        self._state_size = 1
        self._action_size = 7
        self._optimizer = optimizer

        # Initialize discount and exploration rate
        self.gamma = 0.6
        self.epsilon = 0.1
        
        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.alighn_target_model()
    def store(self, state, action, reward, next_state, terminated):
        self.expirience_replay.append((state, action, reward, next_state, terminated))
        
    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())
        
    def _build_compile_model(self):
        model = Sequential()
        model.add(Embedding(observation_size, 40, input_length=20))
        model.add(SimpleRNN(40))
        #model.add(Reshape((40,)))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self._action_size, activation='linear'))
        
        model.compile(loss='mse', optimizer=self._optimizer)
        return model
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice(actions)
        
        q_values = self.q_network.predict(state)
        return np.argmax(q_values[0])
    def retrain(self, batch_size, reward, bet):
        minibatch = random.sample(game_num[:90000], batch_size+1)
        
        terminated = False
        
        r = reward
        
        for b in range(20, batch_size-1):
            state = np.array(minibatch[b:b+20]).reshape((1, 20))
            pred = self.q_network.predict(state)
            action = np.argmax(pred[0])
            r += onethird_react(action, minibatch[b+20], bet)
            
            if r<-1000:
                terminated = True
            elif r>2000:
                terminated = True
            if b+20 == batch_size:
                terminated = True
            
            if terminated:
                pred[0][action] = r
            else:
                next_state = np.array(minibatch[b+1:b+21]).reshape((1, 20))
                t = self.target_network.predict(next_state)
                pred[0][action] = r + self.gamma * np.amax(t)
            
            self.q_network.fit(state, pred, epochs=1, verbose=0)
            
            if terminated:
                self.alighn_target_model()
                return r

class SingleAgent:
    def __init__(self, optimizer):
        
        # Initialize atributes
        self._state_size = 1
        self._action_size = 38
        self._optimizer = optimizer
        
        # Initialize discount and exploration rate
        self.gamma = 0.6
        self.epsilon = 0.1
        
        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.alighn_target_model()
    def store(self, state, action, reward, next_state, terminated):
        self.expirience_replay.append((state, action, reward, next_state, terminated))
        
    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())
        
    def _build_compile_model(self):
        model = Sequential()
        model.add(Embedding(observation_size, 40, input_length=20))
        model.add(SimpleRNN(40))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self._action_size, activation='linear'))
        
        model.compile(loss='mse', optimizer=self._optimizer)
        return model
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice(actions)
        
        q_values = self.q_network.predict(state)
        return np.argmax(q_values[0])
    def retrain(self, batch_size, reward, bet):
        minibatch = random.sample(game_num[:90000], batch_size+1)
        
        terminated = False
        
        r = reward
        
        for b in range(20, batch_size-1):
            state = np.array(minibatch[b:b+20]).reshape((1, 20))
            pred = self.q_network.predict(state)
            action = np.argmax(pred[0])
            r += single_react(action, minibatch[b+20], bet)
            
            if r<-1000:
                terminated = True
            elif r>2000:
                terminated = True
            if b+20 == batch_size:
                terminated = True
            
            if terminated:
                pred[0][action] = r
            else:
                next_state = np.array(minibatch[b+1:b+21]).reshape((1, 20))
                t = self.target_network.predict(next_state)
                pred[0][action] = r + self.gamma * np.amax(t)
            
            self.q_network.fit(state, pred, epochs=1, verbose=0)
            
            if terminated:
                self.alighn_target_model()
                return r

actions = [x for x in range(37)]
optimizer = Adam(learning_rate=0.001)
observation_size = 37
agent1 = HalfAgent(optimizer)
agent2 = OneThirdAgent(optimizer)
agent3 = SingleAgent(optimizer)

#--------------------patch---------------------
agent1.q_network = tf.keras.models.load_model('save_models/onetwo_500.h5')
agent1.target_network = tf.keras.models.load_model('save_models/onetwo_500.h5')
agent2.q_network = tf.keras.models.load_model('save_models/onethird_500.h5')
agent2.target_network = tf.keras.models.load_model('save_models/onethird_500.h5')
agent3.q_network = tf.keras.models.load_model('save_models/single_500.h5')
agent3.target_network = tf.keras.models.load_model('save_models/single_500.h5')

batch_size = 100
num_of_episodes = 2000
timesteps_per_episode = 80

for e in range(1250, num_of_episodes):
    init_reward = 0
    bet = 50
    state = e*100
    
    reward1 = agent1.retrain(batch_size, init_reward, bet)
    reward2 = agent2.retrain(batch_size, init_reward, bet)
    reward3 = agent3.retrain(batch_size, init_reward, bet)
    if (e+1)%10==0:
        #print('Episode: ' + str(e+1) +' Reward: 1. ' + str(reward1) + ' 2. ' + str(reward2) + ' 3. ' + str(reward3)) 
        print('Episode: {} Reward: 1. {} 2. {} 3. {}'.format((e+1), reward1, reward2, reward3))
        
    if (e+1)%250==0:
        agent1.q_network.save('save_models/onetwo_{}.h5'.format(e+1))
        agent2.q_network.save('save_models/onethird_{}.h5'.format(e+1))
        agent3.q_network.save('save_models/single_{}.h5'.format(e+1))

agent1.q_network.save('save_models/onetwo_v1.h5')
agent2.q_network.save('save_models/onethird_v1.h5')
agent3.q_network.save('save_models/single_v1.h5')