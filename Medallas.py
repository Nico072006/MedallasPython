import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,Image
from reportlab.lib.styles import getSampleStyleSheet



def carga_datos(ruta):
    
    df = pd.read_csv(ruta)
    return df

def Datos_nulos(df):
    conteo_nulos=df.isna().sum()
    total_nulos=conteo_nulos.sum()

    if total_nulos >0:
        print(f"Alerta : Se Encontraron {total_nulos} valores nulos ")
        print(conteo_nulos[conteo_nulos>0])
        df.fillna(0,inplace=True)
        print("Casillas vacias rellenadas con 0")

    else:
        print("No se Encontraron datos nulos en el DataSet")
        return False

def duplicados (df,Pais):
    total_repetidos=df.duplicated(subset=[Pais]).sum()

    if total_repetidos >0:
        print(f"Alerta:Se Encontraron{total_repetidos} Paises repetidos en tu DataSet")
        
        #Eliminamos datos repetidos 

        df.drop_duplicates(subset=[Pais],keep='first',inplace=True)
        print(f"Se Borraron {total_repetidos} Datos repetidos")

    else:
        print(f"Se Encontraron registros repetidos en la columna {Pais}. ")
    
    return df

def Pais_Mas_Medallas (df):
    print ("-----Medalleria------")

    indice_gandor=df ['Total'].idxmax()
    pais_top =df.loc[indice_gandor,'Pais']
    medallas_top =df.loc[indice_gandor,'Total']


    print(f"El Pais con mas medallas en {pais_top} con {medallas_top } en total.")
    print("-" * 30)
   
    podio =df.sort_values(by='Total',ascending=False).head(5)

    print("\n")
    print("TABLA DE PAISES COM MAS MEDALLAS")
    print ("=======================================")
    print("\n")
    print("PODIO")
    print(podio[['Pais','Total']])

def Estadisticas_M_M_D(df):    
    moda = df['Total'].mode()[0]
    mediana =df['Total'].median()
    desviacion =df['Total'].std()

    print(f"Moda: {moda}")
    print(f"Mediana {mediana}")
    print(f"Desviacion {desviacion:.2f}")

def Probabilidades(df):
    total_paises =len(df)

    print ("---------PROBABILIDADES---------")

    Mas_10=len(df[df['Total']>10])
    Prob_10=(Mas_10 / total_paises)*100
    print (f"Probabilidad que un pais tenga mas de 10 medallas es de: \n{Prob_10:.2f}%")
    
    Mas_5=len(df[df['Oro']>5])
    Prob_oro=(Mas_5 /total_paises)*100
    print(f"Probabilidad de que un pais consiga mas de >5 medallas de oros es: \n{Prob_oro:.2f}%")


    Una=len(df[df['Total']>=1])
    Prob_una=(Una/total_paises)*100
    print (f"Probabilidad de tener al menos una medalla: \n{Prob_una:.2f}%")

def Posiciones(df):
    # Ordenar por total de medallas (Mayor a Menor)
    orden_total=df.sort_values(by='Total',ascending=False)

    #Mostrar el Top 5 general 
    print("Top 5 Medalleria")
    print (orden_total.head(5)[['Pais','Total']])

    # Mostrar el Top 5 por medallas de ORO

    orden_oro=df.sort_values(by='Oro',ascending=False)
    print(f"\n Top 5 Medalleria de Oro")
    print(orden_oro.head(5)[['Pais','Total']])

    #Identificar el país con menor cantidad de medallas
    Cantidad_Min =df['Total'].idxmin()
    pais_min=df.loc[Cantidad_Min,'Pais']
    Can_min=df.loc[Cantidad_Min,'Total']

    print(f" \n Pais con Menos Medallas")
    print(f"{pais_min} con solo {Can_min} medalla(s).")

def Graficos(df):
    #Crear columna de rendimiento ---
    def Rendiminetos(total):
        if total > 20: return 'Alto'
        elif total >= 10: return 'Medio'
        else: return 'Bajo'

    df['nivel_rendimiento'] = df['Total'].apply(Rendiminetos)
    
    #Mostrar cuántos países hay en cada categoría
    print("\nCONTEO POR NIVEL DE RENDIMIENTO:")
    print(df['nivel_rendimiento'].value_counts())

    #Generar Gráficos ---
    plt.figure(figsize=(12, 10))

    #Top 10 países por total
    plt.subplot(2, 2, 1)
    top_10 = df.sort_values('Total', ascending=False).head(10)
    sns.barplot(x='Total', y='Pais', data=top_10, palette='viridis')
    plt.title('Top 10 Países por Total de Medallas')

    #Medallas de oro por país (Top 10)
    plt.subplot(2, 2, 2)
    top_oro = df.sort_values('Oro', ascending=False).head(10)
    sns.barplot(x='Oro', y='Pais', data=top_oro, palette='Oranges_r')
    plt.title('Top 10 Medallas de Oro por País')

    #Distribución del total
    plt.subplot(2, 2, 3)
    sns.histplot(df['Total'], bins=15, kde=True, color='skyblue')
    plt.title('Distribución del Total de Medallas')

    #Comparación de medallas
    plt.subplot(2, 2, 4)
    sns.boxplot(x=df['Total'], color='lightgreen')
    plt.title('Medallas Totales')

    plt.savefig("graficos_medallas.png")
    print("Imagen de GRaficos Guardado como graficos_medallas.png")

    plt.tight_layout()
    plt.close()

    return df

