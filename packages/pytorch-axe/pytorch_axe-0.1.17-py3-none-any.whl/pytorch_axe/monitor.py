import copy
import numpy as np
from tqdm.notebook import trange

class Monitor:
    def __init__(self, model, optimizer, scheduler, patience, metric_fn, 
                 min_epochs, max_epochs, dataset_sizes, early_stop_on_metric=False,
                 lower_is_better=True, keep_best_models=False, verbose=True):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.patience = patience
        self.metric_fn = metric_fn
        self.min_epochs = min_epochs
        self.max_epochs = max_epochs
        self.dataset_sizes = dataset_sizes
        self.early_stop_on_metric = early_stop_on_metric
        self.lower_is_better = lower_is_better
        self.verbose = verbose
        
        if verbose:
            self.iter_epochs = trange(max_epochs)
        else:
            self.iter_epochs = range(max_epochs)
            
        if lower_is_better:
            self.epoch_loss = {"train": np.inf, "valid": np.inf}
            self.epoch_metric = {"train": np.inf, "valid": np.inf}
            self.best_loss = np.inf
            self.best_metric = np.inf
        else:
            self.epoch_loss = {"train": -np.inf, "valid": -np.inf}
            self.epoch_metric = {"train": -np.inf, "valid": -np.inf}
            self.best_loss = -np.inf
            self.best_metric = -np.inf
            
        self.train_loss = list()
        self.valid_loss = list()
        self.train_metric = list()
        self.valid_metric = list()
            
        self.best_model_state = model.state_dict()
        self.best_models = list()
        self.keep_best_models = keep_best_models

        self.epoch_counter = {"train": 0, "valid": 0}
        self.es_counter = 0
        self.running_loss = 0.0
        self.running_metric = 0.0
        
    def check_if_improved(self, best, actual):
        if self.lower_is_better and (actual < best):
            return True
        elif not self.lower_is_better and (best > actual):
            return True
        else:
            return False

    def reset_epoch(self):
        self.running_loss = 0.0
        self.running_metric = 0.0
    
    def step(self, loss, batch_size, predictions=None, targets=None):
        self.running_loss += loss.item() * batch_size
        if (self.metric_fn is not None) and (predictions is not None and targets is not None):
            self.running_metric += self.metric_fn(predictions, targets).sum().item()

    def log_epoch(self, phase):
        self.epoch_loss[phase] = self.running_loss / self.dataset_sizes[phase]
        self.epoch_metric[phase] = self.running_metric / self.dataset_sizes[phase]
        
        if phase == "train":
            self.train_loss.append(self.epoch_loss[phase])
            self.train_metric.append(self.epoch_metric[phase])
        elif phase == "valid":
            self.valid_loss.append(self.epoch_loss[phase])
            self.valid_metric.append(self.epoch_metric[phase])

        postfix_kwargs = {
            "a_train_loss": f"{self.epoch_loss['train']:0.6f}",
            "b_valid_loss": f"{self.epoch_loss['valid']:0.6f}",
            "c_best_loss":  f"{self.best_loss:0.6f}",}
        if self.metric_fn is not None:
            postfix_kwargs["d_train_metric"] = f"{self.epoch_metric['train']:0.6f}"
            postfix_kwargs["e_valid_metric"] = f"{self.epoch_metric['valid']:0.6f}"
            postfix_kwargs["f_best_metric"] =  f"{self.best_metric:0.6f}"
        postfix_kwargs["g_es_counter"] = self.es_counter
        if self.scheduler is not None:
            try:
                postfix_kwargs["h_last_lr"] = f"{self.scheduler.get_last_lr()[0]:0.8f}"
            except:
                pass
            
        if self.verbose: 
            self.iter_epochs.set_postfix(**postfix_kwargs)

        self.epoch_counter[phase] += 1
        early_stop = False

        if phase == "valid":
            if self.epoch_counter[phase] >= self.min_epochs:
            
                if not self.early_stop_on_metric:
                    improved = self.check_if_improved(self.best_loss, self.epoch_loss["valid"])
                elif self.early_stop_on_metric:
                    improved = self.check_if_improved(self.best_metric, self.epoch_metric["valid"])

                if improved:
                    self.best_loss = copy.deepcopy(self.epoch_loss["valid"])
                    self.best_metric = copy.deepcopy(self.epoch_metric["valid"])
                    self.best_model_state = copy.deepcopy(self.model.state_dict())
                    if self.keep_best_models:
                        self.best_models = [copy.deepcopy(self.model, )]
                    self.es_counter = 0
                else:
                    self.es_counter += 1
                    if self.keep_best_models:
                        self.best_models.append(copy.deepcopy(self.model))
                    if self.es_counter >= self.patience:
                        early_stop = True
                        if self.verbose:
                            self.iter_epochs.close()
                
        return early_stop
