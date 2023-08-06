<img src="/docs/img/AutonML_logo.png" width=25%>


# CMU TA2 (Built using DARPA D3M ecosystem)

Auto<sup>n</sup> ML is an automated machine learning system developed by CMU Auton Lab 
to power data scientists with efficient model discovery and advanced data analytics. 
Auton ML also powers the D3M Subject Matter Expert (SME) User Interfaces such as Two Ravens http://2ra.vn/.

**Taking your machine learning capacity to the nth power.**

[Auto<sup>n</sup> ML Documentation](https://cmu-ta2.readthedocs.io/en/master/index.html)

Docker image available at 
```
registry.gitlab.com/sray/cmu-ta2:latest
```
  <img src="/docs/img/model_pipeline.png" width="869" height="489">

### D3M dataset
- Any dataset to be used should be in D3M dataset format (directory structure with TRAIN, TEST folders and underlying .json files).
- Example available of a single dataset [here](https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/185_baseball_MIN_METADATA)
- More datasets available [here](https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/)
- Any non-D3M data can be converted to D3M dataset. (See section below on "Convert raw dataset to D3M dataset").

#### [Convert raw dataset to D3M dataset](https://gitlab.com/sray/cmu-ta2/-/blob/master/convert_raw_dataset.rst)
```bash
pip install d3m
python create_d3m_dataset.py <train_data.csv> <test_data.csv> <label> <metric> -t classification <-t ...>
```

Detailed description of dataset type(s), task type(s) and metrics provided **[here](https://gitlab.com/sray/cmu-ta2/-/blob/master/convert_raw_dataset.rst).**

### Run in search mode

- Requires docker on your OS.
- Update location of your dataset for target "input" to the docker run.
- Run the following script:
```bash
./scripts/start_container.sh
```
The above script has 4 mount points for the docker-
1. input: Path of the input dataset
2. output: Directory where all outputs will be stored
3. static: Location of all static files (Use static directory of this repository)
4. scripts: Location of this repository's scripts.

### NOTE: USING A GPU

In addition to the above, if you wish to use the container with a GPU, make sure the GPU capability exists on your system and the proper toolkits are installed, and add the following option to the docker run command in the start_container.sh script:
```
--gpus all
```

The above script will do the following-
1. Pull docker image and run search for best pipelines for the specified dataset using TRAIN data.
2. JSON pipelines (with ranks) will be output in JSON format at /output/<search_dir>/pipelines_ranked/
3. CSV prediction files of the pipelines trained on TRAIN data and predicted on TEST data will be available at /output/<search_dir>/predictions/
4. Training data predictions (cross-validated mostly) are produced in the current directory as /output/<search_dir>/training_predictions/<pipeline_id>_train_predictions.csv.
5. Python code equivalent of executing a JSON pipeline on a dataset produced at /output/<search_dir>/executables/
 This code can be run as-
```
python <generated_code.py> <path_to_dataset> <predictions_output_file>
```
 An example -
```
python ./output/6b92f2f7-74d2-4e86-958d-4e62bbd89c51/executables/131542c6-ea71-4403-9c2d-d899e990e7bd.json.code.py 185_baseball predictions.csv 
```

- If feature_importances and intermediate outputs are desired, call scripts/run_outputs.sh instead of scripts/run.sh from scripts/start_container.sh.
Features importances and intermediate step outputs will be produced in /output/<search_dir>/pipeline_runs/.

Prediction files can be scored using the script evaluate_score.py as below-
```
python evaluate_score.py <true_label_file> <predictions_file> <label> <metric>
```
