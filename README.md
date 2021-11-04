# 3D Houses

## Table of contents

[Description](#Description)
[Installation](#Installation)
[Usage](#Usage)
[Visuals](#Visuals)
[Steps](#Steps)
[Architecture](#Architecture)
[Limitations](#Limitations)
[Personal situation](#Personal situation)


## Description
The main goal of this project is to model a house in Flanders in 3D using only the address. It uses several API's (Application Programming Interface) 
provided by the Flanders 
government, as well as datasets of precomputed data.

The raw data was collected as part of the DHMV II [Digital Height Model Flanders II](https://overheid.vlaanderen.be/dhm-digitaal-hoogtemodel-vlaanderen-ii/) project. It was in the form of LIDAR (or Lidar) data. 
"Lidar ... is a method for determining ranges (variable distance) by targeting an object with a laser and measuring 
the time for the reflected light to return to the receiver."\[It\] can ... be used to make digital 3-D representations of areas 
on the earth's surface..."[Lidar](https://en.wikipedia.org/wiki/Lidar/)

From this data, DSM (Digital Surface Map) and DTM (Digital Terrain Map) data was computed. They are available here:
- [DSM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m)
- [DTM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m)

These datasets both have 43 files, representing the following regions of Flanders:
![Flanders](https://overheid.vlaanderen.be/sites/default/files/media/Digitale%20overheid/DHM/Opdrachtzones%20DHM-Vlaanderen%20II_2.jpg)

This project is a part of the [Becode.org AI Bootcamp](https://becode.org/learn/ai-bootcamp/) program.


## Installation
Download the repository from GitHub using:
```python
git@github.com:eceboran/3D_houses.git
```

The packages required to run the project can be found in:
```python
requirements.txt
```
To install all required packages, follow these steps:
- Crete and activate your virtual environment. 
- Navigate to the main project repository that contains requirements.txt.
- To install the required packages in pip, in the terminal, run:
```python
python3 -m pip install -r requirements.txt
```
- To install them with anaconda, run:
```python
conda install --file requirements.txt 
```


## Usage
In the terminal, navigate to the folder that contains the Jupyter notebook main.ipynb. 
Open and run the notebook.

You will be asked to input an address in Flanders. The input request will be repeated until a valid address is provided.
If there are several possible addresses, you will be given a list of suggested addresses.

To quit, type:
```python
quit
```
as the address.


## Visuals
Address in Flanders

![image name here](visuals/example.png)

## Steps

This project required multiple steps, that could be completed independently and then merged.
The steps were:

- Research. Reading on LIDAR, DSM and DTM data, coordinate systems, projections and GeoTIFF files.
Reviewing packages used in DEM (digital elevatio model) related projects online to get ideas on where to start.
- Data exploration. Opening the data and looking at the contents in detail to understand how they can be used. 
- Metadata creation. Creating a metadata file from all DSM and DTM files to save file links and GeoTIFF boundaries.
- Address API. Retrieving information on an address in Flanders with an API.
- Building API. Retrieving information on a building in Flanders with an API.
- File selection. Selection of GeoTIFF file that contains the building.
- Online data access. Loading DSM and DTM files directly from GeoTIFF files in online zip files.
- CHM calculation. Calculating CHM using DSM and DTM data.
- Plotting. Plotting and saving 3D plots of a selected building.
  
## Architecture
The project is structured as below:
```
3d-house-project
│  README.md             :project description
│  main.ipynb 			 :jupyter notebook file to run to start the program
│  create_metadata.ipynb :creates a dataframe for the metadata corresponding to the datasets:
│						  [DSM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m)
│					      [DTM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m)
│  						  saves it under data/metadata	 
│  requirements.txt      :list of required packages
│  .gitignore            :files and folders ignored by git
│
└───data                 :data directory
│   │					  zip files can be downloaded here to be loaded locally
│   └───metadata         :metadata for the Geopunt Flanders DSM and DTM (1 meter resolution) datasets
└───utils                :directory contains all the core scripts of the program
│    Address.py          :script to create a House object and get info
│    Buildings.py        :script to associate the DSM and DTM tiffs to a House object
│ 
└───visuals              :images for buildings
```


## Limitations
- Limited to Flanders.
This project can only plot buildings in Flanders.
- Incorrect location from API.
For some addresses, the API may not give the correct location of the building.
- Execution time
As the files are accessed online, the execution time is slower than for local files.
- Buildings contained by multiple GeoTIFF files.
This project does not yet consider buildings that do not fit in a single GeoTIFF file.
- Newer buildings.
The DEM database was formed by Geopunt Flanders between 2013 and 2015.
This project cannot access height information for buildings and corresponding addresses formed after 2015. 


## Personal situation
This project is my third (second individual) challenge at [BeCode](https://becode.org/), 
following six weeks of learning basic and advanced Python concepts, data manipulation and visualization with Python.


This project uses Black: The Uncompromising Code Formatter
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)