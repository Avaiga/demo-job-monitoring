from taipy import Config
from job_monitoring.algo.ml import train, predict, preprocess, fixed_value


node_dataset = Config.configure_data_node(
    id="dataset", storage_type="csv", default_path="data/data.csv", headers=True
)

node_preprocessed = Config.configure_data_node(
    id="preprocessed",
)


node_prediction_model = Config.configure_data_node(
    id="prediction_model",
    storage_type="pickle",
)

node_prediction = Config.configure_data_node(
    id="prediction",
)

node_value = Config.configure_data_node(
    id="fixed_value",
    default_data=fixed_value,
    storage_type="pickle",
)

# =================

task_preprocess = Config.configure_task(
    id="preprocess", input=[node_dataset], output=node_preprocessed, function=preprocess
)

task_train = Config.configure_task(
    id="train", input=[node_preprocessed], output=node_prediction_model, function=train
)

task_predict = Config.configure_task(
    id="predict",
    input=[node_value, node_prediction_model],
    output=node_prediction,
    function=predict,
)

# =================

pipeline_train = Config.configure_pipeline(
    id="train", task_configs=[task_preprocess, task_train]
)

pipeline_predict = Config.configure_pipeline(id="predict", task_configs=[task_predict])

# =================

if __name__ == "__main__":
    # Generate a config.toml file
    Config.export("config.toml")
