"""Contains callbacks that save the model and objects to disk."""
import os
from typing import Dict, Union

import torch

from nn_helper.callbacks.base_callback import BaseCallback


class SaveModel(BaseCallback):
    """Save a model(s) or checkpoint of a model(s) to disk."""

    def __init__(self, model_path: str, checkpoint_path: str = None, submodels: Dict[str, torch.nn.Module] = None):
        """Initialise the SaveModel instance.

        Args:
            model_path (str): The path where the serialised model(s) are saved.
            checkpoint_path (str): Path to save checkpoint objects after every epoch. These includes
                the models, optimizer, etc. Defaults to None.
            submodels (Dict[str, torch.nn.Module], optional): A dictionary with submodels that should
                be saved. This gives the ability to save mutliple models. Defaults to None.
        """
        super().__init__()
        self.model_path = model_path
        self.checkpoint_path = checkpoint_path
        self.submodels = submodels

    def on_epoch_end(self, epoch: int, logs: Dict[str, Union[int, float]] = None) -> None:
        """This saves models and objects after every epoch.

        Args:
            epoch (int): The number of epochs.
            logs (Dict[str, Union[int, float]], optional): The logs. Defaults to None.
        """
        if self.checkpoint_path:
            if self.submodels:
                checkpoint_dir = {
                    "epoch": epoch,
                    "batch_count": epoch * self.params["num_batches"],
                    "optimizer_state_dict": self.params["optimizer"].state_dict(),
                }

                for model_name, model_object in self.submodels.items():
                    checkpoint_dir[f"{model_name}_state_dict"] = model_object.state_dict()

                torch.save(checkpoint_dir, os.path.join(self.checkpoint_path, f"model_checkpoint_epoch={epoch}.pth"))
            else:
                torch.save(
                    {
                        "epoch": epoch,
                        "batch_count": epoch * self.params["num_batches"],
                        "model_state_dict": self.model.state_dict(),
                        "optimizer_state_dict": self.params["optimizer"].state_dict(),
                    },
                    os.path.join(self.checkpoint_path, f"model_checkpoint_epoch={epoch}.pth"),
                )

    def on_train_end(self, logs: Dict[str, Union[int, float]] = None) -> None:
        """Saves the model at the end of training to disk.

        Args:
            logs (Dict[str, Union[int, float]], optional): The logs. Defaults to None.
        """
        if self.submodels:
            for model_name, model_object in self.submodels.items():
                torch.save(model_object.state_dict(), os.path.join(self.model_path, f"{model_name}.pth"))
        else:
            torch.save(self.model.state_dict(), os.path.join(self.model_path, "model.pth"))
