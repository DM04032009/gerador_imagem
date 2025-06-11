import requests
import os
from PIL import Image
from io import BytesIO
import webbrowser
from urllib.parse import quote
from dotenv import load_dotenv # Importa a nova biblioteca

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- Configuração ---

# Pega a API Key do ambiente. Retorna None se não encontrar.
API_KEY = os.getenv("POLLO_API_KEY")

# URL da API do Pollinations.ai
# ATENÇÃO: A URL pode ser diferente para usuários com API Key.
# Verifique a documentação da Pollo.ai para a URL correta do endpoint autenticado.
API_URL = "https://image.pollinations.ai/prompt/"

# Pasta onde as imagens serão salvas
OUTPUT_DIR = "imagens_geradas"

def gerar_e_salvar_imagem(prompt: str, width: int = 1024, height: int = 1024):
    """
    Função para gerar uma imagem usando a API do Pollinations e salvá-la localmente.
    """
    # Verifica se a API Key foi carregada
    if not API_KEY:
        print("❌ ERRO: A variável POLLO_API_KEY não foi encontrada no seu arquivo .env")
        print("Por favor, crie o arquivo .env e adicione sua chave.")
        return

    print(f"Gerando imagem com autenticação para o prompt: '{prompt}'...")

    prompt_formatado = quote(prompt)
    url_completa = f"{API_URL}{prompt_formatado}?width={width}&height={height}"

    # Prepara os cabeçalhos (headers) para enviar a chave de API.
    # O formato "Bearer <token>" é muito comum, mas pode variar.
    # Verifique a documentação da API para o formato exato.
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        # Faz a requisição GET, agora incluindo os cabeçalhos de autenticação
        response = requests.get(url_completa, headers=headers, stream=True)

        if response.status_code == 200:
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)

            nome_arquivo = f"{prompt[:30].replace(' ', '_').replace('.', '')}.png"
            caminho_arquivo = os.path.join(OUTPUT_DIR, nome_arquivo)
            
            image = Image.open(BytesIO(response.content))
            image.save(caminho_arquivo, 'PNG')
            
            print(f"\n✅ Imagem salva com sucesso em: {caminho_arquivo}")
            
            try:
                webbrowser.open(caminho_arquivo)
            except Exception as e:
                print(f"Não foi possível abrir a imagem automaticamente. Erro: {e}")

        else:
            # Em caso de erro 401 ou 403, provavelmente a chave é inválida.
            print(f"\n❌ Erro ao gerar imagem. Status Code: {response.status_code}")
            if response.status_code in [401, 403]:
                print("   Isso pode significar que sua API Key é inválida ou o formato do header está incorreto.")
            print(f"   Resposta da API: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Falha na conexão com a API. Verifique sua internet. Erro: {e}")

if __name__ == "__main__":
    prompt_usuario = input("Digite o que você quer gerar (em inglês de preferência): ")
    
    if prompt_usuario:
        gerar_e_salvar_imagem(prompt_usuario)
    else:
        print("Nenhum prompt foi fornecido. O programa será encerrado.")