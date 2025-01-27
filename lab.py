def classificar_script(tudo, arquivo):
    """
    Função para classificar scripts em categorias como VL10, S3, S1, etc.

    Args:
        tudo (str): Conteúdo completo do arquivo de texto.
        arquivo (str): Nome do arquivo.

    Returns:
        str: Categoria do script encontrada ou 'Desconhecida'.
    """
    categorias = {
        "S3": [r"Virloc10", r"VL10"],
        "S3+": [r"Virloc12", r"VL12", r"S3+", r">TCFG13,9999<"],
        "S1": [r"Virloc6", r"VL6", r">SIS8.*<"],
        "S4": [r"Vircom5", r"VC5", r"S4"],
        "S4+": [r"Vircom7", r"VC7", r"S4"],
        "S8": [r"Virloc8", r"VL8", r"S8"]
    }

    for categoria, padroes in categorias.items():
        for padrao in padroes:
            if re.search(padrao, tudo) or re.search(padrao, arquivo):
                return categoria

    return "Desconhecida"