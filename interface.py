#!/usr/bin/python3

import tkinter as tk
from tkinter import Button
import argparse
import tempfile
import queue
import sys
import os
from threading import *

import sounddevice as sd
import soundfile as sf

import whisper
import openai

from gtts import gTTS

class GPTVoiceInterface:
	running = False

	def __init__(self):
		# audio stuff
		self.q = queue.Queue()
		self.device = 'default'
		device_info = sd.query_devices(self.device, 'input')
		self.samplerate = int(device_info['default_samplerate'])
		self.recordingfile = tempfile.mktemp(prefix='/tmp/tmp_recording', suffix='.wav', dir='')
		self.speechfile = tempfile.mktemp(prefix='/tmp/tmp_speech', suffix='.wav', dir='')
		self.channels = 1
		self.subtype = "PCM_24"

		# GUI stuff
		self.tk = tk.Tk()
		self.button_rec = Button(self.tk, text='Speak', command=self.record)
		self.button_rec.pack()
		self.button_stop = Button(self.tk, text='Done speaking', command=self.stop)
		self.button_stop.pack()

		# Speech recognition
		#self.model = whisper.load_model("base")
		self.model = whisper.load_model("tiny")

		# Speech to text
		self.language = 'en'

		# GPT3:
		openai.api_key = os.getenv("OPENAI_API_KEY")
		#print(openai.Model.list())


	# Record audio
	def recording_thread(self):
		with sf.SoundFile(self.recordingfile, mode='x', samplerate=self.samplerate, channels=self.channels, subtype=self.subtype) as file:
			with sd.InputStream(samplerate=self.samplerate, device=self.device, channels=self.channels, callback=self.callback):
				while self.running:
					file.write(self.q.get())

	def stop(self):
		if self.running:
			self.running = False
			self.recordingThread.join()
			text = self.speech_to_text()
			self.speak(text)
			os.remove(self.recordingfile)
			print("Recording stopped")
		else:
			print("Already stopped")

	def record(self):
		if self.running:
			print("Already running")
		else:
			self.running = True
			self.recordingThread = Thread(target=self.recording_thread)
			self.recordingThread.start()
			print("Started recording")

	def callback(self, indata, frames, time, status):
		self.q.put(indata.copy())

	# Speech to text
	def speech_to_text(self):
		audio = whisper.load_audio(self.recordingfile)
		audio = whisper.pad_or_trim(audio)
		mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
		options = whisper.DecodingOptions(fp16 = False)
		result = whisper.decode(self.model, mel, options)
		return result.text
	
	# Text to speech
	def speak(self, text):
		myobj = gTTS(text=text, lang=self.language, slow=False)
		myobj.save(self.speechfile)
		os.system("mplayer "+self.speechfile)
		os.remove(self.speechfile)
	
	# Send to GPT3
#self.apikey

	def run(self):
		self.tk.mainloop()

gpti = GPTVoiceInterface()
gpti.run()
