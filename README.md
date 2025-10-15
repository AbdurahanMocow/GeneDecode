# GeneDecode  
**Decode your biology. Own your future.**  
*A computational pipeline for variant decoding and personalised genomic interpretation.*

---

## Overview  
GeneDecode is a bioinformatics application designed to process, interpret, and structure raw genomic data from direct-to-consumer genetic testing platforms such as 23andMe and AncestryDNA.  
The project aims to develop transparent, research-grade genomic interpretation pipelines that place data ownership and understanding directly in the hands of users.  

The core system parses user-supplied genomic text files into standardized data tables suitable for downstream annotation, visualization, and clinical interpretation.  

---

## Current Capabilities  
### DNA Parser  
- Converts raw genome `.txt` files into structured `.csv` format.  
- Successfully tested on full 23andMe V5 datasets (≈836,000 variants).  
- Implements efficient data handling through the pandas library.  
- Designed for extensibility toward functional annotation and trait analysis.  

---

## Ongoing Development  
The next development stages will integrate:  
- **Genomic Annotation:** Mapping rsIDs to gene loci and known variants using the Ensembl REST API.  
- **Functional Interpretation:** Linking variants to biochemical pathways, disease risk factors, and pharmacogenomic relevance.  
- **Visualization Layer:** A web-based dashboard (Streamlit) for gene- and pathway-level insight generation.  

---

## Project Structure  

| **Path / File**         | **Description** |
|--------------------------|-----------------|
| `scripts/`               | Core Python code |
| `scripts/parser.py`      | Main genome file parser |
| `data/`                  | Raw input data (excluded from version control) |
| `outputs/`               | Processed result files (excluded from version control) |
| `.gitignore`             | Specifies which files/folders Git should ignore |
| `requirements.txt`       | Lists Python dependencies |

---

## Technical Overview  
**Programming Language:** Python 3.14  
**Core Libraries:** pandas, numpy *(future: requests, matplotlib, streamlit)*  
**System Requirements:** Compatible with Windows, macOS, and Linux.  

---

### To Run the Parser:
```
python scripts/parser.py
```
### Install Dependencies (if required):
```
pip install -r requirements.txt
```
---

### Research Vision
GeneDecode explores the frontier between personal genomics and computational bioinformatics.
By converting raw genotype data into structured, interpretable formats, the platform supports reproducible research and responsible self-analysis.
Future iterations will focus on integrating high-confidence variant annotation, nutrition-genomics insight, and pharmacogenomic analysis for personalised healthcare decision-making.

---

**Name:** Abdurahan Mocow  
**Discipline:** Bioinformatics & Computational Biology  
**Focus Areas:** Genomic Data Processing · Variant Interpretation · Translational Bioinformatics  
