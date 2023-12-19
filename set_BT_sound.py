#!/usr/bin/python

filepath = '/home/pi/chosenBlueTooth.txt'
writeTo = '/etc/shairport-sync.conf'
scriptOut = '/home/pi/BT_pair.sh'
myInfo = []
shouldWrite = True
script = ""

with open(filepath, 'r+') as aFile:
    myInfo = aFile.readlines()

if len(myInfo) == 1 and shouldWrite:
    with open(writeTo, 'w') as aTarget:
        ssid = myInfo[0]

        script = r"""#!/bin/bash

coproc bluetoothctl
echo -e 'scan on\n' >&${COPROC[1]}
sleep 3

echo -e 'pair """
        script = script + ssid + r"""' >&${COPROC[1]}
sleep 1

echo -e 'trust """
        script = script + ssid + r"""' >&${COPROC[1]}
sleep 1

echo -e 'connect """
        script = script + ssid + r"""' >&${COPROC[1]}
sleep 1

echo -e 'scan off\n' >&${COPROC[1]}
echo -e 'exit\n' >&${COPROC[1]}

output=$(cat <&${COPROC[0]})"""

        writeMe = r"""// Sample Configuration File for Shairport Sync
// Commented out settings are generally the defaults, except where noted.

// General Settings
general =
{
	name = "Novo Audio";
  audio_backend_buffer_desired_length_in_seconds = 1.35; // If set too small, buffer underflow occurs on low-powered machines. Too long and the response time to volume changes becomes annoying. Default is 0.15 seconds in the alsa backend, 0.35 seconds in the pa backend and 1.0 seconds otherwise.

};

// Advanced parameters for controlling how Shairport Sync runs a play session
sessioncontrol = 
{

};

// Back End Settings

// These are parameters for the "alsa" audio back end.
alsa =
{

  output_device = "bluealsa:HCI=hci0,DEV="""

        secondHalf = r""",PROFILE=a2dp"; 

};

// Parameters for the "sndio" audio back end. All are optional.
sndio =
{

};

// Parameters for the "pa" PulseAudio  backend.
pa =
{

};

// Parameters for the "pipe" audio back end, a back end that directs raw CD-style audio output to a pipe. No interpolation is done.
pipe =
{
//  name = "/path/to/pipe"; // there is no default pipe name for the output
};



dsp =
{

  loudness = "yes";                     // Activate the filter
//  loudness_reference_volume_db = -20.0; // Above this level the filter will have no effect anymore. Below this level it will gradually boost the low frequencies.

};

// How to deal with metadata, including artwork
metadata =
{

};

// Diagnostic settings. These are for diagnostic and debugging only. Normally you sould leave them commented out
diagnostics =
{

};
"""
        writeMe = writeMe + ssid + secondHalf

        aTarget.write(writeMe)

with open(scriptOut, 'w') as my_script:
    my_script.write(script)
    pass
