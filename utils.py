import os
import sys
from enum import Enum

class ProcessFiles(Enum):
    FILE=1    # process & evaluate each file separately
    DAY=2    # process & evaluate each all files from one day
    ALL=3    # process & evaluate all files together

#Object to store text and annotation
class Instance:

    def readAnnotation(self,file_annotation,file_automatic_annotation=None):        
        i = 0
        for l in open(file_annotation):
            if len(l.strip())==0:
                continue
            ls = l.strip().split("\t")
            i+=1
            if i==1:
                self.ocr = float(ls[1])
                continue
            self.indices.append(int(ls[0]))
            self.labels.append(ls[1])     
        
        if file_automatic_annotation != None:
            self.autoseg = True
            self.autoindices.append(1)
            for l in open(file_automatic_annotation):
                self.autoindices.append(int(l.strip()))
    def readText(self,file_text):
        i = 0
        l = ""
        for l in open(file_text):
            self.text_lines.append(l.strip())
            
        self.text = open(file_text).read()
        
    def __init__(self,file_text=None,file_annotation=None,file_automatic_annotation= None, name = None):
        self.indices = []
        self.autoseg = False
        self.autoindices=[]
        self.file_automatic_annotation = file_automatic_annotation
        self.labels = []
        self.name = name
        self.file_text = file_text
        self.file_annotation = file_annotation
        self.ocr = -2
        self.text_lines = []
        self.text = ""
        if file_text !=None:
            self.readAnnotation(file_annotation,file_automatic_annotation)
        if file_annotation !=None:
            self.readText(file_text)
        
    # appends instance 2 to the current instance
    def append(self,instance2):
        self.ocr = (instance2.ocr+self.ocr)/2.0
        self.labels.extend(instance2.labels)
        
        self.text +="\n"+instance2.text
        #increase the indices of instance2 by the length of the current document
        doc_length = len(self.text_lines)
        for idx in instance2.indices:
            self.indices.append(idx + doc_length)
        if self.autoindices!=None:
            for idx in instance2.autoindices:
                self.autoindices.append(idx+doc_length)
        self.text_lines.extend(instance2.text_lines)
    
    
    def getSegments(self,indices):
        segments = []
        s_i = indices[0]-1
        for i in range(1,len(indices)):
            s_e = indices[i]-1
            seg = "\n".join(self.text_lines[s_i:s_e])
            segments.append(seg)
            s_i= indices[i]-1
        #last segment
        s_e = len(self.text_lines)
        seg = "\n".join(self.text_lines[s_i:s_e])
        segments.append(seg)
        return segments

    def getAutomaticSegments(self):
        return self.getSegments(self.autoindices)

    def getGoldSegments(self):
        return self.getSegments(self.indices)

    #convert string labels to int labels
    def getGoldLabels(self):
        mapping = {}
        mi = 0
        goldLabels=[]
        for l in self.labels:
            if l in mapping:
                goldLabels.append(mapping[l])
            else:
                goldLabels.append(mi)
                mapping[l]=mi
                mi+=1
        return goldLabels
    
    def getBegin(self,fr):
        
        for i in reversed(range(0,len(self.indices))):
            if fr >= self.indices[i]:
                return i
        
            
    def getEnd(self,to):
        for i in reversed(range(0,len(self.indices))):
            if self.indices[i]<to:
                return i
        

            

    def getAutoLabels(self):
        mapping = {}
        mi = 0
        labels = []
        new_autoindices = self.autoindices[:]
        new_autoindices.append(len(self.text_lines))
        #print(new_autoindices)
        #print(labels)
        #print("Gold Indices",self.indices)
        #print("Gold Annotat", self.labels)
        for i in range(0,len(new_autoindices)-1):
            fr = new_autoindices[i]
            to = new_autoindices[i+1]
            
            label_fr = self.getBegin(fr)
            label_to = self.getEnd(to)
            #print(fr,to,label_fr,label_to)
            #print(label_fr,label_to,len(self.indices),fr,to,self.indices[label_fr])
            label = set()

            for i in range(label_fr,label_to+1):
                lab = self.labels[i]
            #    print(i,len(self.labels))
                if lab in mapping:
                    label.add(mapping[lab])
                else:
                    label.add(mi)
                    mapping[lab]=mi
                    mi+=1
            #print(label)
            labels.append(list(label))
        return labels
        #s_i = 
        #for i in range(
# a dataset is a container of instances
class Dataset:
    
    def __init__(self,text_folder,annotation_folder, process= ProcessFiles.DAY, suffix_annotation= ".txt",automatic_annotation_folder=None, automatic_annotation_suffix=None,min_ocr = -100):
        self.text_folder = text_folder
        self.annotation_folder = annotation_folder
        self.process = process
        self.instances = {}
        for f in os.listdir(text_folder):
            if not f.endswith(".txt"):
                continue
            #if not "sn83030214-1912-03-31-seq-38" in f:
            #    continue
            f_annotation = os.path.join(annotation_folder, f[:f.rfind(".")]+suffix_annotation)
            f_text = os.path.join(text_folder,f)
            if not os.path.exists(f_annotation):
                sys.stderr.write("Annotation file does not exist: %s\n"%(f_annotation))
                continue
            f_automatic_annotation = None
            if automatic_annotation_folder!=None:
                f_automatic_annotation = os.path.join(automatic_annotation_folder, f[:f.rfind(".")]+automatic_annotation_suffix)
            #print("Annotation file exists: %s"%(f_annotation))
            key = None
            if self.process == ProcessFiles.FILE:
                key = f
            elif self.process == ProcessFiles.DAY:
                key = f[:f.rfind("-seq")]
            elif self.process == ProcessFiles.ALL:
                key = "all"
            new_instance = Instance(f_text, f_annotation,f_automatic_annotation,key)
            if new_instance.ocr < min_ocr:
                continue
            if not key in self.instances:
                self.instances[key]=new_instance
            else:
                #append data to existing instance
                self.instances[key].append(new_instance)
            #print ("WTF",key,f_text,self.instances[key].autoindices)
            #print ("WTF",key,f_text,self.instances[key].indices)
            #print ("WTF",key,f_text,self.instances[key].labels)
        self.key_list = self.instances.keys()
    
    
    def iterate_gold_segments(self):
        for instance in self.instances:
            yield self.instances[instance].getGoldSegments()    
    
    def __iter__(self):
        for instance in self.instances:
            yield self.instances[instance]
                    
