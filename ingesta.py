import mysql.connector
import csv
import boto3
from botocore.exceptions import NoCredentialsError
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Imprimir un mensaje de inicio con formato profesional
print(f"{Fore.GREEN}{Style.BRIGHT}Inicio de proceso de exportación de datos a S3...{Style.RESET_ALL}\n")

# Establecer la conexión a la base de datos
try:
    print(f"{Fore.YELLOW}Conectando a la base de datos MySQL...{Style.RESET_ALL}")
    connection = mysql.connector.connect(
        host="172.31.23.130",    # Reemplaza con la IP pública de tu instancia EC2
        user="root",               # Tu usuario de la base de datos
        password="utec",        # Tu contraseña de la base de datos
        database="bd_api_employees",     # Nombre de la base de datos
        port=8005                        # Puerto donde MySQL está escuchando
    )
    print(f"{Fore.GREEN}{Style.BRIGHT}Conexión exitosa a la base de datos.{Style.RESET_ALL}")
except mysql.connector.Error as err:
    print(f"{Fore.RED}Error al conectar a la base de datos: {err}{Style.RESET_ALL}")
    exit(1)

# Crear un cursor para ejecutar la consulta
cursor = connection.cursor()

# Hacer una consulta SELECT para obtener todos los empleados
print(f"{Fore.YELLOW}Ejecutando consulta para obtener empleados...{Style.RESET_ALL}")
cursor.execute("SELECT * FROM employees")

# Obtener todos los resultados de la consulta
results = cursor.fetchall()

# Definir el nombre del archivo CSV
csv_file = "mysql_data.csv"

# Abrir el archivo CSV en modo escritura
try:
    print(f"{Fore.YELLOW}Generando archivo CSV...{Style.RESET_ALL}")
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Escribir la cabecera (nombres de las columnas)
        writer.writerow(['ID', 'Nombre', 'Edad'])

        # Escribir los datos de los empleados
        for row in results:
            writer.writerow(row)

    print(f"{Fore.GREEN}{Style.BRIGHT}Archivo CSV '{csv_file}' generado exitosamente.{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Error al generar el archivo CSV: {e}{Style.RESET_ALL}")
    exit(1)

# Cerrar el cursor y la conexión
cursor.close()
connection.close()

# Subir el archivo CSV a un bucket de S3
bucket_name = 'cloud-s6-ingesta'  # Nombre de tu bucket en S3
object_name = 'mysql_data.csv'  # Nombre con el que se guardará el archivo en S3

# Crear el cliente de S3
print(f"{Fore.YELLOW}Conectando a AWS S3...{Style.RESET_ALL}")
s3_client = boto3.client('s3')

try:
    # Subir el archivo
    print(f"{Fore.YELLOW}Subiendo el archivo CSV a S3...{Style.RESET_ALL}")
    s3_client.upload_file(csv_file, bucket_name, object_name)
    print(f"{Fore.GREEN}{Style.BRIGHT}Archivo '{csv_file}' subido exitosamente a S3://{bucket_name}/{object_name}{Style.RESET_ALL}")
except FileNotFoundError:
    print(f"{Fore.RED}El archivo '{csv_file}' no fue encontrado.{Style.RESET_ALL}")
except NoCredentialsError:
    print(f"{Fore.RED}No se encontraron las credenciales de AWS. Verifique su configuración.{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Error al subir el archivo a S3: {e}{Style.RESET_ALL}")

print(f"\n{Fore.CYAN}{Style.BRIGHT}Proceso completado.{Style.RESET_ALL}")
