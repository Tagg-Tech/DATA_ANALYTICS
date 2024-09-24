import boto3
import os

s3 = boto3.client('s3')

bucket_name = 'seu-bucket-s3'
pasta_local = 'ec2/csv'

for arquivo in os.listdir(pasta_local):
    caminho_arquivo = os.path.join(pasta_local, arquivo)
    
    try:
        s3.upload_file(caminho_arquivo, bucket_name, arquivo)
        print(f"Arquivo {arquivo} enviado para o bucket {bucket_name} com sucesso!")
        
        os.remove(caminho_arquivo)
        print(f"Arquivo {arquivo} apagado da pasta local.")
    
    except Exception as e:
        print(f"Erro ao enviar ou apagar o arquivo {arquivo}: {e}")
