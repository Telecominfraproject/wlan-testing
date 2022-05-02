from tabulate import tabulate
import pandas as pd

class Report:
    def __init__(self, key1=None,
                 key2=None,
                 val1=None,
                 val2=None):
        self.key1 = key1
        self.key2 = key2
        self.val1 = val1
        self.val2 = val2

    def table1(self):
        table ={str(self.key1): self.val1,  str(self.key2):self.val2}
        x = tabulate(table, headers="keys", tablefmt="fancy_grid")
        return x

    def table2(self, table):
        self.table = table
        x = tabulate(self.table, headers='firstrow', tablefmt='fancy_grid')
        return x


    def table_pandas(self, csv_file=None):
        data = pd.read_csv(str(csv_file))
        df = pd.DataFrame(data)
        return df