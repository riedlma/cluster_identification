import argparse
import os
import sys
import utils
import similarities
import clustering


import numpy as np
from numpy import zeros
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
import bcubed


parser = argparse.ArgumentParser(description='Execute the clustering and segmentation and the evaluation')

parser.add_argument('document_folder',        help='folder for the text document')
parser.add_argument('annotation_folder',        help='folder for the annotations of the text document')
parser.add_argument("-e100","--embeddings100",dest="embeddings100",help="binary for the 100 dimensional fastText embeddings. If not active, they will not be used.",default = None)
parser.add_argument("-e200","--embeddings200",dest="embeddings200",help="binary for the 200 dimensional fastText embeddings. If not active, they will not be used.",default = None)
parser.add_argument("-mo","--min-ocr",dest="min_ocr",help="minimum OCR score (default: -100.0)",type=float,default=-100.0)
parser.add_argument("-aaf","--automatic_annotation_folder",dest="automatic_annotation_folder",default = None)
parser.add_argument("-sc","--spectral_clustering",help="use standard spectral clustering",dest="sc",action="store_true")
parser.add_argument("-esc","--exponential_spectral_clustering",help="use exponential spectral clustering",dest="esc",action="store_true")
parser.add_argument("-nc","--number_of_cluster",help="Specify the number of clusters to be used (can be a list of numbers) [1-15,20,30,40,50,60,100]",dest="nc", nargs='+', type=int,default=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,30,40,50,60,100])
parser.add_argument("-n","--ngram",help="specify the N for the n-grams that are extracted (default: 3)", dest="ngram",default=[3],nargs='+',type=int)
parser.add_argument("-pf","--process_file",help="Process each file individually",dest="pf",action="store_true")
parser.add_argument("-pd","--process_day",help="Process files day-wise",dest="pd",action="store_true")
parser.add_argument("-pa","--process_all",help="Process all files",dest="pa",action="store_true")
parser.add_argument("-jws","--jaccard_word_sim",help="apply Jaccard Word similarity",dest="jws",action="store_true")
parser.add_argument("-rs","--random_states", help="Using this option, the clustering will be performed as often as seeds are provided. If none is given, a time-based random seed is used.",dest="rs",nargs="+",type =int)


args = parser.parse_args()


folder_text = args.document_folder
folder_annotations = args.annotation_folder
print("Text: ",folder_text)
print("Annotations: ",folder_annotations)
min_ocr = args.min_ocr
gold = True
embeddings_100= None
embeddings_200 = None
automatic_annotation_folder= None
embeddings_100 = args.embeddings100
embeddings_200 = args.embeddings200

if not args.automatic_annotation_folder==None:
    
    automatic_annotation_folder =args.automatic_annotation_folder
    gold = False

text_suffix= ".txt"
annotation_suffix = "-merged-merged.txt"
automatic_annotation_suffix = ".txt.anno"

#parameters that will be combined and iterated
sims = []

for n in args.ngram:
    sims.append(similarities.JaccardNGramSimilarity(n))

#sims = [similarities.JaccardNGramSimilarity(args.ngram)]#, similarities.DiceNGramSimilarity()]
if args.jws:
    sims.append(similarities.JaccardWordSimilarity())
if embeddings_100!=None:
    sims.append(similarities.CosineEmbeddings(embeddings_100,100))
if embeddings_200!=None:
    sims.append(similarities.CosineEmbeddings(embeddings_200,200))
clusterings = []
if args.sc:
    print("Clustering: Spectral Clustering")
    clusterings.append(clustering.SpectralClustering())
if args.esc:
    print("Clustering: Exponential Spectral Clustering")
    clusterings.append(clustering.SpectralExponentialClustering())

#number_of_cluster = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,30,40,50,60,100]
#number_of_cluster = [2]
#number_of_cluster = range(1,100)
#number_of_cluster = range(10,20)
number_of_cluster = args.nc
print("Number of cluster",number_of_cluster)
#number_of_cluster = [12,13,14,52,53,54]
#number_of_cluster = [12]#,13,14,52,53,54]
#number_of_cluster = range(1,100)

processes = []
if args.pf:
    print("Process: File")
    processes.append(utils.ProcessFiles.FILE)
if args.pd:
    print("Process: Day")
    processes.append(utils.ProcessFiles.DAY)
if args.pa:
    print("Process: All")
    processes.append(utils.ProcessFiles.ALL)

matrix_map = {}
    
# returns evaluation scores (e.g. NMI and B-Cubed)
def evaluateNMI(goldLabels,results):
    #nmi  =  normalized_mutual_info_score(goldLabels,results)
    nmi = adjusted_mutual_info_score(goldLabels,results,"arithmetic")
    return nmi

def evaluateNMING(goldLabels,results):
    #nmi  =  normalized_mutual_info_score(goldLabels,results)
    #nmi = adjusted_mutual_info_score(goldLabels,results,"arithmetic")
    return -1.0

