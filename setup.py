from setuptools import setup

setup(name='hueMIDI',
      version='0.1',
      description='A MIDI Controller for Hue Lights',
      url='http://github.com/mattrigg9/huemidi',
      author='Matt Rigg',
      author_email='mriggery@gmail.com',
      license='MIT',
      packages=['hueMIDI'],
      install_requires=[
          'rtmidi_python',
          'phue',
          'yaml'
      ],
      zip_safe=False)