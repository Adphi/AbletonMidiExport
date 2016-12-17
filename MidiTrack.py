'''
Class MidiTrack

    name
    trackId
    trackColorIndex
    trackGroup
    trackUnfold
    midiFoldIn
    midiPrelisten
    Freeze
    Clips



    Color Indexs :
    140 - 199
'''

from Clip import *
from Note import *
from Envelope import *

class MidiTrack():
    def __init__(self, XMLTrack):
        self.XMLTrack = XMLTrack
        self.name = str(XMLTrack.find('Name/EffectiveName').get('Value'))
        self.id = int(XMLTrack.get('Id'))
        self.colorIndex = int(XMLTrack.find('ColorIndex').get('Value'))
        self.groupId = XMLTrack.find('TrackGroupId').get('Value')
        self.unfold = XMLTrack.find('TrackUnfolded').get('Value')
        self.midiFoldIn = XMLTrack.find('MidiFoldIn').get('Value')
        self.midiPrelisten = XMLTrack.find('MidiPrelisten').get('Value')
        self.freeze = XMLTrack.find('Freeze').get('Value')
        #self.sessionClips
        self.MidiControllersMap = self.mapControllers()
        self.arrangementClips = self.parseClips()
        self.notes = self.parseNotes()
        #print self.name
        #print self.notes

        # Midi Export Options
        self.midiExport = True
        self.volumeMidiExport = True
        self.panMidiExport = True

        # Track Mixer Parameters:
        self.volumeAutomationEvents = self.getAutomationEvents(XMLTrack.find('DeviceChain/Mixer/Volume')) #VolumePath
        self.panAutomationEvents = self.getAutomationEvents(XMLTrack.find('DeviceChain/Mixer/Pan'))  #PanPath

    def __repr__(self):
        return "MidiTrack Name: {}\n{}\n".format(self.name, self.arrangementClips)

    def parseClips(self):
        midiClips = []
        for midiClip in self.XMLTrack.findall('DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip'):
            if midiClip is not None:
                midiClips.append(MidiClip(self, midiClip))
        return midiClips

    def parseNotes(self):
        midiNotes = []
        for midiClip in self.arrangementClips:
            currentStart = midiClip.start
            currentEnd = midiClip.end
            loopStart = midiClip.loopStart
            loopEnd = midiClip.loopEnd
            startRelative = midiClip.startRelative
            length = currentEnd - currentStart
            loopLength = loopEnd - loopStart
            loop = midiClip.loop
            for note in midiClip.notes:
                start = currentStart + note.start - loopStart - startRelative
                if start >= currentStart and start < currentEnd:
                    n = Note(note.pitch, start, note.duration, note.velocity, note.isEnable)
                    midiNotes.append(n)
                    if loop and length > loopLength - startRelative and note.start >= loopStart and note.start < loopEnd:
                        #print('!clip is looping! Loop length:', loopLength)
                        while start < currentEnd:
                            #print('note Start:', start, 'end:', currentEnd)
                            n = Note(note.pitch, start, note.duration, note.velocity, note.isEnable)
                            midiNotes.append(n)
                            start += loopLength

                # case loop Note after start marker
                elif loop and note.start >= loopStart and note.start < loopEnd:
                    #print(note)
                    start = currentStart + note.start - loopStart - startRelative + loopLength
                    while start < currentEnd:
                        # print('note Start:', start, 'end:', currentEnd)
                        n = Note(note.pitch, start, note.duration, note.velocity, note.isEnable)
                        midiNotes.append(n)
                        start += loopLength

        return midiNotes

    def mapControllers(self):
        controllersMap = {}
        controllersNames = ["Pitch Bend", "Channel Pressure", "Bank Select", "Modulation","Breath","(Controller)",
                            "Foot Pedal","Portamento Time","Data Entry","Volume","Balance","(Controller)","Pan","Expression",
                            "Effect Control 1","Effect Control 2","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","Hold Pedal","Portamento On/Off","Sostenuto Pedal",
                            "Soft Pedal","Legato Pedal","Hold Pedal 2","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","Data Entry Increment","Data Entry Decrement",
                            "NRPN LSB","NRPN MSB","RPN LSB","RPN MSB","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)",
                            "(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)","(Controller)"]
        midiControllers = self.XMLTrack.find('DeviceChain/MainSequencer/MidiControllers')
        count = 0
        for midiController in midiControllers.iterchildren():
            if count < 2:
                name = controllersNames[count]
            else:
                name = count-2
            #print(self.name, name, midiController.tag, midiController.get('Id'))
            count += 1
            controllersMap[int(midiController.get('Id'))] = str(name)
        #print (controllersMap)
        return controllersMap

    def getAutomationEvents(self, XMLPathParameter):
        floatEvents = []
        events = XMLPathParameter.findall('ArrangerAutomation/Events/FloatEvent')
        for event in events:
            time = float(event.get('Time'))
            value = float(event.get('Value'))
            ccX = float(event.get('CurveControl1X')) if event.get('CurveControl1X') else None
            ccY = float(event.get('CurveControl1Y')) if event.get('CurveControl1Y') else None
            count = len(floatEvents)
            if count != 0:
                e = Event(time, value, ccX, ccY, floatEvents[count - 1])
            else:
                e = Event(time, value, ccX, ccY)
            floatEvents.append(e)
        return floatEvents