def evaluateBCubedNG(goldLabels,results):
    res_map = {}
    gold_map = {}
    for i in range(0,len(results)):
        res_map[i]=set()
        res_map[i].add(results[i])
        gold_map[i]=set()        
        for gi in goldLabels[i]:
            gold_map[i].add(gi)
    p =  bcubed.precision(res_map,gold_map)
    r =  bcubed.recall(res_map,gold_map)
    f =  bcubed.fscore(p,r)

    
    return [p,r,f]
def evaluateBCubed(goldLabels,results):
    res_map = {}
    gold_map = {}
    for i in range(0,len(results)):
        res_map[i]=set()
        res_map[i].add(results[i])
        gold_map[i]=set()        
        gold_map[i].add(goldLabels[i])
    p =  bcubed.precision(res_map,gold_map)
    r =  bcubed.recall(res_map,gold_map)
    f =  bcubed.fscore(p,r)

    
    return [p,r,f]
def evaluate(instance, results,gold = True):
    if gold:
        goldLabels = instance.getGoldLabels()
        results = results.tolist()
        arr = evaluateBCubed(goldLabels,results)
        arr.append(evaluateNMI(goldLabels,results))
    else:

        goldLabels = instance.getAutoLabels()
        #print("autolabels",goldLabels)
        #print("results",results)
        arr = evaluateBCubedNG(goldLabels,results)
        arr.append(evaluateNMING(goldLabels,results))
    return arr

def getName(instance):
    return type(instance).__name__

matrix_map = {}

def startProcessingSegments(dataset,sim_measure,clustering,num_cluster,output_str,gold =True,random_seeds=None):
    
    
    #iterate over segments:
    num_instances = 0
    sum_results = [0.0]*4

    for instance in dataset:
        num_instances+=1
        if gold:
            goldSegments = instance.getGoldSegments()
        else:
            goldSegments = instance.getAutomaticSegments()
        if len(goldSegments)<num_cluster:
            print("%s\tcluster number (%d) > number of gold segments (%d): "%(output_str,num_cluster,len(goldSegments)))
            continue
        
        matrix = None
        #print(name)
        fromMatrix = "TRUE"
        name = instance.name +"-"+sim_measure.getName()
        
        if name in matrix_map:
            matrix = matrix_map[name]
        else:
            fromMatrix = "FALSE"
            matrix = zeros([len(goldSegments),len(goldSegments)])
            for i in range(0,len(goldSegments)):
                for j in range(i,len(goldSegments)):
                    #TODO: adjust to correct stuff
                    
                    similarity = sim_measure.similarity(goldSegments[i],goldSegments[j])
                    matrix[i][j] = similarity
                    matrix[j][i] = similarity
            matrix_map[name]=matrix
        #print("Matrix Length",len(matrix))
        if random_seeds == None:
            cluster_results = clustering.cluster(num_cluster,matrix)
            #print("Cluster")
            #print(cluster_results)
            eval_results = evaluate(instance,cluster_results,gold)
        else:
            merge_results = [0.0]*4
            for seed in random_seeds:
                cluster_results = clustering.cluster(num_cluster,matrix,seed)
                eval_results = evaluate(instance,cluster_results,gold)
                merge_results+=np.array(eval_results)
            eval_results = [x/len(random_seeds) for x in merge_results]
            
        str_eval_results = ""
        for r in eval_results:
            str_eval_results+="\t%f"%(r)
                                        
        print(output_str+"\t"+instance.name+"\t"+str_eval_results+"\t"+fromMatrix)
        sum_results = sum_results+np.array(eval_results)
    if num_instances ==0:
        return
    sum_results = [x /float(num_instances) for x in sum_results] 
    #sum_results = sum_results/float(num_instances)
    
    str_sum_results = ""
    for r in sum_results:
        str_sum_results+="\t%f"%(r)
    print(output_str+"\t"+"Overall: "+str_sum_results)

def check_files_consistency(files1,files2):
    res1 = (files2-files1)
    res2 = (files1-files2)
    if len(res1)>0:
        print(res1)
    if len(res2)>0:
        print(res2)
def check_file_consistency(folder_text,folder_annotations):
    files1 = set([f for f in os.listdir(folder_text) if f.endswith(".txt")])
    files2 = set([f.replace(annotation_suffix,text_suffix) for f in os.listdir(folder_annotations)])
    check_files_consistency(files1,files2)
    check_files_consistency(files2,files1)


check_file_consistency(folder_text,folder_annotations)

for process in processes:
    #instanciate dataset
    dataset = utils.Dataset(folder_text,folder_annotations,process,annotation_suffix,automatic_annotation_folder,automatic_annotation_suffix,min_ocr)
    for clustering in clusterings:
        for num in number_of_cluster:
            for sim in sims:
                if sim.getName().startswith("CosineEmbeddings") and getName(clustering).startswith("SpectralClustering"):
                    print("SpectralClustering not possible with embeddings")
                    continue
                str_out = "%s\t%s(%d)\t%s\t"%(str(process),getName(clustering),num,sim.getName())
                #print("%s\t%s(%d)\t%s\t"%(str(process),getName(clustering),num,getName(sim)))
                random_seeds= args.rs
                startProcessingSegments(dataset, sim,clustering,num,str_out,gold,random_seeds)

                sys.stdout.flush()            
