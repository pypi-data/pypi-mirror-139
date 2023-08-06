"""Contains callbacks that save the model and objects to disk."""
import os
from typing import Dict, Union

import torch

from nn_helper.callbacks.base_callback import BaseCallback


class SaveModel(BaseCallback):
    """Save a model(s) or checkpoint of a model(s) to disk."""

    def __init__(self, path: str, submodels: Dict[str, torch.nn.Module] = None, save_checkpoints: bool = False):
        """Initialise the SaveModel instance.

        Args:
            path (str): The path where the serialised objects are saved.
            submodels (Dict[str, torch.nn.Module], optional): A dictionary with submodels that should
                be saved. This gives the ability to save mutliple models. Defaults to None.
            save_checkpoints (bool, optional): Whether to save models and objects after every
                epoch. Defaults to False.
        """
        super().__init__()
        self.path = path
        self.submodels = submodels
        self.save_checkpoints = save_checkpoints

    def on_epoch_end(self, epoch: int, logs: Dict[str, Union[int, float]] = None) -> None:
        """This saves models and objects after every epoch.

        Args:
            epoch (int): The number of epochs.
            logs (Dict[str, Union[int, float]], optional): The logs. Defaults to None.
        """
        if self.save_checkpoints:
            if self.submodels:
                checkpoint_dir = {
                    "epoch": epoch,
                    "batch_count": epoch * self.params["num_batches"],
                    "optimizer_state_dict": self.params["optimizer"].state_dict(),
                }

                for model_name, model_object in self.submodels.items():
                    checkpoint_dir[f"{model_name}_state_dict"] = model_object.state_dict()

                torch.save(checkpoint_dir, os.path.join(self.path, f"model_checkpoint_epoch={epoch}.pth"))
            else:
                torch.save(
                    {
                        "epoch": epoch,
                        "batch_count": epoch * self.params["num_batches"],
                        "model_state_dict": self.model.state_dict(),
                        "optimizer_state_dict": self.params["optimizer"].state_dict(),
                    },
                    os.path.join(self.path, f"model_checkpoint_epoch={epoch}.pth"),
                )

    def on_train_end(self, logs: Dict[str, Union[int, float]] = None) -> None:
        """Saves the model at the end of training to disk.

        Args:
            logs (Dict[str, Union[int, float]], optional): The logs. Defaults to None.
        """
        if self.submodels:
            for model_name, model_object in self.submodels.items():
                torch.save(model_object.state_dict(), os.path.join(self.path, f"{model_name}.pth"))
        else:
            torch.save(self.model.state_dict(), os.path.join(self.path, "model.pth"))
