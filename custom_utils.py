import pandas as pd
import matplotlib.pyplot as plt

def mostrar_tabla(df):
    # Crear la figura
    fig, ax = plt.subplots(figsize=(12, len(df) * 0.5 + 1))  # Auto-ajuste de altura
    ax.axis('off')  # Oculta ejes

    # Crear la tabla
    tabla = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center'
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.2)

    plt.title("Visualización de Individuo", fontsize=14, weight='bold')
    plt.tight_layout()
    # Mostrar tabla
    plt.show()