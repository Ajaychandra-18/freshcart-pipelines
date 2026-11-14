import os
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


# Writes the metrics table returned by evaluate_model to a CSV file
@data_exporter
def export_metrics(df, *args, **kwargs):
    df.to_csv('iris_metrics.csv', index=False)
    print('Saved metrics to iris_metrics.csv')


# An exporter returns nothing, so this test takes no required arguments
@test
def test_file_written(*args, **kwargs):
    import pandas as pd
    assert os.path.exists('iris_metrics.csv'), 'iris_metrics.csv was not created'
    assert len(pd.read_csv('iris_metrics.csv')) == 4, 'Expected 4 metric rows'
