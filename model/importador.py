import pandas as pd

class ImportadorCSV:

    def importar(self, caminho_arquivo):
        dados = pd.read_csv(caminho_arquivo)
        return dados