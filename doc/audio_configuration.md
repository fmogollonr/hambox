# Detección de dispositivos de audio en Linux

Al ejecutar:
``` 
udevadm monitor --kernel --subsystem-match=sound
```

al conectar y desconectar el USB aparecerá algo parecido a:
```
/devices/pci0000:00/0000:00:1a.0/usb1/1-1/1-1.4/1-1.4:1.0/sound/card2
```

Con este dato editamos el fichero ```/lib/udev/rules.d/85-my-usb-audio.rules```

y creamos algo parecido a:
```

SUBSYSTEM!="sound", GOTO="my_usb_audio_end"
ACTION!="add", GOTO="my_usb_audio_end"

DEVPATH=="/devices/pci0000:00/0000:00:1a.0/usb1/1-1/1-1.4/1-1.4:1.0/sound/card?", ATTR{id}="audio_a"
DEVPATH=="/devices/pci0000:00/0000:00:1a.0/usb1/1-1/1-1.6/1-1.6:1.0/sound/card?", ATTR{id}="audio_b"

LABEL="my_usb_audio_end"

#
# For pulsaudio card naming (check with `pacmd list-sources`)
#
# This could go in a separate file if you want
SUBSYSTEM!="sound", GOTO="pa_naming_end"
ACTION!="change", GOTO="pa_naming_end"
KERNEL!="card*", GOTO="pa_naming_end"

# Same as before, edit this block at will.
DEVPATH=="/devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1.3/2-1.3.5/2-1.3.5:1.0/sound/card?", ENV{PULSE_NAME}="MyCard1"
DEVPATH=="/devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1.3/2-1.3.7/2-1.3.7:1.0/sound/card?", ENV{PULSE_NAME}="MyCard2"
DEVPATH=="/devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1.3/2-1.3.3/2-1.3.3:1.0/sound/card?", ENV{PULSE_NAME}="MyCard3"
DEVPATH=="/devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1.3/2-1.3.1/2-1.3.1.4/2-1.3.1.4:1.0/sound/card?", ENV{PULSE_NAME}="MyCard4"

LABEL="pa_naming_end"
```

donde definimos audio_a y audio_b para cada uno de los dispositivos que tengamos

Una vez hayamos reiniciado el equipo, cada vez que conectemos alguno de nuestros USB identificados anteriormente se establecerán los nombres "audio_a" y "audio_b" para cada uno de ellos.

Con eso podremos capturar un audio usando ALSA de la siguiente forma:
```
ffmpeg -f s16le -ar 44100 -ac 1 -f alsa -i hw:audio_b -t 30 out.wav -y
```
o
```
ffmpeg -f s16le -ar 44100 -ac 1 -f alsa -i hw:audio_b -f alsa -ac 2 hw:audio_b
```

es necesario establecer el formato y la frecuencia de muestro del audio de salida. Esto se puede averiguar con:
```
cat /proc/asound/audio_b/pcm0p/sub0/hw_params
```

En general con los dispositivos USB que estamos utilizando la configuración de audio siempre será la comentada anteriormente.


Dado que los dispositivos ALSA sólo pueden ser usados por un proceso a la vez, la forma más óptima de leer a la vez con varios dispositivos es usando PulseAudio:

```
ffmpeg -f s16le -ar 44100 -ac 1 -f pulse -i alsa_input.MyCard1.analog-mono output3.wav -y
```

Para detectar los nombres de los dispositivos se pueden usar los comandos:
```
$ pactl list short sources
$ pactl list short sinks
```


