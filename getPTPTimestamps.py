import pyshark
from pyshark.packet.fields import LayerFieldsContainer

cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')
cap.sniff(timeout=5)
for pak in cap.sniff_continuously(packet_count=200):
    if 'PTP' in pak:

        if hasattr(pak.ptp, 'v2_sdr_origintimestamp_seconds'):
            print(pak.ptp.v2_sdr_origintimestamp_seconds)
