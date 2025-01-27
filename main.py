import pandas as pd
import functions  # Supondo que o pacote functions contém todas as funções fornecidas
import os
import controller

def main():
    # Diretório com os arquivos que serão processados
    diretorio = "./scripts"

    # Lista para armazenar os dados extraídos
    dados_processados = []

    # Iterar sobre os subdiretórios e arquivos no diretório principal
    for root, dirs, files in os.walk(diretorio):
        # Verificar se há uma pasta chamada "CAN-Sensor"
        if "CAN-Sensor" in dirs:
            caminho_can_sensor = os.path.join(root, "CAN-Sensor")
            
            # Iterar pelos arquivos dentro da pasta "CAN-Sensor"
            for arquivo in os.listdir(caminho_can_sensor):
                if arquivo.endswith(".txt") or arquivo.endswith(".log"):
                    caminho_arquivo = os.path.join(caminho_can_sensor, arquivo)

                    # Processar o arquivo usando a função fornecida
                    resultado = functions.processar_arquivo(caminho_arquivo)

                    # Organizar os dados em um dicionário para adicionar à lista
                    dados_processados.append({
                        "Marca": controller.get_marca(resultado["tudo"], arquivo),                        
                        "Device": controller.classificar_dispositivo(resultado),
                        "Arquivo": controller.get_nomes(resultado),
                        "Versao": functions.extrair_versao(resultado["tudo"]),
                        "Velocidade": controller.get_velocidade(resultado),
                        "RPM": controller.get_rpm(resultado),  # Adicionando o RPM
                        "Odômetro": controller.get_odometro(resultado),
                        "Limpador": controller.get_limpador(resultado),
                        "Freio": controller.get_freio(resultado),
                        "Farol": controller.get_farol(resultado),
                    })

    # Converter os dados em um DataFrame do pandas
    df = pd.DataFrame(dados_processados)

    # Salvar os dados em um arquivo Excel
    caminho_planilha = "dados_processados.xlsx"
    df.to_excel(caminho_planilha, index=False)

    print(f"Dados processados e salvos em: {caminho_planilha}")

if __name__ == "__main__":
    main()
