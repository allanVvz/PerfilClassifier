import pandas as pd
import functions  # Supondo que o pacote functions contém todas as funções fornecidas
import os

def main():
    # Diretório com os arquivos que serão processados
    diretorio = "./scripts"

    # Lista para armazenar os dados extraídos
    dados_processados = []

    # Iterar sobre os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".txt") or arquivo.endswith(".log"):
            caminho_arquivo = os.path.join(diretorio, arquivo)

            # Processar o arquivo usando a função fornecida
            resultado = functions.processar_arquivo(caminho_arquivo)

            # Organizar os dados em um dicionário para adicionar à lista
            dados_processados.append({
                "Arquivo": resultado["path"],
                "CC_Tag": resultado["cc_tag"],
                "Versao": functions.extrair_versao(resultado["tudo"]),
                "Velocidade": functions.extrair_vel_evento(resultado["tudo"]),
                "Limite Velocidade": functions.extrair_lim_vel(resultado["tudo"]),
                "Tempo Infra": functions.extrair_tempo_infra(resultado["tudo"]),
                "Comandos": " | ".join(resultado["lista_comandos"]),
            })

    # Converter os dados em um DataFrame do pandas
    df = pd.DataFrame(dados_processados)

    # Salvar os dados em um arquivo Excel
    caminho_planilha = "dados_processados.xlsx"
    df.to_excel(caminho_planilha, index=False)

    print(f"Dados processados e salvos em: {caminho_planilha}")

if __name__ == "__main__":
    main()
