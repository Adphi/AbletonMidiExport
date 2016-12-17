'''
Class Clip
    currentStart
    currentEnd
    loopStart
    loopEnd
    loopOn
    outMarker
    Name
    colorIndex
    timeSignature
    grid


    Color Index :
    0 - 59

'''
from Note import Note
from Envelope import *

class MidiClip:
    def __init__(self, track, XMLClip):
        self.XMLClip = XMLClip
        self.track = track
        self.startTime = float(XMLClip.get('Time'))
        self.lomId = int(XMLClip.find('LomId').get('Value'))
        self.name = XMLClip.find('Name').get('Value')
        self.colorIndex = int(XMLClip.find('ColorIndex').get('Value'))
        self.start = float(XMLClip.find('CurrentStart').get('Value'))
        self.end = float(XMLClip.find('CurrentEnd').get('Value'))
        self.loopStart = float(XMLClip.find('Loop/LoopStart').get('Value'))
        self.loopEnd = float(XMLClip.find('Loop/LoopEnd').get('Value'))
        self.startRelative = float(XMLClip.find('Loop/StartRelative').get('Value'))
        self.loop = True if (XMLClip.find('Loop/LoopOn').get('Value')) == 'true' else False
        self.timeSignatureNumerator = int(XMLClip.find('TimeSignature/TimeSignatures/RemoteableTimeSignature/Numerator').get('Value'))

        self.notes = self.parseNotes(XMLClip)
        self.envelopes = self.parseEnvelopes(XMLClip)
        #print (self.envelopes)

    def __repr__(self):
        return "Clip Name: {}\nStart Time: {}\n{}".format(self.name, self.startTime, self.notes)

    def parseNotes(self, XMLClip):
        clipNotes = []
        pitchs = XMLClip.findall('Notes/KeyTracks/KeyTrack')
        for p in pitchs:
            pitch = p.find('MidiKey').get('Value')
            notes = p.findall('Notes/MidiNoteEvent')
            for n in notes:
                time = n.get("Time")
                duration = n.get("Duration")
                velocity = n.get("Velocity")
                isEnable = n.get("IsEnabled")
                note = Note(pitch, time, duration, velocity, isEnable)
                clipNotes.append(note)
        '''
        for n in clipNotes:
            print n
        '''
        return clipNotes

    def parseEnvelopes(self, XMLClip):
        #print('init parse Envelopes')
        clipEnvelopes = []
        envelopes = XMLClip.findall('Envelopes/Envelopes/ClipEnvelope')
        for envelope in envelopes:
            if envelope is not None:
                #print('envelope found')
                target = int(envelope.find('EnvelopeTarget/PointeeId').get('Value'))
                targetName = self.track.MidiControllersMap[target]
                floatEvents = []
                events = envelope.findall('Automation/Events/FloatEvent')
                for event in events:
                    time = float(event.get('Time'))
                    value = float(event.get('Value'))
                    ccX = float(event.get('CurveControl1X')) if event.get('CurveControl1X') else None
                    ccY = float(event.get('CurveControl1Y')) if event.get('CurveControl1Y') else None
                    count = len(floatEvents)
                    if count != 0:
                        e = Event(time, value, ccX, ccY, floatEvents[count-1])
                    else :
                        e = Event(time, value, ccX, ccY)
                    floatEvents.append(e)
                clipEnvelopes.append(Envelope(target, targetName, floatEvents))

        return clipEnvelopes
