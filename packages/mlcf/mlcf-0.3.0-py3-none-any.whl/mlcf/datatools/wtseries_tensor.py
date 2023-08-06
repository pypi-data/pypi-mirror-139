import numpy as np
from pathlib import Path
from typing import Callable

from torch.utils.data import TensorDataset
from torch.utils.data.dataloader import DataLoader
from torch import Tensor, tensor

# MLCF modules
from mlcf.datatools.wtseries_training import Partition, Field, WTSeriesTraining


class WTSeriesTensor(TensorDataset):
    def __init__(self,
                 partition: Partition,
                 ts_data: WTSeriesTraining = None,
                 dir_ts_data: Path = None,
                 transform_x: Callable = None,
                 transform_y: Callable = None,
                 *args, **kwargs):
        """WTSeriesTensor provide an indexer on time series tensor data which is compatible
        to a dataloader use in machine learning traning

        Args:
            partition (str): the part 'train', 'validation' or 'test'
            ts_data (WTSeriesTraining, optional): 'The time series data'. Defaults to None.
            dir_ts_data (Path, optional): 'the dir to the time series file'. Defaults to None.

        Raises:
            ValueError: You should to have a WTSeriesTraining (ts_data) or at least the dir to a
            TimeSeries (dir_ts_data)
            NotImplementedError: read a time serie data from a file is not implemented yet
            Warning: read a time serie data from a file is not implemented yet
        """
        self.input_data: Tensor
        self.target_data: Tensor
        self.partition = partition
        self.transform_x = transform_x
        self.transform_y = transform_y

        if ts_data is None and dir_ts_data is None:
            raise ValueError("You should to have a WTSeriesTraining (ts_data) or " +
                             "at least the dir to a TimeSeries (dir_ts_data).")
        if dir_ts_data is not None and ts_data is None:
            raise NotImplementedError("read a time serie data from a file is not implemented yet")
        if ts_data is not None:
            if dir_ts_data is not None:
                raise Warning("read a time serie data from a file is not implemented yet")
            self.ts_data: WTSeriesTraining = ts_data
        if len(self.ts_data) == 0:
            raise ValueError("WTSeriesTraining has a length of 0. It is empty")

        self.ts_data_to_tensor(self.partition, transform_x=transform_x, transform_y=transform_y)

        super(WTSeriesTensor, self).__init__(*[self.input_data, self.target_data])

    def x_size(self):
        return self.input_data.size()

    def y_size(self):
        return self.target_data.size()

    def __len__(self):
        if self.input_data is not None:
            return len(self.input_data)
        return self.ts_data.len(part=self.partition)

    def ts_data_to_tensor(self,
                          partition: Partition,
                          transform_x: Callable = None,
                          transform_y: Callable = None):
        self.input_data = tensor(np.array(self.ts_data(partition,
                                                       Field.INPUT)).astype(np.float32))
        self.target_data = tensor(np.array(self.ts_data(partition,
                                                        Field.TARGET)).astype(np.float32))
        self.transform_data(transform_x, transform_y)

    def get_dataloader(self, *args, **kwargs):
        return DataLoader(self, *args, **kwargs)

    def transform_data(self,
                       transform_x: Callable = None,
                       transform_y: Callable = None):
        if transform_x is not None:
            self.input_data = transform_x(self.input_data)
        if transform_y is not None:
            self.target_data = transform_y(self.target_data)

    def copy(self):
        return WTSeriesTensor(self.partition,
                              ts_data=self.ts_data,
                              dir_ts_data=None,
                              transform_x=self.transform_x,
                              transform_y=self.transform_y)
