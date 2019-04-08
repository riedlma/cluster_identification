# Clustering-Based Article Identification in Historical Newspapers

source code and text collection for the paper "Clustering-Based Article Identification in Historical Newspapers" published at the LaTech workshop.


# Clustering of Texts:

Before the clustering can be performed, the dataset needs to be downloaded and the segmentation boundaries need to be known.
Then, the clustering can be performed with the following script:

```
python execute_clustering_gold_standard_arg.py dataset/corpus_txt dataset/annotations/ -esc -pd -rs 1 2 3 4 5 
```

The script allows lots of parameters, which are listed in the help command:

```
python execute_clustering_gold_standard_arg.py --help
usage: execute_clustering_gold_standard_arg.py [-h] [-e100 EMBEDDINGS100]
                                               [-e200 EMBEDDINGS200]
                                               [-mo MIN_OCR]
                                               [-aaf AUTOMATIC_ANNOTATION_FOLDER]
                                               [-sc] [-esc] [-nc NC [NC ...]]
                                               [-n NGRAM [NGRAM ...]] [-pf]
                                               [-pd] [-pa] [-jws]
                                               [-rs RS [RS ...]]
                                               document_folder
                                               annotation_folder

Execute the clustering and segmentation and the evaluation

positional arguments:
  document_folder       folder for the text document
  annotation_folder     folder for the annotations of the text document

optional arguments:
  -h, --help            show this help message and exit
  -e100 EMBEDDINGS100, --embeddings100 EMBEDDINGS100
                        binary for the 100 dimensional fastText embeddings. If
                        not active, they will not be used.
  -e200 EMBEDDINGS200, --embeddings200 EMBEDDINGS200
                        binary for the 200 dimensional fastText embeddings. If
                        not active, they will not be used.
  -mo MIN_OCR, --min-ocr MIN_OCR
                        minimum OCR score (default: -100.0)
  -aaf AUTOMATIC_ANNOTATION_FOLDER, --automatic_annotation_folder AUTOMATIC_ANNOTATION_FOLDER
  -sc, --spectral_clustering
                        use standard spectral clustering
  -esc, --exponential_spectral_clustering
                        use exponential spectral clustering
  -nc NC [NC ...], --number_of_cluster NC [NC ...]
                        Specify the number of clusters to be used (can be a
                        list of numbers) [1-15,20,30,40,50,60,100]
  -n NGRAM [NGRAM ...], --ngram NGRAM [NGRAM ...]
                        specify the N for the n-grams that are extracted
                        (default: 3)
  -pf, --process_file   Process each file individually
  -pd, --process_day    Process files day-wise
  -pa, --process_all    Process all files
  -jws, --jaccard_word_sim
                        apply Jaccard Word similarity
  -rs RS [RS ...], --random_states RS [RS ...]
                        Using this option, the clustering will be performed as
                        often as seeds are provided. If none is given, a time-
                        based random seed is used.
```

 
 
# Automatic Text Segmentation

The automatic segmentation using TextTiling can be performed with the following command, expecting as parameters an input directory of files and that will write the segmented documents to output_directory.

```
python texttiling_app.py input_directory output_directory
```

In order to evaluate the segmentation, the following script can be used:

```
python texttiling_eval.py input_directory annotation_dir min_ocr
```

The input_directory contains the text documents, the annotation_dir the annotated segment boundaries and the min_ocr the mininmal OCR score that a file needs to fullfy in order to be considered for the evaluation. 


# Dataset:

The dataset needs to be downloaded using the script:

```
sh scripts/download_newspaper.sh 
```

Then, all data for the task are located in the folder "dataset". There are the following folder and file:

- annotations: annotation for each page
- corpus_txt: all text files of the pages OCRed from the pdfs. 
- corpus_pdf: all PDFs of the pages
- content.csv: file, listing all articles including their title and author (if available)



## Citation


```
@inproceedings{riedl19:historic_newspaper,
  title = {Clustering-Based Article Identification in Historical Newspapers},
  author = {Riedl, Martin, Daniela Betz and Padó, Sebastian},
  booktitle = {Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature},
  series={LaTeCH-CLfL 2019},
  address = {Minneapolis, USA},
  note = {To appear},
  year = 2019
}

```


## License

This project is licensed under the terms of the Apache 2.0 ASL license. If used for research, citation would be appreciated. The annotation data is published under the permissive CC-BY license.
