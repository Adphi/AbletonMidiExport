'''
class Envelope


XML path :
    MidiClip/Envelopes/Envelope/ClipEnvelope/Automation/Events/FloatEvent (Time, Value)
                                        ''  /EnvelopeTartget(Value)

(CC1 : Value "21466"
Tests
1_____

        CC1 : 15845
        CC7 : 15851 (+6)
        CC11: 15855 (+10)
        CC64: 15908 (+63)
        PitchBend : 15842 (-3)

XML Path :
    LiveSet/Tracks/MidiTrack/DeviceChain/MainSequencer/MidiControllers/MidiControllerTargets.x (Id)

        ControllerTarget.0 -> PitchBend
        ControllerTarget.3 -> CC1
        etc.
            LockEnvelope Value 0 Shown
            LockEnvelope Value 1 Hidden

Map defined by Track

['Pitch Bend', 'Channel Pressure', 'Bank Select', 'Modulation', 'Breath', '(Controller)', 'Foot Pedal', 'Portamento Time', 'Data Entry', 'Volume', 'Balance', '(Controller)', 'Pan', 'Expression', 'Effect Control 1', 'Effect Control 2', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', 'Hold Pedal', 'Portamento On/Off', 'Sostenuto Pedal', 'Soft Pedal', 'Legato Pedal', 'Hold Pedal 2', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', 'Data Entry Increment', 'Data Entry Decrement', 'NRPN LSB', 'NRPN MSB', 'RPN LSB', 'RPN MSB', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)', '(Controller)']

'''

class Envelope:
    def __init__(self, targetId=None, targetName=None, events=None):
        self.targetId = targetId
        self.targetName = targetName
        self.events = events

    def __repr__(self):
        return 'Envelope : targetName:{}, targetId:{} \nevents:{}'.format(self.targetName, self.targetId, self.events)

class Event:
    def __init__(self, time, value, ccX, ccY, previousEvent=None):
        self.time = time
        self.value = value
        self.ccX = ccX
        self.ccY = ccY
        self.getEventType(previousEvent)



    def __repr__(self):
    #    if self.type is not 'bCurve':
    #        return 'type:{}, time:{}, value:{}'.format(self.type, self.time, self.value)
    #    else:
        return '\ntype:{}, time:{}, value:{}, ccX:{}, ccY:{}'.format(self.type, self.time, self.value, self.ccX, self.ccY)

    def getEventType(self, previousEvent=None):
        self.type =None
        if self.ccX is not None and self.ccY is not None:
            self.type = 'bCurve'
        elif self.ccX is not None and self.ccY is not None and previousEvent.time != self.time and previousEvent.value != self.value:
            self.type = 'affine & bCurve'
        elif previousEvent is not None and previousEvent.time == self.time:
            self.type = 'break'
        elif previousEvent is not None and previousEvent.time != self.time and previousEvent.value != self.value and self.ccX is None \
                and self.ccY is None and previousEvent.ccX is None and previousEvent.ccY is None:
            self.type = 'affine'
        elif previousEvent is not None and previousEvent.time != self.time and self.ccX is None and self.ccY is None \
                and previousEvent.ccX is not None and previousEvent.ccY is not None and self.type is None:
            self.type = 'EndCurve'
        elif previousEvent is None:
            self.type = 'init'
