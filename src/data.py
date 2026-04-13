from minicamels import MiniCamels
from torch.utils.data import IterableDataset, DataLoader

def get_attrs():
    mc = MiniCamels()
    return mc.attributes()


class CamelsDataset(IterableDataset):
    def __init__(
        self,
        in_vars = ['prcp', 'tmin', 'tmax', 'srad'],
        out_vars = ['qobs'],
        time_selection=slice('1980-01-01', '2010-12-31'),
        seq_len = 365,
        pred_len = 1
    ):
        super().__init__()
        self.in_vars = in_vars
        self.out_vars = out_vars
        self.seq_len = seq_len
        self.pred_len = pred_len
        self.mc = MiniCamels()
        self.data= self.mc.load_all().sel(time=time_selection)
        self.data = self.normalize_data(self.data)

    def normalize_data(self, data):
        pass

    def __iter__(self ):
        # Pull out (x, y) pairs for a single sample
        for basin_id in self.data.basin.values:
            bd = self.data.sel(basin=basin_id)
            x = bd[self.in_vars].values
            y = bd[self.out_vars].values
            # Pull out subsequences of length seq_len for x and pred_len for y  
            for i in range(len(bd) - self.seq_len - self.pred_len + 1):
                x_seq = x[i:i+self.seq_len]
                y_seq = y[i+self.seq_len:i+self.seq_len+self.pred_len]
                yield x_seq, y_seq
