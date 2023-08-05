class DataLoader:
    def __init__(self, conf_file=None):
        self.data_dir = 'patchcomm/data/'
        self.test_inputs_dir = self.data_dir + 'test_inputs/'

    def _cleanUp(self, data):
        return [
            x for x in [y.strip() for y in data]
            if x is not ''
        ]

    def _load(self, dir, filename):
        with open(dir+filename, 'r') as f:
            return self._cleanUp(f.readlines())

    def loadTestPartialParses(self, test_partial_parses_filename):
        return self._load(self.test_inputs_dir, test_partial_parses_filename)
