#!/usr/bin/python
import sys, select, random, yaml, os.path
import rtmidi_python as rtmidi
from phue import Bridge

BRIDGE_IP = '172.16.1.80'

def first_run():
	print("Welcome to hueMIDI!\n\n")
	light_names = bridge_handle.get_light_objects('name')

	light_dict = dict()
	for light in light_names:
		print "Press the MIDI key you want to turn on {}, or press Ctrl+C to skip.".format(light)
		key = listen_for_key()
		light_dict[key] = light
		#print "Assigned {} to key #{}!".format(light,key)

	print "Writing config file..."
	data = dict(
		light_map = light_dict
	)

	with open('hue_config.yml', 'w') as outfile:
		yaml.dump(data, outfile, default_flow_style=True)

	print("\n\n\nAll ready- Enjoy your hueMIDI setup!")

def listen_for_key():
	try:
		while True:
			message, delta_time = midi_handle.get_message()
			if message:
				if message[0] == 144:
					return message[1]
	except KeyboardInterrupt:
	    return None

def launch_poller(bridge_handle,midi_handle,light_map):
	light_names = bridge_handle.get_light_objects('name')

	print("Press any of your mapped MIDI keys to start a light show!")
	while True:
		message, delta_time = midi_handle.get_message()
		if message:
			#print message
			if message[0] == 144:
				#Key Press DOWN
				try:
					light = light_names[light_map[message[1]]]
					print "Turning on {}".format(light_map[message[1]])
					velocity = message[2]
					transitiontime = (delta_time*10)
					#light.xy = [random.random(),random.random()]
					light.transitiontime = transitiontime
					light.brightness = velocity+50
				except: 
					print "Not a light!"
			elif message[0] == 128:
				#Key Press Up
				try:
					light = light_names[light_map[message[1]]]
					print "Turning off " + light_map[message[1]]
					transitiontime = (delta_time*10)
					light.transitiontime = transitiontime
					light.brightness = 1
				except: 
					print "Not a light!"

if __name__ == "__main__":
	bridge_handle = Bridge(BRIDGE_IP)
	# If the app is not registered and the button is not pressed, press the button and run this script again
	bridge_handle.connect()

	midi_handle = rtmidi.MidiIn()
	midi_handle.open_port(0)

	if not(os.path.isfile('hue_config.yml')):
		first_run()

	with open("hue_config.yml", 'r') as stream:
		try:
			config = yaml.load(stream)
		except yaml.YAMLError as exc:
			print("Error loading configuration file: {}".format(exc))

	launch_poller(bridge_handle,midi_handle,config['light_map'])