def generar_pdf(df_datos,nombre_pdf):
    doc=SimpleDocTemplate(nombre_pdf)
    estilos=getSampleStyleSheet()
    elementos=[]

    elementos.append(Paragraph("Reporte de Medallas",estilos['Title']))
    elementos.append(Spacer(1,12))
    
    datos_lista=[df_datos.columns.tolist()]+df_datos.values.tolist()
    tabla=Table(datos_lista)
    elementos.append(tabla)
    elementos.append(Spacer(1,12))


    elementos.append(Paragraph("Graficos de Analisis",estilos['Heading2']))
    imagen = Image("graficos_medallas.png",width=400,height=400)
    elementos.append(imagen)
    elementos.append(Spacer(1,12))

    elementos.append(Paragraph("Conclusion",estilos['Heading2']))
    texto="!El PDF Muestra un pequeño resumen de la medalleria , Informacion relevante ,porcentajes,rendimientos y datos importantes que nos muestra una brecha importante entre paises.! "
    elementos.append(Paragraph(texto,estilos['Normal']))

    doc.build(elementos)
    print(f"PDF{nombre_pdf}")

def main():
    df = carga_datos("medallas.csv")
    print(df)

   
    print("\n")
    print ("=======================================")
    print("\n")

    print("INFORMACION DEL DATASET")
    print("\n")
    print ("=======================================")
    print("\n")
    #¿Cuántos registros hay?
    total_filas=len(df)
    print(f"El Archivo tiene {total_filas} registros")
    print("\n")
    print ("=======================================")
    print("\n")
    #¿Cuántas columnas tiene el dataset?
    total_columnas=len(df.columns)
    print(f"El Archivo tiene un total de {total_columnas} columnas")
    print("\n")
    print ("=======================================")
    print("\n")
    #¿Existen valores nulos?
    #Verificar y tratar valores nulos.
    Datos_nulos(df)
    print("\n")
    print ("=======================================")
    print("\n")
    #Eliminar registros duplicados si existen.
    df=duplicados(df,"Pais")
    print("\n")
    print ("=======================================")
    print("\n")
    #Recuento
    print(f"Registros finales después de limpieza: {len(df)}")
    print("\n")
    print ("=======================================")
    print("\n")
    #El país con más medallas de oro.
    #El país con más medallas en total.
    Pais_Mas_Medallas (df)
    print("\n")
    print ("=======================================")
    print("\n")
    #Promedio
    #Mediana
    #Desviación estándar
    print("Estadisticas DataSet")
    Estadisticas_M_M_D (df)
    print("\n")
    print ("=======================================")
    print("\n")
    Probabilidades(df)
    #Probabilidad de que un país tenga más de 10 medallas.
    #Probabilidad de que un país tenga más de 5 medallas de oro
    #Probabilidad de que un país tenga al menos una medalla
    print("\n")
    print ("=======================================")
    print("\n")
    #Ordenar los países por total de medallas (de mayor a menor).
    #Mostrar el Top 5.
    #Mostrar el Top 5 por medallas de oro.
    #Identificar el país con menor cantidad de medallas.
    Posiciones(df)
    print("\n")
    print ("=======================================")
    print("\n")
    #Gráfico de barras → Top 10 países por total de medallas.
    #Gráfico de barras → Medallas de oro por país.
    #Histograma → Distribución del total de medallas.
    #Boxplot → Comparación de medallas totales entre países.
    df=Graficos(df)
    print("\n")
    print ("=======================================")
    print("\n")
    #Crear un archivo EXCEL con:
    #País
    #Oro
    #Plata
    #Bronce
    #Total_medallas
    #Nivel_rendimiento
    columnas_internas=['Pais','Oro','Plata','Bronce','Total','nivel_rendimiento']
    df_excel=df[columnas_internas]

    df_excel.to_excel("Resumen_Medalleria.xlsx",index=False )
    print("Archivo Generado ")
    print("\n")
    print ("=======================================")
    print("\n")
    #Generar un PDF que contenga:
    #Título
    #Tabla resumen
    #gráficos
    #Conclusión escrita (mínimo 5 líneas)
    generar_pdf(df_excel,"Medalleria.pdf")





main ()