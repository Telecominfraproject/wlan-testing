#!/usr/bin/env pythonn3

import pandas as pd

class pandas_extensions:

    # ================ Pandas Dataframe Functions ======================================

    # takes any dataframe and returns the specified file extension of it
    def df_to_file(self, output_f=None, dataframe=None, save_path=None):
        if output_f.lower() == 'hdf':
            dataframe.to_hdf(save_path.replace('csv', 'h5', 1), 'table', append=True)
        if output_f.lower() == 'parquet':
            dataframe.to_parquet(save_path.replace('csv', 'parquet', 1), engine='pyarrow')
        if output_f.lower() == 'png':
            fig = dataframe.plot().get_figure()
            fig.savefig(save_path.replace('csv', 'png', 1))
        if output_f.lower() == 'xlsx':
            dataframe.to_excel(save_path.replace('csv', 'xlsx', 1))
        if output_f.lower() == 'json':
            dataframe.to_json(save_path.replace('csv', 'json', 1))
        if output_f.lower() == 'stata':
            dataframe.to_stata(save_path.replace('csv', 'dta', 1))
        if output_f.lower() == 'pickle':
            dataframe.to_pickle(save_path.replace('csv', 'pkl', 1))
        if output_f.lower() == 'html':
            dataframe.to_html(save_path.replace('csv', 'html', 1))

    # takes any format of a file and returns a dataframe of it
    def file_to_df(self, file_name):
        if file_name.split('.')[-1] == 'csv':
            return pd.read_csv(file_name)

    # only works for test_ipv4_variable_time at the moment
    def compare_two_df(self, dataframe_one=None, dataframe_two=None):
        # df one = current report
        # df two = compared report
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        # get all of common columns besides Timestamp, Timestamp milliseconds
        common_cols = list(set(dataframe_one.columns).intersection(set(dataframe_two.columns)))
        cols_to_remove = ['Timestamp milliseconds epoch', 'Timestamp', 'LANforge GUI Build: 5.4.3']
        com_cols = [i for i in common_cols if i not in cols_to_remove]
        # check if dataframes have the same endpoints
        if dataframe_one.name.unique().tolist().sort() == dataframe_two.name.unique().tolist().sort():
            endpoint_names = dataframe_one.name.unique().tolist()
            if com_cols is not None:
                dataframe_one = dataframe_one[[c for c in dataframe_one.columns if c in com_cols]]
                dataframe_two = dataframe_two[[c for c in dataframe_one.columns if c in com_cols]]
                dataframe_one = dataframe_one.loc[:, ~dataframe_one.columns.str.startswith('Script Name:')]
                dataframe_two = dataframe_two.loc[:, ~dataframe_two.columns.str.startswith('Script Name:')]
                lowest_duration = min(dataframe_one['Duration elapsed'].max(), dataframe_two['Duration elapsed'].max())
                print("The max duration in the new dataframe will be... " + str(lowest_duration))

                compared_values_dataframe = pd.DataFrame(
                    columns=[col for col in com_cols if not col.startswith('Script Name:')])
                cols = compared_values_dataframe.columns.tolist()
                cols = sorted(cols, key=lambda L: (L.lower(), L))
                compared_values_dataframe = compared_values_dataframe[cols]
                print(compared_values_dataframe)
                for duration_elapsed in range(lowest_duration):
                    for endpoint in endpoint_names:
                        # check if value has a space in it or is a str.
                        # if value as a space, only take value before space for calc, append that calculated value after space.
                        # if str. check if values match from 2 df's. if values do not match, write N/A
                        for_loop_df1 = dataframe_one.loc[(dataframe_one['name'] == endpoint) & (
                                    dataframe_one['Duration elapsed'] == duration_elapsed)]
                        for_loop_df2 = dataframe_two.loc[(dataframe_one['name'] == endpoint) & (
                                    dataframe_two['Duration elapsed'] == duration_elapsed)]
                        # print(for_loop_df1)
                        # print(for_loop_df2)
                        cols_to_loop = [i for i in com_cols if
                                        i not in ['Duration elapsed', 'Name', 'Script Name: test_ipv4_variable_time']]
                        cols_to_loop = sorted(cols_to_loop, key=lambda L: (L.lower(), L))
                        print(cols_to_loop)
                        row_to_append = {}
                        row_to_append["Duration elapsed"] = duration_elapsed
                        for col in cols_to_loop:
                            print(col)
                            print(for_loop_df1)
                            # print(for_loop_df2)
                            print(for_loop_df1.at[0, col])
                            print(for_loop_df2.at[0, col])
                            if type(for_loop_df1.at[0, col]) == str and type(for_loop_df2.at[0, col]) == str:
                                if (' ' in for_loop_df1.at[0, col]):
                                    # do subtraction
                                    new_value = float(for_loop_df1.at[0, col].split(" ")[0]) - float(
                                        for_loop_df2.at[0, col].split(" ")[0])
                                    # add on last half of string
                                    new_value = str(new_value) + for_loop_df2.at[0, col].split(" ")[1]
                                    # print(new_value)
                                    row_to_append[col] = new_value
                                else:
                                    if for_loop_df1.at[0, col] != for_loop_df2.at[0, col]:
                                        row_to_append[col] = 'NaN'
                                    else:
                                        row_to_append[col] = for_loop_df1.at[0, col]
                            elif type(for_loop_df1.at[0, col]) == int and type(for_loop_df2.at[0, col]) == int or type(
                                    for_loop_df1.at[0, col]) == float and type(for_loop_df2.at[0, col]) == float:
                                new_value = for_loop_df1.at[0, col] - for_loop_df2.at[0, col]
                                row_to_append[col] = new_value
                        compared_values_dataframe = compared_values_dataframe.append(row_to_append, ignore_index=True, )
                        print(compared_values_dataframe)
                    # add col name to new df
                print(dataframe_one)
                print(dataframe_two)
                print(compared_values_dataframe)
            else:
                ValueError("Unable to execute report comparison due to inadequate file commonalities. ")
                exit(1)
        else:
            ValueError(
                "Two files do not have the same endpoints. Please try file comparison with files that have the same endpoints.")
            exit(1)

        # take those columns and separate those columns from others in DF.

        pass
        # return compared_df
