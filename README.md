# Clustering-Based Article Identification in Historical Newspapers

source code and text collection for the paper "Clustering-Based Article Identification in Historical Newspapers" published at the LaTech workshop.


# Cluster data:

1) download dataset:
 
```
sh scripts/download_newspaper.sh 
```
 


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

This project is licensed under the terms of the Apache 2.0 ASL license (as Tensorflow and derivatives). If used for research, citation would be appreciated.
