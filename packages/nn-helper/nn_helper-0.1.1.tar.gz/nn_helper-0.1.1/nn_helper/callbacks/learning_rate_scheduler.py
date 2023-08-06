"""Contains callback for custom learning rate schedulers."""
from typing import Dict, Union

from nn_helper.callbacks.base_callback import BaseCallback


class LRBatchDecay(BaseCallback):
    """Learning rate decay per batch iteration."""

    def __init__(self, lr: float, lr_decay: float, batch_count: int = 0):
        """Initialise the LRBatchDecay instance.

        Args:
            lr (float): The learning rate that has been set in the optimizer.
            lr_decay (float): The amount of decay per batch.
            batch_count (int, optional): The total number of batches over epochs. Defaults to 0.
        """
        super().__init__()
        self.lr = lr
        self.lr_decay = lr_decay
        self.batch_count = batch_count

    def on_batch_begin(self, batch_index: int, logs: Dict[str, Union[int, float]] = None) -> None:
        """Decays the learning rate in the optimizer before every batch begins.

        Args:
            batch_index (int): The batch number within an epoch.
            logs (Dict[str, Union[int, float]], optional): The logs. Defaults to None.
        """
        self.batch_count += 1

        new_lr = self.lr / (1.0 + self.lr_decay * self.batch_count)

        for param_group in self.params["optimizer"].param_groups:
            param_group["lr"] = new_lr
