import pandas as pd

from Service.DataService import DataService


class Statistics:
    def generation_df_impact_frecuency(self, directory):
        d = DataService( ).data( )
        new_df = pd.DataFrame(d)
        return new_df
    '''
    Crea un nuevo dataFrame donde las columnas a utilizar son la severdidad= impactoV1 * frecuenciaV1 de cada variable(Vn)
    @params
    start_col: indica de la encuesta en que posición de columna empiezan las variables a tratar
    '''

    def gerenation_df_severity(self, start_col, dataUpload):
        d = DataService( )
        if type(dataUpload) is str:
            dataUpload = pd.DataFrame(d.data())
            print('Entro')
        list_title = list(d.file_variables_title())
        full_set_df = dataUpload
        new_df = pd.DataFrame()
        new_df[list_title[0]] = full_set_df.iloc[:, start_col] * full_set_df.iloc[:, (start_col - 1) + 2]
        for col in range(len(list_title) - 1):
            start_col = start_col + 1
            new_df[list_title[col + 1]] = full_set_df.iloc[:, start_col + 1] * full_set_df.iloc[:, start_col + 2]
        return new_df

    def frecuency_table(self, new_df):
        df = pd.DataFrame(new_df.describe())
        return df

    def shape(self, new_df):
        return new_df.shape()

    def title(self):
        df = pd.DataFrame(DataService( ).file_variables_title( ))
        return df

    def generate_titles(self):
        titles = []
        df_titles = Statistics().title()
        for i in df_titles:
            titles.append({'label': i, 'value': i})
        return titles

