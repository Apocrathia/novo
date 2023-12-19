import bluetooth
import sys

try:
    nearby_devices = bluetooth.discover_devices(lookup_names=True, flush_cache = True)
    print str(nearby_devices)
    sys.stdout.flush()
except Exception as e:
    print >>sys.stderr, "Error scanning for bluetooth devices", e
