from airflow.operators import PythonOperator
from airflow.models import Variable
from train import train_production
import os


class TrainModel(PythonOperator):
    def __init__(self, dag, *args, **kwargs):
        task_id = 'train_model'
        op_kwargs = {
            'model_path': os.path.join(
                Variable.get('local_directory'), 'stackoverflow', 'model'),
            'train_dataset_paths': "{{ task_instance.xcom_pull(task_ids='train_download_to_local', key='downloaded_files') }}",
            'test_dataset_paths': "{{ task_instance.xcom_pull(task_ids='test_download_to_local', key='downloaded_files') }}",
            'labels_paths': "{{ task_instance.xcom_pull(task_ids='tags_download_to_local', key='downloaded_files') }}",
            'train_params': Variable.get('train_params', deserialize_json=True)}
        super().__init__(
            task_id=task_id, dag=dag, python_callable=self.python_callable_wrapper,
            op_kwargs=op_kwargs)

    @staticmethod
    def python_callable_wrapper(model_path, train_dataset_paths,
                                test_dataset_paths, labels_paths,
                                train_params):
        return train_production(model_path, eval(train_dataset_paths),
                                eval(test_dataset_paths),
                                eval(labels_paths)[0], train_params)
