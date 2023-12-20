# Human Touch Super Novo Virtual Therapist Reverse Engineering

That's a mouthful of a title, but it's the best I could come up with. This is a project to reverse engineer the Human Touch Virtual Therapist bridge that connects the Super Novo chair to the Virtual Therapist service. The goal is to be able to control the chair without the need for the bridge, and to be able to use the chair with other services.

## Background

I've had a Super Novo for a while now, and been through a couple of these bridges that have failed on me. After being sent a 3rd bridge, I decided to take a look at what was going on inside. It's seriously just a Raspberry Pi Zero W with a stock case and a mostly stock Raspbian SD card image. The only odd files I could find were in the pi user home directory, which I have compiled in this repository.

## Current Status

At this point, I think that most of what I would need to recreate the functionality is located in the NovoBluetoothCommands.py file. I have not tested anything at this time.
