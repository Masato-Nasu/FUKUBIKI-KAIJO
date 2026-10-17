"""Two original handbell strikes for winning prizes."""
from pathlib import Path
import wave
import numpy as np
sr=44100;t=np.arange(int(1.2*sr))/sr;s=np.zeros_like(t)
for at,gain in [(0,1),(.235,.9)]:
 u=np.maximum(t-at,0);ring=np.zeros_like(t)
 for f,a,decay in [(1046,1,.28),(1668,.5,.18),(2325,.27,.11),(3190,.12,.065)]:ring+=a*np.sin(2*np.pi*f*u)*np.exp(-u/decay)
 ring*=np.where(t>=at,1-np.exp(-u/.0007),0);s+=gain*ring
s*=.72/abs(s).max();s[-400:]*=np.linspace(1,0,400)
with wave.open(str(Path(__file__).resolve().parents[1]/'audio/winner-bell.wav'),'wb')as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((s*32767).astype('<i2').tobytes())
