reward: float = .01
punishment: float = .001
falloff: float = 0.0

def set_reward(new_reward):
    global reward
    reward = float(new_reward)

def set_punishment(new_punishment):
    global punishment
    punishment = float(new_punishment)

def set_falloff(new_falloff):
    global falloff
    falloff = float(new_falloff)

def get_reward():
    return str(reward)

def get_punishment():
    return str(punishment)

def get_falloff():
    return str(falloff)