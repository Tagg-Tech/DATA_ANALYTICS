import boto3, dotenv , os

s3 = boto3.client('s3')

dotenv.load_dotenv(dotenv.find_dotenv())

baseurl = os.getenv("URL")
url = f'{baseurl}//rest/api/2/issue'
token = os.getenv("TOKEN")
email = os.getenv("LOGIN")
key_id = os.getenv("KEY_ID")
key_acess = os.getenv("KEY_ACESS")
aws_token = os.getenv("AWS_TOKEN")


s3 = boto3.client( 's3',
          aws_access_key=key_id,
          aws_secret_access_key=key_acess,
          aws_session_token=aws_token
)


bucket_name = 'tagtech-raw'
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
