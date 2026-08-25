import pandas as pd
import glob
import matplotlib.pyplot as plt
import os

# --------------------------------------------
# UBICACIÓN DEL PROYECTO
# --------------------------------------------

carpeta_proyecto = os.path.dirname(os.path.abspath(__file__))
carpeta_data = os.path.join(carpeta_proyecto, "Data")
carpeta_resultados = os.path.join(carpeta_proyecto, "Resultados")

# --------------------------------------------
# PARTE 1: Leer los archivos
# --------------------------------------------

archivos_csv = glob.glob(os.path.join(carpeta_data, "sucursal_*.csv"))
archivos_xlsx = glob.glob(os.path.join(carpeta_data, "sucursal_*.xlsx"))

print("Archivos CSV encontrados:")
for archivo in archivos_csv:
    print(archivo)

print("\nArchivos Excel encontrados:")
for archivo in archivos_xlsx:
    print(archivo)

lista_informes = []

# Leer archivos CSV
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_informes.append(df)

# Leer archivos Excel
for archivo in archivos_xlsx:
    df = pd.read_excel(archivo, engine="openpyxl")
    lista_informes.append(df)

# --------------------------------------------
# Verificar archivos
# --------------------------------------------

if not lista_informes:
    print("\nERROR: No se encontraron archivos.")
    print("La carpeta buscada fue:")
    print(carpeta_data)
    exit()

print("\nTotal de archivos cargados:", len(lista_informes))

# --------------------------------------------
# PARTE 2: Renombrar columnas
# --------------------------------------------
df_consolidado = pd.concat(lista_informes, ignore_index=True)

for i, df in enumerate(lista_informes):

    if "Fecha_Venta" in df.columns:
        lista_informes[i] = df.rename(columns={
            "Fecha_Venta": "fecha",
            "Producto": "producto",
            "Categoria": "categoria",
            "Cant": "cantidad",
            "Valor_Unitario": "precio_unitario",
            "Vendedor": "vendedor",
            "Pago": "metodo_pago"
        })

# --------------------------------------------
# Consolidar
# --------------------------------------------

df_consolidado = pd.concat(lista_informes, ignore_index=True)

# --------------------------------------------
# PARTE 3: Limpieza
# --------------------------------------------

df_consolidado = df_consolidado.drop_duplicates()

df_consolidado["metodo_pago"] = df_consolidado[
    "metodo_pago"
].fillna("No especificado")

promedio_precio = df_consolidado["precio_unitario"].mean()

df_consolidado["precio_unitario"] = df_consolidado[
    "precio_unitario"
].fillna(promedio_precio)

# Crear carpeta Resultados
os.makedirs(carpeta_resultados, exist_ok=True)

# Guardar Excel
df_consolidado.to_excel(
    os.path.join(carpeta_resultados, "consolidado_limpio.xlsx"),
    index=False
)

# --------------------------------------------
# PARTE 4: Gráfico por categoría
# --------------------------------------------

ventas_categoria = df_consolidado.groupby(
    "categoria"
)["precio_unitario"].sum()

ventas_categoria.plot(
    kind="bar",
    title="Ventas por Categoría"
)

plt.xlabel("Categoría")
plt.ylabel("Total de ventas")
plt.tight_layout()

plt.savefig(
    os.path.join(carpeta_resultados, "grafico_categoria.png")
)

plt.show()
plt.close()

# --------------------------------------------
# PARTE 5: Gráfico por vendedor
# --------------------------------------------

ventas_vendedor = df_consolidado.groupby(
    "vendedor"
)["precio_unitario"].sum()

ventas_vendedor.plot(
    kind="pie",
    autopct="%1.1f%%",
    title="Participación por Vendedor"
)

plt.ylabel("")
plt.tight_layout()

plt.savefig(
    os.path.join(carpeta_resultados, "grafico_vendedor.png")
)

plt.show()
plt.close()

# --------------------------------------------
# FINAL
# --------------------------------------------

print("\n--------------------------------------------")
print("Proceso completo.")
print("Los resultados están en la carpeta Resultados/")
print("--------------------------------------------")