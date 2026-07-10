# Retriving filepaths from the Data Aggregation System
We use the terminal dasgoclient to query the DAS.
In order to access the client, set up the cmssw default environment (the coffea apptainer image is not required).
```
$ source setup_dasgoclient.sh
```

When using `find_dataset_files.py`, provide the script the dataset name key as it exists in your dictionary json (you can specify the path to the json using option --dataset) as well as the year.
This script with query the DAS for files in the specified dataset, prepend the relevant xrootd url, and write out the list of files to a json.
