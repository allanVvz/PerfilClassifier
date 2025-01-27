from functions import *
import re


def get_marca(tudo, arquivo):
    """
    Função para buscar a marca do veículo em um arquivo de texto ou pelo nome do arquivo.
    Procura por marcas conhecidas como BYD, Ford, GM, Honda, etc.

    Args:
        tudo (str): Conteúdo completo do arquivo de texto.
        arquivo (str): Nome do arquivo.

    Returns:
        str: Marca do veículo encontrada ou 'Desconhecida'.
    """
    marcas_possiveis = ["BYD", "Ford", "GM", "Honda", "Maquinas", "Mb", "Renault", "Toyota", 
                        "Fiat", "Dodge", "VW", "J1939", "SCANIA", "Pegeout", "Nissan", "Hyunda",
                        "Mitsubishi", "Citroen", "Chery", "Ferrari", "JAC", "Jeep", "Kalmar", "TERBERG", "VOLVO"]

    # Verificar no conteúdo do arquivo
    linhas = tudo.splitlines()  # Divide o conteúdo por linhas
    for linha in linhas:
        for marca in marcas_possiveis:
            if marca.lower() in linha.lower():
                return marca

    # Verificar no nome do arquivo
    for marca in marcas_possiveis:
        if marca.lower() in arquivo.lower():
            return marca

    return "N/A"


def classificar_dispositivo(resultado_processado):
    """
    Classifica o tipo de dispositivo com base nos campos de busca encontrados.

    Args:
        resultado_processado (dict): Dicionário retornado pela função processar_arquivo.

    Returns:
        str: Tipo de dispositivo classificado (ex: 'S1', 'S3', 'VL10', etc.) ou 'Desconhecido'.
    """
    if resultado_processado['buscaS8']:
        return 'S8'
    elif resultado_processado['buscaS4']:
        return 'S4'
    elif resultado_processado['buscaVL10']:
        return 'S3'
    elif resultado_processado['buscaS1']:
        return 'S1'
    elif resultado_processado['buscaS3']:
        return 'S3+'
    else:
        return 'N/A'



def get_odometro(resultado):
    """
    Determina o tipo de equipamento (S1, S3, etc.) utilizando o conteúdo e o nome do arquivo,
    e chama a função correspondente para extrair o odômetro.

    Args:
        tudo (str): Conteúdo completo do arquivo de texto.
        comandos (list): Lista de comandos extraídos do arquivo.
        arquivo (str): Nome do arquivo.

    Returns:
        str: Valor do odômetro extraído ou 'Desconhecido'.
    """
    tipo_equipamento = classificar_dispositivo(resultado)

    if tipo_equipamento == "S1":
        return odometro_s1(resultado["comandos"])
    elif tipo_equipamento == "S3":
        return odometro_s3(resultado["comandos"])
    elif tipo_equipamento == "S3+":
        return odometro_s3(resultado["comandos"])
    elif tipo_equipamento == "S8":
        return odometro_s8(resultado["comandos"])
    elif tipo_equipamento == "S4":
        return odometro_s3(resultado["comandos"])
    elif tipo_equipamento == "S4+":
        return odometro_s3(resultado["comandos"])
    else:
        return "N/A"
    

def get_limpador(resultado):
    """
    Extrai informações sobre o limpador e retorna o resultado.

    Args:
        resultado (dict): Objeto contendo as informações processadas do arquivo, incluindo comandos.

    Returns:
        str: Tipo do limpador extraído ('CAN', 'SENSOR', ou None).
    """
    try:
        comandos = resultado.get("comandos", [])
        return extrair_limpador(comandos)  # Certifique-se de usar a função corretamente
    except Exception as e:
        logging.error(f"Erro ao extrair limpador: {e}")
        return None


