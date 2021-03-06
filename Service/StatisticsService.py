import pandas as pd
import numpy as np
from Model.Statistics import Statistics
from Model.Data import Data as data

# Gestiona la data proveniente del archivo excel
class StatisticsController:
    def get_allData(dataUpload):
        s = Statistics()
        df = s.gerenation_df_severity(6, dataUpload)
        return df

    def generate_statistics(self, dataUpload):
        s = Statistics()
        df = s.gerenation_df_severity(0, dataUpload)
        df_frec = s.frecuency_table(df)
        return df_frec

    def get_graphs_dispersion(self, nameX, nameY):
        df = StatisticsController.get_allData(data.df_X)
        df_dispersion = pd.merge(df[nameX], df[nameY], left_on=nameX, right_on=nameY)
        return df_dispersion




