from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from datetime import datetime


class RelatorioPDF:

    def gerar(
        self,
        recursos,
        energias,
        transformidades,
        emergias,
        emergia_total
    ):

        nome_arquivo = (
            "relatorios/relatorio_emergia.pdf"
        )

        pdf = canvas.Canvas(
            nome_arquivo,
            pagesize=letter
        )

        pdf.setFont("Helvetica-Bold", 16)

        pdf.drawString(
            50,
            750,
            "Relatório de Cálculo Emergético"
        )

        pdf.setFont("Helvetica", 10)

        pdf.drawString(
            50,
            730,
            f"Data: {datetime.now()}"
        )

        y = 680

        pdf.drawString(50, y, "Recurso")
        pdf.drawString(200, y, "Energia")
        pdf.drawString(320, y, "Transformidade")
        pdf.drawString(470, y, "Emergia")

        y -= 20

        for i in range(len(recursos)):

            pdf.drawString(
                50,
                y,
                str(recursos[i])
            )

            pdf.drawString(
                200,
                y,
                str(energias[i])
            )

            pdf.drawString(
                320,
                y,
                str(transformidades[i])
            )

            pdf.drawString(
                470,
                y,
                str(emergias[i])
            )

            y -= 20

        y -= 20

        pdf.setFont("Helvetica-Bold", 12)

        pdf.drawString(
            50,
            y,
            f"Emergia Total: {emergia_total} sej"
        )

        pdf.save()