def get_freio(resultado):
    """
    Extrai informações sobre o freio e retorna o resultado.

    Args:
        resultado (dict): Objeto contendo as informações processadas do arquivo, incluindo comandos.

    Returns:
        str: Tipo do freio extraído ('CAN', 'SENSOR', ou None).
    """
    try:
        tipo_equipamento = classificar_dispositivo(resultado)
        if tipo_equipamento == "S1":
            return freio_s3(resultado["comandos"])
        if tipo_equipamento == "S3":
            return freio_s3(resultado["comandos"])
        if tipo_equipamento == "S3+":
            return freio_s3(resultado["comandos"])
        elif tipo_equipamento == "S4":
            return freio_s3(resultado["comandos"])
        elif tipo_equipamento == "S4+":
            return freio_s3(resultado["comandos"])
        elif tipo_equipamento == "S8":
            return freio_s8(resultado["comandos"])

        return "N/A"
    except Exception as e:
        logging.error(f"Erro ao extrair freio: {e}")
        return None

def get_farol(resultado):
    """
    Extrai informações sobre o farol e retorna o resultado.

    Args:
        resultado (dict): Objeto contendo as informações processadas do arquivo, incluindo comandos.

    Returns:
        str: Tipo do farol extraído ('CAN', 'SENSOR', ou None).
    """
    try:
        tipo_equipamento = classificar_dispositivo(resultado)
        if tipo_equipamento == "S3":
            return farol_s3(resultado["comandos"])
        if tipo_equipamento == "S3+":
            return farol_s3(resultado["comandos"])
        if tipo_equipamento == "S4":
            return farol_s3(resultado["comandos"])
        if tipo_equipamento == "S4+":
            return farol_s3(resultado["comandos"])
        elif tipo_equipamento == "S8":
            return farol_s8(resultado["comandos"])
        return "N/A"
    except Exception as e:
        logging.error(f"Erro ao extrair farol: {e}")
        return None

def get_velocidade(resultado):
    """
    Extrai informações sobre a velocidade e retorna o resultado.

    Args:
        resultado (dict): Objeto contendo as informações processadas do arquivo, incluindo comandos.

    Returns:
        str: Tipo da velocidade extraída ('CAN', 'SENSOR', ou None).
    """
    try:

        tipo_equipamento = classificar_dispositivo(resultado)

        if tipo_equipamento == "S3":
            return velocidade_s3(resultado["comandos"])
        if tipo_equipamento == "S3+":
            return velocidade_s3(resultado["comandos"])
        if tipo_equipamento == "S4":
            return velocidade_s3(resultado["comandos"])        
        if tipo_equipamento == "S4+":
            return velocidade_s3(resultado["comandos"])
        elif tipo_equipamento == "S8":
            return velocidade_s8(resultado["comandos"])
        elif tipo_equipamento == "S1":
            return velocidade_s1(resultado["comandos"])
        return "N/A"
    except Exception as e:
        logging.error(f"Erro ao extrair velocidade: {e}")
        return None


def get_rpm(resultado):
    """
    Extrai informações sobre o RPM e retorna o resultado.

    Args:
        resultado (dict): Objeto contendo as informações processadas do arquivo, incluindo comandos.

    Returns:
        str: Tipo do RPM extraído ('CAN', 'CALCULADO', ou None).
    """
    try:
        tipo_equipamento = classificar_dispositivo(resultado)

        # Chamar a função correspondente ao tipo do equipamento
        if tipo_equipamento == "S1":
            return rpm_s1(resultado["comandos"])
        elif tipo_equipamento == "S3":
            return rpm_s3(resultado["comandos"])
        elif tipo_equipamento == "S3+":
            return rpm_s3(resultado["comandos"])
        elif tipo_equipamento == "S4":
            return rpm_s3(resultado["comandos"])
        elif tipo_equipamento == "S4+":
            return rpm_s3(resultado["comandos"])        
        elif tipo_equipamento == "S8":
            return rpm_s8(resultado["comandos"])
        return "N/A"
    except Exception as e:
        logging.error(f"Erro ao extrair RPM: {e}")
        return None

def get_nomes(resultado):
    """
    Obtém o nome baseado no tipo de dispositivo identificado.

    Args:
        resultado (dict): Dados processados contendo os comandos.

    Returns:
        str: Nome extraído ou None se não encontrado.
    """
    try: 
        tipo_equipamento = classificar_dispositivo(resultado)
        logging.info(f"Tipo de equipamento: {tipo_equipamento}")

        if tipo_equipamento == "S1":
            return extrair_nome_s1(resultado["comandos"])
        else:
            return extrair_nome(resultado["comandos"])

    except Exception as e:
        logging.error(f"Erro ao extrair nome: {e}")
        return None
