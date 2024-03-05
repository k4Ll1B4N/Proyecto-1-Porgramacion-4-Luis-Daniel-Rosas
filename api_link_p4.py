import pandas as pd
from sodapy import Socrata
import numpy as np

def crear_lista_departamentos():                        
    
    client = Socrata("www.datos.gov.co", None)          
    results = client.get("ch4u-f3i5")                   
    results_df = pd.DataFrame.from_records(results)     
                                                        
    nombre_lista = list(results_df["departamento"]) 
                                                        
    
    return nombre_lista                                 

def calcular_mediana_edaficas(data):
    try:
        #eliminar caracteres especiales
        data['potasio_k_intercambiable_cmol_kg'] = data['potasio_k_intercambiable_cmol_kg'].str.replace('[<>]', '', regex=True)
        data['f_sforo_p_bray_ii_mg_kg'] = data['f_sforo_p_bray_ii_mg_kg'].str.replace('[<>]', '', regex=True)
        data['ph_agua_suelo_2_5_1_0'] = data['ph_agua_suelo_2_5_1_0'].str.replace('[<>]', '', regex=True)

        #cambiar "," por "." 
        data['potasio_k_intercambiable_cmol_kg'] = data['potasio_k_intercambiable_cmol_kg'].str.replace(',', '.', regex=True)
        data['f_sforo_p_bray_ii_mg_kg'] = data['f_sforo_p_bray_ii_mg_kg'].str.replace(',', '.', regex=True)
        data['ph_agua_suelo_2_5_1_0'] = data['ph_agua_suelo_2_5_1_0'].str.replace(',', '.', regex=True)
        
        #convertir a nuemros
        data['potasio_k_intercambiable_cmol_kg'] = pd.to_numeric(data['potasio_k_intercambiable_cmol_kg'].astype(float))
        data['f_sforo_p_bray_ii_mg_kg'] = pd.to_numeric(data['f_sforo_p_bray_ii_mg_kg'].astype(float))
        data['ph_agua_suelo_2_5_1_0'] = pd.to_numeric(data['ph_agua_suelo_2_5_1_0'].astype(float))

        #eliminar valores nulos
        data['potasio_k_intercambiable_cmol_kg'] = data['potasio_k_intercambiable_cmol_kg'].fillna(np.nan)
        data['f_sforo_p_bray_ii_mg_kg'] = data['f_sforo_p_bray_ii_mg_kg'].fillna(np.nan)
        data['ph_agua_suelo_2_5_1_0'] = data['ph_agua_suelo_2_5_1_0'].fillna(np.nan)

        data = data.dropna(subset=['f_sforo_p_bray_ii_mg_kg', 'ph_agua_suelo_2_5_1_0', 'potasio_k_intercambiable_cmol_kg'])  # último filtro para evitar errores inesperados
        
        mediana_edaficas = data[['f_sforo_p_bray_ii_mg_kg', 'ph_agua_suelo_2_5_1_0', 'potasio_k_intercambiable_cmol_kg']].apply(lambda x: np.median(x), axis=0)

        return mediana_edaficas

    except Exception as e:
        print(f"Error al calcular la mediana de las variables edáficas: {str(e)}")
        return None

def api (nombre_departamento, limite_registros):                                                        
    
    client = Socrata("www.datos.gov.co", None)                                                           
    results = client.get("ch4u-f3i5", departamento = nombre_departamento, limit = limite_registros) 
    results_df = pd.DataFrame.from_records(results)                                                     
    
    mediana = calcular_mediana_edaficas(results_df)

    results_df.rename(columns={"departamento": "Departamento"}, inplace=True)                       
    results_df.rename(columns={"municipio": "Municipio"}, inplace=True)                            
    results_df.rename(columns={"cultivo": "Cultivo"}, inplace=True)                                 
    results_df.rename(columns={"ph_agua_suelo_2_5_1_0": "Ph"}, inplace=True)                                
    results_df.rename(columns={"f_sforo_p_bray_ii_mg_kg": "Fosforo"}, inplace=True)
    results_df.rename(columns={"potasio_k_intercambiable_cmol_kg": "Potasio"}, inplace=True)

    if 'topografia' not in results_df:                                                           
        results_df['Topografia'] = "Pendiente"                                                           
    else:                                                                                               
        results_df.rename(columns={"'topografia'": "Topografia"}, inplace=True)

    results_df = results_df[["Departamento", "Municipio", "Cultivo", "topografia", "Ph", "Fosforo", "Potasio"]] # Se le da el formato al dataframe para que muestre las columnas que se requieren
    
    print(results_df.to_string(index = False)) #Imprime en la consola el dataframe

    print(mediana)


    


