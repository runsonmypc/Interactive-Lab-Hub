#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "zero oh one two three four five six seven eight nine [unk]")

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        break
        print(rec.Result())
        raw_result = str(rec.Result())
    else:
        print(rec.PartialResult())

final_result = str(rec.FinalResult())
print(final_result)
jsonDict = json.loads(final_result)
parsed_text = jsonDict['text']
print("Parsed text:", parsed_text)

file = open('result.txt', 'w')
file.write(parsed_text + '\n')
file.close()
