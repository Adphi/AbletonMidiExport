'''
Class Note

    pitch
    time
    duration
    velocity
    isEnable
'''


class Note:
    def __init__(self, pitch, time, duration, velocity, isEnable):
        self.pitch = int(pitch)
        self.start = float(time)
        self.duration = float(duration)
        self.velocity = int(float(velocity))
        self.isEnable = isEnable

    def __repr__(self):
        return '\npitch: ' + str(self.pitch) + ' time: ' + str(self.start) + ' duration: ' + str(self.duration) \
               + ' velocity: '+ str(self.velocity)+ ' isEnable: '+ str(self.isEnable)



