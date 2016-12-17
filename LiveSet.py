from FileHandler import extract, compact
from lxml import etree as ET
from MidiTrack import *
from Envelope import *
import os


class LiveSet():
    def __init__(self,filePath, copy=False):
        self.filePath = filePath
        self.name = os.path.basename(self.filePath).replace('.als', '')
        print ("LiveSet", self.name)
        #'/Users/Philippe-Adrien/Desktop/ALS Decode/TralierShitRemake.als'
        self.infos = extract(str(filePath), copy)
        print ('Init LiveSet Parse')
        parser = ET.XMLParser(huge_tree=True)
        self.doc = ET.fromstring(self.infos, parser)

        self.tempo = int(self.doc.find("LiveSet/MasterTrack/DeviceChain/Mixer/Tempo").find('Manual').get('Value'))
        self.tempoMap = self.getTempoMap()
        self.tracks = self.parseTracks()
        #print (len(self.tracks), "Midi Tracks found")
        #print ('Tempo Map', self.tempoMap)
        print ('LiveSet Parse Done')

    def parseTracks(self):
        midiTracks =[]
        for midiTrack in self.doc.xpath("//MidiTrack"):
            track = MidiTrack(midiTrack)
            midiTracks.append(track)
        return midiTracks

    def getTempoMap(self):
        events = self.doc.findall("LiveSet/MasterTrack/DeviceChain/Mixer/Tempo/ArrangerAutomation/Events/FloatEvent")
        floatEvents = []
        for event in events:
            time = float(event.get('Time'))
            value = int(float(event.get('Value')))
            ccX = float(event.get('CurveControl1X')) if event.get('CurveControl1X') else None
            ccY = float(event.get('CurveControl1Y')) if event.get('CurveControl1Y') else None
            count = len(floatEvents)
            if count != 0:
                e = Event(time, value, ccX, ccY, floatEvents[count - 1])
            else:
                e = Event(time, value, ccX, ccY)
            floatEvents.append(e)

        return floatEvents

