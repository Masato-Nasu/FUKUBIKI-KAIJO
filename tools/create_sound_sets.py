"""Five coherent original sound themes, each with four award tiers."""
from create_sounds import render,event,C,E,G,C2,E2,SR,OUT
import create_sounds as base
import numpy as np
original=base.voice
def voice(freq,d,kind):
 if kind=='bell':
  t=np.arange(int(d*SR))/SR
  s=sum(a*np.sin(2*np.pi*freq*r*t)*np.exp(-t/tau)for r,a,tau in [(1,1,.45),(2,.25,.22),(2.76,.10,.12)])
  return s*(1-np.exp(-t/.001))*np.minimum(np.maximum(d-t,0)/.06,1)
 return original(freq,d,kind)
base.voice=voice
for theme,kind in [('bell','bell'),('brass','brass'),('piano','piano'),('festival','marimba'),('retro','retro')]:
 for tier in ['grand','win','small','lose']:
  notes={'grand':[C,E,G,C2,E2,C2],'win':[C,E,G,C2],'small':[E,G,C2],'lose':[G,E]}[tier]
  step={'grand':.15,'win':.17,'small':.14,'lose':.14}[tier]
  tail={'grand':1.0,'win':.65,'small':.40,'lose':.22}[tier]
  events=[event(i*step,f,tail if i==len(notes)-1 else .24,kind,.85,(i%3-1)*.18)for i,f in enumerate(notes)]
  if tier=='grand':events +=[event((len(notes)-1)*step,f,tail,kind,.30,p)for f,p in [(C,-.35),(E,0),(G,.35)]]
  if theme=='festival':events +=[event(i*step,85 if i%2 else 65,.35,'drum',.35,0)for i in range(len(notes))]
  render('set-'+theme+'-'+tier+'.wav',events,(len(notes)-1)*step+tail+.2)
