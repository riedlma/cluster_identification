import os
import sys

class Annotation:
    
    def __init__(self,filename=None, ignore_new_column = True):
        self.filename = filename
        self.ocr =-1
        self.indices = []
        # value in second column
        self.labels = []
        # value in third column (if used)
        self.section_type = []
        if filename==None:
            return
        i = 0
        #print(filename)
        for l in open(self.filename):
            i+=1
            if len(l.strip())==0:
                continue
            ls = l.strip().split("\t")
            #print(ls)
            if i==1:
                if len(ls)<2:
                    print(filename,ls)
                self.ocr = float(ls[1])
                continue
            if len(ls)<2:
                print(filename,ls)
            self.indices.append(int(ls[0]))
            self.labels.append(ls[1])
            if len(ls)>2:
                if ignore_new_column and (ls[2]=="nc" or ls[2]=="next column"):
                    continue
                self.section_type.append(ls[2])
            else:
                self.section_type.append("")

    # merge advertisement to one block
    def mergeAdvertisement(self):
        idxs = []
        for i in range(1,len(self.section_type)):
            if self.section_type[i]=="ad" and self.section_type[i-1]=="ad":
                idxs.append(i)
        if len(idxs)==0:
            return
        idxs= sorted(idxs,reverse=True)
        for i in idxs:
            del self.labels[i]
            del self.section_type[i]
            del self.indices[i]

    # compare two annotation files just looking at the indices and the section types
    def compare_first_annotation(self,a):
        if not  self.ocr ==a.ocr:
            print(self.filename+"\tOCR different: "+str(self.ocr)+"\t"+str(a.ocr))
        s1 = set(self.indices)
        s2 = set(a.indices)
        
        if len(s1)!=len(self.indices):
            sys.stderr.write("duplicate segments: "+str(self.indices))
        if len(s2)!=len(a.indices):
            sys.stderr.write("duplicate segments: "+str(self.indices))
        #sets are equal
        union =len(s1.union(s2))
        diff = len(s1-s2) + len(s2-s1)
        diff_set = s1-s2
        diff_set |= s2-s1
        return [diff,diff_set]

    # get the section type from a second anotation with the same index
    def getType(self,idx,a):
        for i in range(0,len(a.indices)):
            if idx == a.indices[i]:
                return a.section_type[i]
        return ""
    
    # merge two annotation files for the first annotation step
    def merge_first_annotation(self,a):
        c = Annotation(self.filename)
        c.ocr = (1.0*int(self.ocr)+1.0*int(a.ocr))/2.0
        mapping = {}
        char_i = 0
        for i in range(0,len(self.indices)):
            idx = self.indices[i]
            types = set()
            types.add(self.section_type[i])
            t2 = self.getType(idx,a)
            if t2!= "":
                types.add(t2)
            
            c.section_type.append( ",".join(list(types)))
            c.indices.append(self.indices[i])
            ci = self.labels[i][0]
            if ci in mapping:
                c.labels.append(mapping[self.labels[i]])
                continue
            if ord(ci)==65+char_i:
                mapping[self.labels[i]]=self.labels[i]
                c.labels.append(self.labels[i][0])
            else:
                mapping[self.labels[i]]=str(chr(65+char_i))
                c.labels.append(str(chr(65+char_i)))
            
            char_i+=1
        return c

    def compare_second_annotation(self,a):
        [diff,diff_set] = self.compare_first_annotation(a)
        err=diff
        if (diff)>0:

            print("Difference of sets: ",diff,a.filename)
        else:
            for i in range(0,len(self.labels)):
                if not self.labels[i]==a.labels[i]:
                    print("Labels are different (%s): %s\t%s"%(self.filename,self.labels[i],a.labels[i]))
                    err+=1
                if not self.section_type[i] == a.section_type[i]:
                    print("section types are different (%s): %s\t%s"%(self.filename,self.section_type[i],a.section_type[i]))
                    err+=1
        return err
    def merge_second_annotation(self, a):
        c = Annotation()
        c.filename = self.filename
        c.ocr = self.ocr
        for i in range(0,len(self.indices)):
            if self.indices[i]!=a.indices[i]:
                sys.stderr.write("Indices not equal %s"%(c.filename))
                continue
            c.indices.append(self.indices[i])
            if not self.labels[i]==a.labels[i]:
                print("Labels are different (%s): %s\t%s"%(self.filename,self.labels[i],a.labels[i]))
            if self.section_type[i]=="ad":
                c.labels.append("ad")
            else:
                c.labels.append(self.labels[i])
            if not self.section_type[i] == a.section_type[i]:
                print("section types are different (%s): %s\t%s"%(self.filename,self.section_type[i],a.section_type[i]))
            c.section_type.append("")
                
        return c
        
    
    def write(self,folder, suffix="-merged.txt"):
        fileout = os.path.join(folder,os.path.basename(self.filename))
        idx = fileout.rfind("-")
        fileout = fileout[:idx]+suffix
        fw = open(fileout,"w")
        fw.write("OCR\t"+str(self.ocr)+"\n")
        #print(fileout,self.labels)
        for i in range(0,len(self.indices)):
            fw.write(str(self.indices[i])+"\t"+self.labels[i]+"\t"+self.section_type[i]+"\n")
        fw.close()
