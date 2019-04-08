from nltk.corpus import brown
from matplotlib import pylab
import os
import sys
import segeval
import decimal
#
from texttiling import TextTilingTokenizer

text_dir = sys.argv[1]
annotation_dir = sys.argv[2]
min_ocr = float(sys.argv[3])
def readAnnotations(f):
    idxs = []
    types = []
    i = 0
    ocr = -10
    for l in open(f):
        i+=1
        if i==1:
            ls = l.strip().split("\t")
            ocr = float(ls[1])
            continue
        if len(l.strip())==0:
            continue
        ls = l.strip().split("\t")
        idxs.append(int(ls[0]))
        types.append(ls[1])
    return [idxs,types,ocr]


def getTextTilingBoundaries(f):
    text = open(f).read()
    #print(f)
    #print(len(text.split("\n")))
    l = len(text.split("\n"))
    if l<=20:
        return [[1],[l],l+1]
    tt = TextTilingTokenizer()
    ts,segs = (tt.tokenize(text))
    idxs = []
    c = 1
    prev = c
    idxs.append(c)
    segs = []
    for t in ts: #(1,10):
        nex = len(t.split("\n"))
        c +=nex-1
        idxs.append(c)
        segs.append(c-prev)
        prev = c
        #print(t)
        #print("##########################################################################")
    end = prev+1
    del idxs[-1] 
    segs[-1]+=1
    return [idxs,segs,end]
     #   print(t)
     #   print("##########################################################################")

def convertFromIndex2Range(idx,end):
    arr = []
    c=1
    e = end
    for i in reversed(idx):
        arr.append(e-i)
        e = i
    return arr    


avg_prec = 0.0
avg_recall = 0.0
avg_wd = decimal.Decimal(0.0)
avg_pk = decimal.Decimal(0.0)

files = os.listdir(text_dir)
sel_files = 0
for f in files:
    #if not f =="sn83030214-1912-03-17-seq-32.txt" : #sn83030214-1912-03-03-seq-33.txt":
    #    continue
    if not f.endswith("txt"):
        continue
    af = os.path.join(annotation_dir,f)
    af = af.replace(".txt","-merged-merged.txt")
    if not os.path.exists(af):
        sys.stderr.write("Annotation does not exist: "+af+"\n")
        continue
    [anno_idx,anno_type,ocr] = readAnnotations(af)
    if ocr<min_ocr:
        continue
    sel_files+=1
    [anno_pred,anno_seg,anno_end] = getTextTilingBoundaries(os.path.join(text_dir,f))
    anno_idx2range = convertFromIndex2Range(anno_idx,anno_end)
    print("-----")
    print(anno_end)
    print(anno_idx2range)
    print(anno_seg)
    print("----")
    print(anno_pred)
    print(anno_idx)

    anno_pred = set(anno_pred)
    anno_idx = set(anno_idx)
    union = len(anno_pred.union(anno_idx))
    correct = len(anno_pred.intersection(anno_idx))
    precision = 1.0*correct/union
    recall = 1.0*correct/len(anno_idx)
    avg_prec += precision
    avg_recall += recall
    
    print("%s	%f	%f"%(f,precision,recall))
    wd = segeval.window_diff(anno_seg,anno_idx2range)
    pk = segeval.pk(anno_seg,anno_idx2range)
    avg_wd +=wd
    avg_pk +=pk
    print("WD:	%f	P-k:	%f"%(wd,pk))
print("Average:	%f	%f	WD:	%f	Pk:	%f	(%d)"%(avg_prec/(sel_files),avg_recall/(sel_files),avg_wd/decimal.Decimal(sel_files),avg_pk/decimal.Decimal(sel_files),(sel_files)))

