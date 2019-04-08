from nltk.corpus import brown
from matplotlib import pylab
import os
import sys
#
from texttiling import TextTilingTokenizer
#tt = TextTilingTokenizer(demo_mode=True)
#text = brown.raw()
#print (text)
#text = open("corpus_story/sn83030214-1912-03-24-seq-32.txt").read()
#text = text[:5000]

#text = brown.raw()[:10000]
#s, ss, d, b = tt.tokenize(text)
#print(b)
#print(s)
#print(d)
#print(ss)
#pylab.xlabel("Sentence Gap index")
#pylab.ylabel("Gap Scores")
#pylab.plot(range(len(s)), s, label="Gap Scores")
#pylab.plot(range(len(ss)), ss, label="Smoothed Gap scores")
#pylab.plot(range(len(d)), d, label="Depth scores")
#pylab.stem(range(len(b)), b)
#pylab.legend()
#pylab.show()
tt = TextTilingTokenizer()
input_dir = sys.argv[1]
output_dir = sys.argv[2]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
for f in os.listdir(input_dir):
    #if not f =="sn83030214-1912-03-03-seq-35.txt":
    #    continue
    if not f.endswith("txt"):
        continue
    print(f)
    text = open(os.path.join(input_dir,f),encoding="utf8").read()
    if len(text.split("\n"))<20:
        fw = open(os.path.join(output_dir,f),"w",encoding="utf8")
        fw.write(text)
        fw.close()
        continue
            
    ts,segs  = tt.tokenize(text)
    fw = open(os.path.join(output_dir,f),"w",encoding="utf8")
    i = 0
    idxs = []
    j = 0
    ks = 0
    pl = 1
    p = 0
    idxs = []
    for s in segs:
        ke = s
        l = (len(text[ks:ke].split("\n")))
        #print(text[ks:ke])
        pl +=l-1 
        idxs.append(pl)
        #print("112312312312313123123123123")
        ks = ke+1
        p+=1

    print(idxs)
    for t in ts: #(1,10):
        fw.write(t)
        fw.write("###########################################################\n")
        j+=1
    fw.close()
    fwa = open(os.path.join(output_dir,f+".anno"),"w",encoding="utf8")
    for i in idxs:
        fwa.write("%d\n"%(i))
    fwa.close()

