import matplotlib.pyplot as plt


class GraficoEmergetico:

    def gerar_grafico(
        self,
        recursos,
        emergias
    ):

        plt.figure(figsize=(10, 6))

        plt.bar(
            recursos,
            emergias
        )

        plt.title(
            "Emergia por Recurso"
        )

        plt.xlabel(
            "Recursos"
        )

        plt.ylabel(
            "Emergia (sej)"
        )

        plt.xticks(rotation=15)

        plt.tight_layout()

        plt.show()