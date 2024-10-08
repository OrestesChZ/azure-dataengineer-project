# Databricks notebook source
dbutils.fs.ls('mnt/silver/SalesLT/')

# COMMAND ----------

dbutils.fs.ls('mnt/gold/')

# COMMAND ----------

input_path = '/mnt/silver/SalesLT/Address/'

# COMMAND ----------

df = spark.read.format('delta').load(input_path)

# COMMAND ----------

display(df)

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# Get the list of column names
column_names = df.columns

for old_col_name in column_names:
    # Convert column name from ColumnName to Column_Name format
    new_col_name = "".join(["_" + char if char.isupper() and not old_col_name[i - 1].isupper() else char for i, char in enumerate(old_col_name)]).lstrip("_")
    
    # Change the column name using withColumnRenamed
    df = df.withColumnRenamed(old_col_name, new_col_name)

# COMMAND ----------

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Doing transformations for all tables (Changing column names)

# COMMAND ----------

table_name = []

for i in dbutils.fs.ls('/mnt/silver/SalesLT/'):
    table_name.append(i.name.split('/')[0])

# COMMAND ----------

table_name

# COMMAND ----------

for name in table_name:
    path = '/mnt/silver/SalesLT/' + name
    print(path)
    df = spark.read.format('delta').load(path)

    # Obtener la lista de nombres de columnas
    column_names = df.columns

    for old_col_name in column_names:
        # Convertir el nombre de la columna de CamelCase a snake_case
        new_col_name = "".join(["_" + char if char.isupper() and not old_col_name[i - 1].isupper() else char for i, char in enumerate(old_col_name)]).lstrip("_")
    
        # Cambiar el nombre de la columna usando withColumnRenamed
        df = df.withColumnRenamed(old_col_name, new_col_name)

    # Definir la ruta de salida para cada tabla individualmente
    output_path = '/mnt/gold/SalesLT/' +name +'/'
    
    # Guardar cada tabla en la ruta correspondiente
    df.write.format('delta').mode("overwrite").save(output_path)


# COMMAND ----------

display(df)
