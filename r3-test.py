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
        if game_num[step_num]<25 and game_num[step_num]>12:
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
        self.q_network = tf.keras.models.load_model('save_models/onetwo_1500.h5')
        self.target_network = tf.keras.models.load_model('save_models/onetwo_1500.h5')
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
        self.q_network = tf.keras.models.load_model('save_models/onethird_1500.h5')
        self.target_network = tf.keras.models.load_model('save_models/onethird_1500.h5')
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
        self.q_network = tf.keras.models.load_model('save_models/single_1500.h5')
        self.target_network = tf.keras.models.load_model('save_models/single_1500.h5')
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
#agent1.q_network = tf.keras.models.load_model('save_models/onetwo_1500.h5')
#agent1.target_network = tf.keras.models.load_model('save_models/onetwo_1500.h5')
#agent2.q_network = tf.keras.models.load_model('save_models/onethird_1500.h5')
#agent2.target_network = tf.keras.models.load_model('save_models/onethird_1500.h5')
#agent3.q_network = tf.keras.models.load_model('save_models/single_1500.h5')
#agent3.target_network = tf.keras.models.load_model('save_models/single_1500.h5')

batch_size = 100
num_of_episodes = 2000
timesteps_per_episode = 80

total_reward1 = 0
total_reward2 = 0
total_reward3 = 0

ag1_end = []
ag2_end = []
ag3_end = []

winlose1 = [0,0,0]
winlose2 = [0,0,0]
winlose3 = [0,0,0]

for e in range(100):
    init_reward = 0
    bet = 50
    state = 90000 + e*100
    
    test_state = game_num[state:state+100]
    
    r1 = init_reward
    r2 = init_reward
    r3 = init_reward
    
    terminated = False
    
    for b in range(batch_size-20): 
        b_state = np.array(test_state[b:b+20]).reshape((1, 20))
        p1 = agent1.target_network.predict(b_state)
        a1 = np.argmax(p1[0])
        r1 += onetwo_react(a1, test_state[b+20], bet)
        if r1<-1000:
            terminated = True
        elif r1>2000:
            terminated = True
        if b+20 == batch_size:
            terminated = True
        if terminated:
            break
    total_reward1 += r1
    ag1_end.append(b+1)
    if r1>0:
        winlose1[0]+=1
    elif r1<0:
        winlose1[1]+=1
    else:
        winlose1[2]+=1
    
    terminated = False
        
    for b in range(batch_size-20):     
        b_state = np.array(test_state[b:b+20]).reshape((1, 20))
        p2 = agent2.target_network.predict(b_state)
        a2 = np.argmax(p2[0])
        r2 += onethird_react(a2, test_state[b+20], bet)
        if r2<-1000:
            terminated = True
        elif r2>2000:
            terminated = True
        if b+20 == batch_size:
            terminated = True
        if terminated:
            break
    total_reward2 += r2
    ag2_end.append(b+1)
    if r2>0:
        winlose2[0]+=1
    elif r2<0:
        winlose2[1]+=1
    else:
        winlose2[2]+=1
    
    terminated = False
    
    for b in range(batch_size-20):    
        b_state = np.array(test_state[b:b+20]).reshape((1, 20))
        p3 = agent3.target_network.predict(b_state)
        a3 = np.argmax(p3[0])
        r3 += single_react(a3, test_state[b+20], bet)
        if r3<-1000:
            terminated = True
        elif r3>2000:
            terminated = True
        if b+20 == batch_size:
            terminated = True
        if terminated:
            break
    total_reward3 += r3
    ag3_end.append(b+1)
    if r3>0:
        winlose3[0]+=1
    elif r3<0:
        winlose3[1]+=1
    else:
        winlose3[2]+=1
        
    if (e+1)%10==0:
        print('Test round: {} Reward: 1. {} 2. {} 3. {}'.format((e+1), total_reward1, total_reward2, total_reward3))
    
res1 = [total_reward1, ag1_end, winlose1]
res2 = [total_reward2, ag2_end, winlose2]
res3 = [total_reward3, ag3_end, winlose3]

with open('res1.txt', 'w') as f:
    for item in res1:
        f.write("%s\n" % item)
        
with open('res2.txt', 'w') as f:
    for item in res2:
        f.write("%s\n" % item)
        
with open('res3.txt', 'w') as f:
    for item in res3:
        f.write("%s\n" % item)
        