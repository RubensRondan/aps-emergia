from model.banco import BancoDados
from model.calculo import CalculoEmergetico
from model.importador import ImportadorCSV
from model.grafico import GraficoEmergetico
from model.relatorio import RelatorioPDF

from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox
)


class TelaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Sistema de Cálculo Emergético"
        )

        self.setGeometry(
            200,
            200,
            800,
            500
        )

        # Estilo geral
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
            }
        """)

        # Classes do sistema
        self.importador = ImportadorCSV()
        self.calculo = CalculoEmergetico()
        self.banco = BancoDados()
        self.grafico = GraficoEmergetico()
        self.relatorio = RelatorioPDF()

        # Título
        self.titulo = QLabel(
            "Sistema de Cálculo Emergético"
        )

        self.titulo.setFont(
            QFont("Arial", 18, QFont.Bold)
        )

        # Botões
        self.botao_importar = QPushButton(
            "Importar CSV"
        )

        self.botao_calcular = QPushButton(
            "Calcular Emergia"
        )

        self.botao_pdf = QPushButton(
            "Gerar Relatório PDF"
        )

        # Altura dos botões
        self.botao_importar.setMinimumHeight(40)
        self.botao_calcular.setMinimumHeight(40)
        self.botao_pdf.setMinimumHeight(40)

        # Estilo dos botões
        estilo_botao = """
            QPushButton {
                background-color: #2E86DE;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1B4F72;
            }
        """

        self.botao_importar.setStyleSheet(
            estilo_botao
        )

        self.botao_calcular.setStyleSheet(
            estilo_botao
        )

        self.botao_pdf.setStyleSheet(
            estilo_botao
        )

        # Eventos
        self.botao_importar.clicked.connect(
            self.importar_csv
        )

        self.botao_calcular.clicked.connect(
            self.calcular_emergia
        )

        self.botao_pdf.clicked.connect(
            self.gerar_relatorio
        )

        # Tabela
        self.tabela = QTableWidget()

        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels([
            "Recurso",
            "Energia",
            "Transformidade",
            "Emergia"
        ])

        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #dcdde1;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #2E86DE;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)

        # Resultado
        self.resultado = QLabel(
            "Emergia Total: 0"
        )

        self.resultado.setFont(
            QFont("Arial", 14, QFont.Bold)
        )

        # Layout
        layout = QVBoxLayout()

        layout.setSpacing(15)

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.addWidget(self.titulo)
        layout.addWidget(self.botao_importar)
        layout.addWidget(self.tabela)
        layout.addWidget(self.botao_calcular)
        layout.addWidget(self.botao_pdf)
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

            dados = self.importador.importar(
                caminho_arquivo
            )

            self.tabela.setRowCount(
                len(dados)
            )

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

        if self.tabela.rowCount() == 0:

            QMessageBox.warning(
                self,
                "Aviso",
                "Importe um arquivo CSV primeiro."
            )

            return

        lista_emergias = []
        lista_recursos = []

        for linha in range(
            self.tabela.rowCount()
        ):

            try:

                item_recurso = self.tabela.item(
                    linha,
                    0
                )

                item_energia = self.tabela.item(
                    linha,
                    1
                )

                item_transformidade = self.tabela.item(
                    linha,
                    2
                )

                if (
                    item_recurso is None
                    or item_energia is None
                    or item_transformidade is None
                ):

                    QMessageBox.warning(
                        self,
                        "Erro",
                        f"Dados incompletos na linha {linha + 1}"
                    )

                    return

                recurso = item_recurso.text()

                energia = float(
                    item_energia.text()
                )

                transformidade = float(
                    item_transformidade.text()
                )

                emergia = self.calculo.calcular_emergia(
                    energia,
                    transformidade
                )

                self.banco.salvar_calculo(
                    recurso,
                    energia,
                    transformidade,
                    emergia
                )

                lista_recursos.append(
                    recurso
                )

                lista_emergias.append(
                    emergia
                )

                self.tabela.setItem(
                    linha,
                    3,
                    QTableWidgetItem(
                        str(emergia)
                    )
                )

            except ValueError:

                QMessageBox.warning(
                    self,
                    "Erro",
                    f"Valores inválidos na linha {linha + 1}"
                )

                return

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

        QMessageBox.information(
            self,
            "Sucesso",
            "Cálculo emergético realizado com sucesso."
        )

    def gerar_relatorio(self):

        if self.tabela.rowCount() == 0:

            QMessageBox.warning(
                self,
                "Aviso",
                "Nenhum dado disponível para gerar relatório."
            )

            return

        recursos = []
        energias = []
        transformidades = []
        emergias = []

        for linha in range(
            self.tabela.rowCount()
        ):

            item_recurso = self.tabela.item(
                linha,
                0
            )

            item_energia = self.tabela.item(
                linha,
                1
            )

            item_transformidade = self.tabela.item(
                linha,
                2
            )

            item_emergia = self.tabela.item(
                linha,
                3
            )

            if (
                item_recurso is None
                or item_energia is None
                or item_transformidade is None
                or item_emergia is None
            ):

                QMessageBox.warning(
                    self,
                    "Erro",
                    f"Dados incompletos na linha {linha + 1}"
                )

                return

            recursos.append(
                item_recurso.text()
            )

            energias.append(
                item_energia.text()
            )

            transformidades.append(
                item_transformidade.text()
            )

            emergias.append(
                item_emergia.text()
            )

        emergia_total = (
            self.resultado.text()
        )

        self.relatorio.gerar(
            recursos,
            energias,
            transformidades,
            emergias,
            emergia_total
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Relatório PDF gerado com sucesso."
        )