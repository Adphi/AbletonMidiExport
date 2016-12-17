from MidiFile import MIDIFile
from AutomationCurve import *

def getAutomationEvents(events):
    automationEvents = []
    count = 0
    quantize = 1/64
    for event in events:
        eventTime = event.time if event.time >= 0 else 0
        eventValue = event.value
        eventCCX = event.ccX
        eventCCY = event.ccY
        if event.type == 'init' or event.type == 'break' or event.type == 'EndCurve':
            automationEvents.append({'Time': eventTime, 'Value' : eventValue})

        elif event.type == 'affine':
            previousEvent = events[count - 1]
            points = affine(previousEvent.time, previousEvent.value, eventTime, eventValue, quantize)
            for p in points:
                automationEvents.append({'Time' : points[p]['Time'], 'Value' : points[p]['Value']})

        elif event.type == 'bCurve':
            nextEvent = events[count + 1]
            points = bCurve(eventTime, eventValue, nextEvent.time, nextEvent.value,
                            eventCCX, eventCCY, quantize)
            for p in points:
                automationEvents.append({'Time' : points[p]['Time'], 'Value' : points[p]['Value']})

        elif event.type == 'affine & bCurve':
            previousEvent = events[count - 1]
            points = affine(previousEvent.time, previousEvent.value, eventTime, eventValue, quantize)
            for p in points:
                automationEvents.append({'Time' : points[p]['Time'], 'Value' : points[p]['Value']})
            nextEvent = events[count + 1]
            points = bCurve(eventTime, eventValue, nextEvent.time, nextEvent.value,
                            eventCCX, eventCCY, quantize)
            for p in points:
                automationEvents.append({'Time' : points[p]['Time'], 'Value' : points[p]['Value']})

        count += 1

    return automationEvents


def midiExport(liveSet, midiFilePath, separateChannels=False):

    print('Init Midi Export')
    # How Many Midi Tracks in liveSet?
    usedMidiTrack = 0
    for track in liveSet.tracks:
        if len(track.notes) != 0:
            usedMidiTrack += 1
    #print ("Used Midi Track count:", usedMidiTrack)

    # Create the MIDIFile Object with 1 track
    MyMIDI = MIDIFile(len(liveSet.tracks), file_format=1, adjust_origin=True)

    i = 0
    for track in liveSet.tracks:
        # Tracks are numbered from zero. Times are measured in beats.
        if track.midiExport:    #len(track.notes) != 0 and
            trackId = i
            channel = i % 16 if separateChannels else 0
            time = 0

            # Add track name.
            name = str(track.name)
            MyMIDI.addTrackName(trackId, time, name)

            # Add tempo Map to first track.
            if trackId == 0:
                events = getAutomationEvents(liveSet.tempoMap)
                for event in events:
                    MyMIDI.addTempo(trackId, event['Time'], event['Value'])

            # Add Notes.
            for note in track.notes:
                pitch = note.pitch
                time = note.start
                duration = note.duration
                volume = note.velocity

                MyMIDI.addNote(trackId, channel, pitch, time, duration, volume)

            # Add Clip Automations to MidiTrack
            for clip in track.arrangementClips:
                for envelope in clip.envelopes:
                    events = getAutomationEvents(envelope.events)
                    target = envelope.targetName
                    for event in events:
                        time = event['Time'] + clip.startTime - clip.loopStart
                        value = int(event['Value'])
                        #print('time:{}, value:{}'.format(time, value))

                        if target == 'Pitch Bend':
                            MyMIDI.addPitchWheelEvent(trackId, channel, time, value)
                            print(time, value)
                        elif target == 'Channel Pressure':
                            MyMIDI.addChannelPressureEvent(trackId, channel, time, value)

                        # Prevent CC7(Volume) and CC10(Pan) Conflicts
                        elif int(target) != 7 and int(target)!= 10:
                            MyMIDI.addControllerEvent(trackId, channel, time, int(target), value)

                        if isinstance(target, int) and int(target) == 7 and not track.volumeMidiExport:
                            MyMIDI.addControllerEvent(trackId, channel, time, int(target), value)

                        if isinstance(target, int) and int(target) == 10 and not track.panMidiExport:
                            MyMIDI.addControllerEvent(trackId, channel, time, int(target), value)

            i += 1

            # Add Volume Automation to Track
            if track.volumeMidiExport:
                events = getAutomationEvents(track.volumeAutomationEvents)
                for event in events:
                    time = event['Time']
                    value = event['Value']

                    # Scale value [0, 1] to [0, 100] and [1, 2] and [100, 127]
                    if value <= 1:
                        value = int(value * 100)
                    else:
                        value = int(100 + value * 28/2)
                    #print('time:', time, 'value:', value)
                    MyMIDI.addControllerEvent(trackId, channel, time, 7, value)

            # Add Pan Automation to Track
            if track.panMidiExport:
                events = getAutomationEvents(track.panAutomationEvents)
                for event in events:
                    time = event['Time']
                    value = event['Value']
                    # Scale value [-1, 1] to [0, 127]
                    value = int((value + 1) * 64)
                    MyMIDI.addControllerEvent(trackId, channel, time, 10, value)

    # And write it to disk.
    binfile = open(midiFilePath, 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()
    print('Midi Export Done')


