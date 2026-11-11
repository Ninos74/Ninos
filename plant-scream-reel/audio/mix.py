#!/usr/bin/env python3
# Builds the full soundtrack: music bed + narration lines + screams, placed at film times.
import subprocess, sys
R='audio/raw/'; D=36.4
cues=[]  # (file, src_start, src_len or None, film_time, gain, extra filters)
def cue(f,ss,ln,at,gain,extra=''): cues.append((f,ss,ln,at,gain,extra))
# narration (vo1), one line each
vo=[(0,2.66,0.9),(3.08,1.74,6.4),(5.28,2.0,10.3),(7.72,1.65,14.6),(9.79,1.97,18.3),(12.12,2.21,23.9),(14.85,1.98,26.9),(17.26,2.46,29.6),(19.97,1.06,32.25),(21.51,1.24,33.9)]
for ss,ln,at in vo: cue(R+'vo1.mp3',ss,ln,at,1.85,'afade=t=in:d=0.02,afade=t=out:st=%.2f:d=0.04'%(ln-0.04))
P=lambda r:'asetrate=44100*%s,aresample=48000'%r
# shot 1: the first scream, then it carries on quietly under the question
cue(R+'scream4.mp3',0,0.85,0.08,0.95)
cue(R+'scream4.mp3',0.85,0.9,0.93,0.11,'afade=t=out:st=0.6:d=0.3')
cue(R+'scream3.mp3',0.3,2.1,1.65,0.06,'afade=t=in:d=0.2,afade=t=out:st=1.8:d=0.3')
# shot 2: the fern at 3:07, cut dead by the water
cue(R+'scream2.mp3',0,1.5,4.3,0.9,P(1.08))
cue(R+'scream3.mp3',2.0,0.72,5.63,0.85,'afade=t=in:d=0.05,afade=t=out:st=0.68:d=0.04')
# shot 3: four desk plants go off one by one, then keep going under the line
for i,(f,at,r) in enumerate([('scream1',8.85,1.0),('scream2',9.25,1.18),('scream4',9.55,0.9),('scream1',9.8,1.3)]):
    ln=10.22-at; cue(R+f+'.mp3',0,ln,at,0.6,P(r)+',afade=t=out:st=%.2f:d=0.12'%(ln-0.12))
cue('work/crowd.wav',0,2.9,9.95,0.06,'afade=t=in:d=0.3,afade=t=out:st=2.75:d=0.15')
# shot 4: the whole garden centre, then the push to the quiet one
cue('work/crowd.wav',0.5,1.5,12.9,0.75,'afade=t=out:st=1.1:d=0.4')
cue('work/crowd.wav',2.0,2.6,14.3,0.055,'afade=t=in:d=0.2,afade=t=out:st=2.5:d=0.1')
# shot 5: the lawn, the street, the planet
cue('work/crowd.wav',1.0,1.5,16.9,0.8,'afade=t=out:st=1.2:d=0.3')
cue('work/crowd.wav',2.5,2.0,18.3,0.055,'afade=t=in:d=0.2')
cue('work/crowd.wav',0.2,1.9,20.2,0.3,'highpass=f=900,lowpass=f=3500,afade=t=in:d=0.3,afade=t=out:st=1.6:d=0.3')
# shot 6: still screaming, rain, silence, relief
cue('work/crowd.wav',3.0,0.75,22.0,0.7,'afade=t=out:st=0.6:d=0.15')
cue('work/rain.wav',0,4.1,22.4,0.2,'afade=t=in:d=0.5,afade=t=out:st=3.6:d=0.5')
cue(R+'sigh1.mp3',0,0.92,22.98,0.9,'afade=t=out:st=0.7:d=0.22')
# shot 7: the clicks, the watering
for at in (29.1,29.9,30.8,31.7,32.6): cue('work/pop.wav',0,None,at,0.5)
cue('work/rain.wav',1.0,1.6,34.35,0.22,'highpass=f=1500,afade=t=in:d=0.2,afade=t=out:st=1.2:d=0.4')
ins=['-i','work/bed.wav']; fc=['[0:a]aresample=48000,volume=0.26,afade=t=out:st=35.2:d=1.2[b]']; lab=['[b]']
for i,(f,ss,ln,at,gain,extra) in enumerate(cues,1):
    ins+=['-i',f]; tr='atrim=start=%s'%ss+(':duration=%s'%ln if ln else '')+',asetpts=PTS-STARTPTS'
    ch=[tr,'aresample=48000','aformat=channel_layouts=stereo']+([extra] if extra else [])+['volume=%s'%gain,'adelay=%d:all=1'%round(at*1000)]
    fc.append('[%d:a]%s[c%d]'%(i,','.join(ch),i)); lab.append('[c%d]'%i)
fc.append(''.join(lab)+'amix=inputs=%d:normalize=0:duration=longest,atrim=duration=%s,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11[o]'%(len(lab),D))
subprocess.check_call(['ffmpeg','-y','-v','error',*ins,'-filter_complex',';'.join(fc),'-map','[o]','-ar','48000',sys.argv[1]])
