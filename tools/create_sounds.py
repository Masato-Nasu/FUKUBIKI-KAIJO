"""Original short prize cues. No television or commercial music recordings."""
from pathlib import Path
import wave
import numpy as np
from scipy.signal import butter,sosfilt
SR=44100
OUT=Path(__file__).resolve().parents[1]/'audio'
RNG=np.random.default_rng(20261017)
def env(t,d,attack=.015,release=.09):return np.minimum(t/attack,1)*np.clip((d-t)/release,0,1)
def voice(freq,d,kind):
 t=np.arange(int(d*SR))/SR
 if kind=='brass':
  phase=2*np.pi*freq*(t+.0025/6*np.sin(2*np.pi*6*t));s=np.zeros(len(t))
  for n in range(1,17):
   if freq*n>10000:break
   form=.25+np.exp(-((freq*n-1200)/1200)**2)
   s+=np.sin(n*phase)*(n**-1.25)*form
  s=np.tanh(s*1.15)*env(t,d,.025,.12);s=sosfilt(butter(2,4500,fs=SR,output='sos'),s)
 elif kind=='piano':
  s=sum(np.sin(2*np.pi*freq*n*np.sqrt(1+.00012*n*n)*t)*np.exp(-t/(1.1/n**.42))/(n**1.8)for n in range(1,11)if freq*n<12000)
  s*=1-np.exp(-t/.004);s*=np.minimum((d-t)/.15,1)
 elif kind=='marimba':
  s=sum(a*np.sin(2*np.pi*freq*r*t)*np.exp(-t/tau)for r,a,tau in [(1,1,.30),(4,.10,.095),(10,.015,.035)]if freq*r<15000);s*=1-np.exp(-t/.002)
 elif kind=='retro':
  s=sum(np.sin(2*np.pi*freq*n*t)/n**1.25 for n in range(1,14,2)if freq*n<10000)*env(t,d,.004,.035)*np.exp(-t*.9)
 elif kind=='drum':
  phase=2*np.pi*(freq*t+freq*.8*.045*(1-np.exp(-t/.045)))
  body=np.sin(phase)*np.exp(-t/.24)+.24*np.sin(phase*1.58)*np.exp(-t/.1)
  noise=sosfilt(butter(2,[150,2400],fs=SR,btype='bandpass',output='sos'),RNG.standard_normal(len(t)))*np.exp(-t/.025)
  s=(body+noise*.22)*(1-np.exp(-t/.001))
 else:raise ValueError(kind)
 return s

def render(name,events,duration):
 a=np.zeros((int(duration*SR),2))
 for at,freq,d,kind,level,pan in events:
  s=voice(freq,d,kind)*level;i=round(at*SR);n=min(len(s),len(a)-i)
  if n<=0:continue
  a[i:i+n,0]+=s[:n]*np.sqrt((1-pan)/2);a[i:i+n,1]+=s[:n]*np.sqrt((1+pan)/2)
 # Small room reflections soften the dry oscillators without washing out the melody.
 dry=a.copy()
 for delay,gain in [(.043,.12),(.079,.075),(.127,.045)]:
  n=round(delay*SR);a[n:]+=dry[:-n,::-1]*gain
 a=sosfilt(butter(2,7500,fs=SR,output='sos'),a,axis=0)
 rms=np.sqrt(np.mean(a*a));a*=min(.115/max(rms,1e-8),.72/max(abs(a).max(),1e-8));a=np.tanh(a*1.05)/1.05
 n=int(.10*SR);a[-n:]*=np.linspace(1,0,n)[:,None]
 with wave.open(str(OUT/name),'wb')as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((a*32767).astype('<i2').tobytes())
def event(t,f,d,k='brass',v=1,p=0):return(t,f,d,k,v,p)
C,E,G,C2,E2,G2=523.25,659.25,783.99,1046.5,1318.51,1567.98
brass=[event(0,C,.15),event(.18,C,.15),event(.38,G,.25),event(.67,C2,.8)]
brass +=[event(.67,f,.8,'brass',.45,p)for f,p in [(C,-.4),(E,.15),(G,.4)]]
render('trumpet-win.wav',brass,2.0)
grand=[event(i*.16,f,.22,'brass',.9,(i%3-1)*.3)for i,f in enumerate([C,C,G,C2,E2])]
grand +=[event(1.0,f,1.35,'brass',v,p)for f,v,p in [(C,.5,-.5),(E,.5,-.2),(G,.5,.2),(C2,.8,.45)]]
grand +=[event(.85,72,.7,'drum',.55,0)]
render('trumpet-grand.wav',grand,3.1)
piano=[event(i*.14,f,1.5,'piano',.9,(i-2)*.15)for i,f in enumerate([C,E,G,C2,E2])]+[event(.92,f,1.5,'piano',.55,p)for f,p in [(C,-.35),(E,0),(G,.35)]]
render('piano-win.wav',piano,2.8)
render('marimba-win.wav',[event(i*.13,f,.8,'marimba',.9,(i-2)*.15)for i,f in enumerate([C,E,G,C2,G,C2])],1.7)
render('taiko-win.wav',[event(t,f,.7,'drum',v,p)for t,f,v,p in [(0,82,.8,-.3),(.23,110,.65,.3),(.43,110,.65,-.2),(.66,66,1,0),(1.1,55,.9,0)]],2.1)
render('retro-win.wav',[event(i*.11,f,.18 if i<5 else .55,'retro',.75,0)for i,f in enumerate([C,E,G,C2,E2,C2])],1.5)
