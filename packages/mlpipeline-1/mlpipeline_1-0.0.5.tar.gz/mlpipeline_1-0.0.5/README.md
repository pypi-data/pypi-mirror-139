Currently it prepares the data ready for a Machine Learning Classification problem (mainly for now Tabular Dataset). I am soon planning to add other features for Regression problem as well as for Clustering based Problem. My purpose of creating this project is to build an AutoML library, which reduces writing more code to a create a model.
How you can use this is by following the below step:
```
pip install mlpipeline_1==0.0.5
```
```
from ml_pipeline.pipeline import ml_pipe
```
Then you need to pass certain parameters to the ml_pipe function, the first one is the "location of the csv file" which you want to do Classification on, second parameter being the "target variable name", and the last one being the "split size" (value between 0 - 1) i.e., what percent of the whole dataset you want to use as a test set.
```
X_train, X_test, y_train, y_test = ml_pipe(file_path, target_var, split_ratio)
```
The output of the above function you can pass to any Classification model for training.

Soon planning to coming up with more and more features. Planning to make this a full-fledged AutoML library.