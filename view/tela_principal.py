from model.grafico import GraficoEmergetico
from model.banco import BancoDados
from model.calculo import CalculoEmergetico
from model.importador import ImportadorCSV

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog
)


class TelaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Cálculo Emergético")
        self.setGeometry(200, 200, 800, 500)

        # Classes do sistema
        self.importador = ImportadorCSV()
        self.calculo = CalculoEmergetico()
        self.banco = BancoDados()
        self.grafico = GraficoEmergetico()

        # Título
        self.titulo = QLabel("Sistema de Cálculo Emergético")

        # Botões
        self.botao_importar = QPushButton("Importar CSV")
        self.botao_calcular = QPushButton("Calcular Emergia")

        # Eventos
        self.botao_importar.clicked.connect(self.importar_csv)
        self.botao_calcular.clicked.connect(self.calcular_emergia)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels([
            "Recurso",
            "Energia",
            "Transformidade",
            "Emergia"
        ])

        # Resultado
        self.resultado = QLabel("Emergia Total: 0")

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(self.titulo)
        layout.addWidget(self.botao_importar)
        layout.addWidget(self.tabela)
        layout.addWidget(self.botao_calcular)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def importar_csv(self):

        caminho_arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar CSV",
            "",
            "Arquivos CSV (*.csv)"
        )

        if caminho_arquivo:

            dados = self.importador.importar(caminho_arquivo)

            self.tabela.setRowCount(len(dados))

            for linha in range(len(dados)):

                self.tabela.setItem(
                    linha,
                    0,
                    QTableWidgetItem(
                        str(dados.iloc[linha, 0])
                    )
                )

                self.tabela.setItem(
                    linha,
                    1,
                    QTableWidgetItem(
                        str(dados.iloc[linha, 1])
                    )
                )

                self.tabela.setItem(
                    linha,
                    2,
                    QTableWidgetItem(
                        str(dados.iloc[linha, 2])
                    )
                )

    def calcular_emergia(self):

        lista_emergias = []
        lista_recursos = []

        for linha in range(self.tabela.rowCount()):

            energia = float(
                self.tabela.item(linha, 1).text()
            )

            transformidade = float(
                self.tabela.item(linha, 2).text()
            )

            emergia = self.calculo.calcular_emergia(
                energia,
                transformidade
            )

            recurso = self.tabela.item(
                linha,
                0
            ).text()
            lista_recursos.append(recurso)

            self.banco.salvar_calculo(
                recurso,
                energia,
                transformidade,
                emergia
            )

            lista_emergias.append(emergia)

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(str(emergia))
            )

        emergia_total = self.calculo.calcular_total(
            lista_emergias
        )

        self.resultado.setText(
            f"Emergia Total: {emergia_total} sej"
        )
        self.grafico.gerar_grafico(
    lista_recursos,
    lista_emergias
)