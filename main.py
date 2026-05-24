import sys

from PyQt5.QtWidgets import QApplication

from view.tela_principal import TelaPrincipal

app = QApplication(sys.argv)

janela = TelaPrincipal()
janela.show()

sys.exit(app.exec_())