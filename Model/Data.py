import pandas as pd
from sklearn import datasets


class Data:
    x, y = datasets.make_moons(
        n_samples=200,
        noise=0.6,
        random_state=0
    )
    df_X = pd.DataFrame(datasets.make_moons(
        n_samples=200,
        noise=0.6,
        random_state=0
    ))

    def __init__(self):
        self.df_X = Data.x



    def get_df_X(self):
            return self.df_X

    def set_df_X(self, df_X):
            self.df = df_X
            return df_X

    # Recibe el archivo en formato csv de los resultados de la encuesta
    def data(self):
        file = pd.read_csv('D:\IngenieriadeSistemas\TrabajodeGrado\prueba.csv',
                           encoding='unicode_escape')
        return file

    # Recibe el archivo en formato csv de los titulos para el nuevo DataFrame
    def file_variables_title(self):
        file = pd.read_csv('D:\IngenieriadeSistemas\TrabajodeGrado\dataTituloVariables.csv',
                           encoding='unicode_escape')
        return file
