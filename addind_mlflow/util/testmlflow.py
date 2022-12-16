import streamlit as st

def info_to_mlflow(algorism):
    # determine algorism
        get parameters
        mlflow.log_param('penalty', penalty)
        mlflow.log_param('dual', dual)
        mlflow.log_param('C', C)
        mlflow.log_param('solver', solver)
        mlflow.log_param('multi_class', multi_class)

    elif algorism == 'RandomForest Classifier':
        # get parameters
        mlflow.log_param('n_estimators', n_estimators)
        mlflow.log_param('max_depth', max_depth)
        mlflow.log_param('criterion', criterion)
        mlflow.log_param('min_samples_split', min_samples_split)
        mlflow.log_param('min_samples_leaf', min_samples_leaf)
        mlflow.log_param('max_features', max_features)
        mlflow.log_param('bootstrap', bootstrap)
        mlflow.log_param('max_samples', max_samples)

    elif algorism == 'Support Vector Classifier':
        # get parameters
        mlflow.log_param('C', C)
        mlflow.log_param('kernel', kernel)
        mlflow.log_param('degree', degree)
        mlflow.log_param('coefo', coefo)

    elif algorism == 'KNeighbors Classifier':
    # get parameters
        mlflow.log_param('n_neighbours', n_neighbours)
        mlflow.log_param('weights', weights)
        mlflow.log_param('algorithm', algorithm)
        mlflow.log_param('leaf_size', leaf_size)
        mlflow.log_param('p', p)


