from stonewave.sql.udtfs.base_function import BaseFunction
import pyarrow as pa
import pandas as pd


class PivotTableFunction(BaseFunction):
    def __init__(self):
        self.tables = []
        self.x_field = None
        self.y_name_field = None
        self.y_data_fields = None

    def get_name(self):
        return "pivot_table"

    def process(self, params, table_writer, context):
        if self.x_field == None and len(params) < 4:
            raise Exception(
                "Table function 'pivot_table' parameter invalid: "
                "parameter should be (data_set_name, index_field, "
                "column_name, column_values)"
            )
        batch = params[0]
        if batch is not None:
            self.x_field = params[1]
            self.y_name_field = params[2]
            self.y_data_fields = list(map(str.strip, params[3].split(",")))
            table = pa.Table.from_batches([batch])
            self.tables.append(table)
        else:
            self.pivot(table_writer)

    def pivot(self, table_writer):
        if self.tables:
            table = pa.concat_tables(self.tables, promote=True)
            df = table.to_pandas()
            pvt = pd.pivot_table(
                df,
                values=self.y_data_fields,
                index=self.x_field,
                columns=self.y_name_field,
            )
            pvt.columns = ["{}${}".format(x[0], x[1]) for x in pvt.columns]
            pvt = pvt.reset_index()
            table = pa.Table.from_pandas(pvt, preserve_index=False)
            batches = table.to_batches()
            table_writer.table_batch_iterator = iter(batches)
        else:
            return
