import pandas as pd
import numpy as np

from projectwind.data import get_data, split_test_data, split_fit_data
from projectwind.sampling import get_clean_sequences
from projectwind.pipeline import get_pipeline

def trainer():

    # Get data & perform  splits
    data, fit_data, = get_data()
    train_data, test_data = split_test_data(data)
    X_fit, y_fit = split_fit_data(fit_data)

    
    # Pipeline fit
    pipeline = get_pipeline()
    pipeline.fit(X_fit)
    
    # Transform data & fetch sequences
    scaled_samples = []
    for WTG_data in train_data:
        WTG_samples = get_clean_sequences(WTG_data,
                                        fitted_pipeline=pipeline,
                                        day_length=5.5, 
                                        number_of_subsamples=100,  # Starting small with only 100 samples / WTG
                                        acceptable_level_of_missing_values=0.1)
        scaled_samples.append(WTG_samples)
    
    print(scaled_samples)
    
    # Shuffle WTG sequences & target
    
    # Save sequences for quicker upload time
    # samples_csv_zip = pd.DataFrame()
    # for sample in scaled_samples:
    #     samples_csv_zip = pd.concat((samples_csv_zip,sample),ignore_index=False)
    # samples_csv_zip.to_csv('./data/samples.csv')

    # Load samples
    
    # Get model

    # Train model

    # Predict (test pipeline)

  

if __name__ == "__main__":
    trainer()
    
