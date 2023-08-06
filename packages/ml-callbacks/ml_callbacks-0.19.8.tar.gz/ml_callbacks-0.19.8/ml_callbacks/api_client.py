import time
import uuid
from pprint import pprint
import ml_tracking
from ml_tracking.api import ml_model_api
from ml_tracking.model.register_model_run_command import RegisterModelRunCommand
from ml_tracking.model.iteration_update_command import IterationUpdateCommand
from ml_tracking.model.epoch_update_command import EpochUpdateCommand
from ml_tracking.model.save_notebook_code_command import SaveNotebookCodeCommand
from ml_tracking.model.status_update_command import StatusUpdateCommand

class ApiClient():
    name = ""
    session_id = 0
    configuration = None
    
    def __init__(self, name, base_url):
        self.name = name
        self.configuration = ml_tracking.Configuration(host = base_url)
        
    def register(self, dataset, device, part, lr, loss, batchsize, optimizer, momentum):
        if self.session_id == 0:
            with ml_tracking.ApiClient(self.configuration) as api_client:
                api_instance = ml_model_api.MlModelApi(api_client)
                model = RegisterModelRunCommand(
                    name=self.name,
                    dataset=dataset,
                    part=part,
                    device=device,
                    lr=lr,
                    loss=loss,
                    batch_size=batchsize,
                    optimizer=optimizer,
                    momentum=momentum,
                    u_id=str(uuid.uuid1())
                )
                api_response = api_instance.ml_model_register(register_model_run_command=model)
                self.session_id = api_response
            
    def after_iteration(self, iteration):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = IterationUpdateCommand(
                session_id=self.session_id,
                iteration=iteration
            )
            api_instance.ml_model_iteration(iteration_update_command=model)
            
    def after_epoch(
        self, 
        epoch, 
        train_accuracy, 
        train_loss, 
        train_time, 
        val_accuracy, 
        val_loss,
        val_time,
        train_kappa,
        train_auc,
        train_f1s,
        train_recall,
        train_precision,
        val_kappa,
        val_auc,
        val_f1s,
        val_recall,
        val_precision
        ):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = EpochUpdateCommand(
                session_id=self.session_id,
                epoch=epoch,
                train_accuracy=float(train_accuracy),
                train_loss=float(train_loss),
                train_time=float(train_time),
                val_accuracy=float(val_accuracy),
                val_loss=float(val_loss),
                val_time=float(val_time),
                train_kappa=float(train_kappa),
                train_auc=float(train_auc),
                train_f1s=float(train_f1s),
                train_recall=float(train_recall),
                train_precision=float(train_precision),
                val_kappa=float(val_kappa),
                val_auc=float(val_auc),
                val_f1s=float(val_f1s),
                val_recall=float(val_recall),
                val_precision=float(val_precision)
            )
            api_instance.ml_model_after_epoch(epoch_update_command=model)
            
    def get_save_path(self):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = RegisterModelRunCommand(
                name=self.name,
                u_id=str(uuid.uuid1())
            )
            return api_instance.ml_model_save_path(session_id=self.session_id)
            
    def set_status(self, status, error):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = StatusUpdateCommand(
                session_id=self.session_id,
                status=status,
                error=error
            )
            api_instance.ml_model_update_status(status_update_command=model)
            
    def save_script(self, script):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = SaveNotebookCodeCommand(
                session_id=self.session_id,
                script=script
            )
            api_instance.ml_model_save_script(save_notebook_code_command=model)
