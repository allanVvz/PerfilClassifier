import re
from datetime import date
import json
import base64
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
###### FUNÇÕES PARA PERFIL #########

def processar_arquivo(path):
    with open(path, encoding='utf-8') as f:
        tudo = f.read()
        cc_tag = None
        if "Cliente" in path:
            try:
                cc_tag = Get_cc_tag(tudo)
            except Exception as e:
                logging.error(f'Erro ao processar CC_ID tag do {path}: {e}')
                # cc_tag = None

    tudo = re.sub('//.*', '', tudo)
    comandos = re.findall('>.*<|#.*', tudo)
    lista_comandos = []
    for i in range(len(comandos)):
        if i != (len(comandos) - 1):
            lista_comandos.append(comandos[i] + ';')
        if i == (len(comandos) - 1):
            lista_comandos.append(comandos[i])


    buscaVL10 = re.search('Virloc10', path)
    if buscaVL10 is None:
        buscaVL10 = re.search('VL10', path)
        if buscaVL10 is None:
            buscaVL10 = re.search('S3', path)

    
    buscaS3 = re.search('Virloc12', path)
    if buscaS3 is None:
        buscaS3 = re.search('VL12', path)
        if buscaS3 is None:
            buscaS3 = re.search('S3+', path)
            if buscaS3 is None:
                buscaS3 = re.search('>TCFG13,9999<', tudo)
                

    
    buscaS1 = re.search('Virloc6', path)
    if buscaS1 is None:
        buscaS1 = re.search('VL6', path)
        if buscaS1 is None:
            buscaS1 = re.search('>SIS8.*<', tudo)
                

    
    buscaS4 = re.search('Vircom5', path)
    if buscaS4 is None:
        buscaS4 = re.search('VC5', path)
        if buscaS4 is None:
            buscaS4 = re.search('S4', path)
            # if buscaS4 is None:
                # buscaS4 = re.search('>SSB.*<', tudo)

    buscaS8 = re.search('Virloc8', path)
    if buscaS8 is None:
        buscaS8 = re.search('VL8', path)
        if buscaS8 is None:
            buscaS8 = re.search('S8', path)
            if buscaS8 is None:
                buscaS8 = re.search('VL8', tudo)
                

    path = str(path).split('/')[-1].split('.')[0]
    idarquivo = path.replace('_', ' ')

    list_replace = [' VL12',' VL10',' VC5',' VL6',' VL8']

    for i in list_replace:
        idarquivo = idarquivo.replace(i, '')
    

    return {
        'cc_tag': cc_tag,
        'tudo': tudo,
        'lista_comandos': lista_comandos,
        'buscaS3': buscaS3,
        'buscaVL10': buscaVL10,
        'buscaS1': buscaS1,
        'buscaS4': buscaS4,
        'buscaS8': buscaS8,
        'path': path,
        'idarquivo': idarquivo,
        'comandos': comandos
    }

def message(path):
    f=open(f'{path}.json',encoding='utf_8')
    try:
        json_data=f.read()
        json_dict = json.loads(json_data)
        comandos=json_dict['comandos']
        return comandos
    except:
        logging.error(f'Erro ao ler o arquivo {path}.json')
        logging.info('json data:',json_data)
    

def Get_cc_tag(tudo):
    try:
        cc_tag = re.search('[cc.id].*', tudo)
        if cc_tag is not None:
            cc_tag = re.search('\d\d*',cc_tag.group()).group()
        return cc_tag
    except Exception as e:
        logging.error(f'Erro ao extrair CC_ID tag: {e}')

def extrair_lim_vel(tudo):
    try:
        lim_vel = re.search('>SCT11.*<', tudo)
        if lim_vel is not None:
            lim_vel = lim_vel.group()[7:-1]
            if len(lim_vel) == 5:
                lim_vel = lim_vel[0:2]
            else:
                lim_vel = lim_vel[0:3]
        return lim_vel
    except Exception as e:
        logging.error(f'Erro ao extrair limite de velocidade: {e}')

def extrair_vel_evento(tudo):
    try:
        vel_evento = re.search('>SCT12.*<', tudo)
        if vel_evento is not None:
            vel_evento = vel_evento.group()[7:-1]
            if len(vel_evento) == 5:
                vel_evento = vel_evento[0:2]
            elif len(vel_evento) == 6:
                vel_evento = vel_evento[0:3]
        return vel_evento
    except Exception as e:
        logging.error(f'Erro ao extrair velocidade evento: {e}')

def extrair_tempo_infra(tudo):
    try:
        tempo_infra = re.search('>SCT06.*<', tudo)
        if tempo_infra is not None:
            tempo_infra = tempo_infra.group()[7:-1]
        return tempo_infra
    except Exception as e:
        logging.error(f'Erro ao extrair tempo infra: {e}')

def verificar_mifare(tudo):
    try:
        mifare = re.search('>SSH111<', tudo)
        if mifare is not None:
            return 'Habilitado'
        else:
            return 'Desabilitado'
    except Exception as e:
        logging.error(f'Erro ao verificar mifare: {e}')


# def extrair_versao(tudo):
#     versao = re.search('>STP01.*<', tudo)
#     if versao is not None:
#         versao1 = re.search('-', versao.group())
#         if versao1 is None:
#             versao1 = re.search('>STP01.*<', tudo).group()
#             versao1 = re.search('\d\d\d\d*', versao1).group()
#             versao = versao1
#         else:
#             versao = None
#     if versao is None:
#         versao = re.search('>STP03.*<', tudo)
#         if versao is not None:
#             versao2 = re.search('-', versao.group())
#             if versao2 is None:
#                 versao2 = re.search('\d\d\d\d*', versao.group()).group()
#                 versao = versao2
#     if versao is None:
#         versao = str(date.today())
#         versao = versao.replace('-', '')[-6::]
#     return versao

def extrair_versao(tudo):
    try:
        versao = re.search('>STP01.*<', tudo)
        if versao is not None:
            versao1 = re.search('-', versao.group())
            if versao1 is None:
                versao1 = re.search('>STP01.*<', tudo).group()
                versao1 = re.search('\d\d\d\d*', versao1).group()
                return versao1
        versao = re.search('>STP03.*<', tudo)
        if versao is not None:
            versao2 = re.search('-', versao.group())
            if versao2 is None:
                versao2 = re.search('\d\d\d\d*', versao.group()).group()
                return versao2
        versao = re.search('>STP02.*<', tudo)
        if versao is not None:
            versao1 = re.search('-+', versao.group())
            if versao1 is None:
                versao1 = re.search('>STP02.*<', tudo).group()
                versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
                return versao1
        versao = re.search('>STP00.*<', tudo)
        if versao is not None:
            versao1 = re.search('-+', versao.group())
            if versao1 is None:
                versao1 = re.search('>STP00.*<', tudo).group()
                versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
                return versao1
        return str(date.today()).replace('-', '')[-6:]
    except Exception as e:
        logging.error(f'Erro ao extrair versão: {e}')


def verificar_tablet(tudo):
    try:
        if re.search('>SED169U<',tudo):
            tablet = None
            return tablet
        tablet = re.search('>SED169.*<', tudo)
        if tablet is not None:
            tablet = re.search('>SED169.*<', tudo).group()
            tabletN77 = re.search('TRM', tablet)
            if tabletN77 is not None:
                tablet = 'N776/N77'
            tabletSAM = re.search('VCM_SL', tablet)
            if tabletSAM is not None:
                tablet = 'SAMSUNG'
            SEMtablet = re.search('SGN NN', tablet)
            if SEMtablet is not None:
                tablet = None
        return tablet
    except Exception as e:
        logging.error(f'Erro ao verificar tablet: {e}')

def lim_vel_S1(tudo):
    try:
        lim_vel = re.search('>VS08,100.*<', tudo)
        if lim_vel is not None:
            lim_vel = re.search('>VS08,100.*<', tudo).group()[10:13]
            if lim_vel[0] == '0':
                lim_vel = re.sub(r'0', '', lim_vel, count=1)
        return lim_vel
    except Exception as e:
        logging.error(f'Erro ao extrair limite de velocidade S1: {e}')

def tempo_infra_S1(tudo):
    try:
        tempo_infra = re.findall('>SCT06.*<', tudo)
        if tempo_infra and tempo_infra != '0':
            tempo_infra = re.findall('>SCT06.*<', tudo)[0]
            tempo_infra = tempo_infra[7:-1]
            return tempo_infra
        return None
    except Exception as e:
        logging.error(f'tempo_infra_S1 : {e}')



# def versao_S1(tudo):
#     versao = re.search('>SIS82.*<', tudo)
#     if versao is not None:
#         versao1 = re.search('-', versao.group())
#         if versao1 is not None:
#             versao1 = re.search('-', versao1.group())
#         else:
#             versao1 = re.search('>SIS82.*<', tudo).group()
#             versao1 = re.search('\d\d\d\d*', versao1).group()
#         versao = versao1
#     else:
#         versao = re.search('>SIS84.*<', tudo)
#         if versao is not None:
#             versao2 = re.search('>SIS84.*<', tudo).group()
#             if versao2 != '-':
#                 versao2 = re.search('\d\d\d\d*', versao2).group()
#                 versao = versao2
#     return versao

def extrair_versao_s1(tudo):
    try:
        versao = re.search('>SIS82.*<', tudo)
        if versao is not None:
            versao1 = re.search('-', versao.group())
            if versao1 is not None:
                versao1 = re.search('-', versao1.group())
            else:
                versao1 = re.search('>SIS82.*<', tudo).group()
                versao1 = re.search('\d\d\d\d*', versao1).group()
            return versao1
        else:
            versao = re.search('>SIS84.*<', tudo)
            if versao is not None:
                versao2 = re.search('>SIS84.*<', tudo).group()
                if versao2 != '-':
                    versao2 = re.search('\d\d\d\d*', versao2).group()
                    return versao2
        versao = re.search('>SIS83.*<', tudo)
        if versao is not None:
            versao1 = re.search('-+', versao.group())
            if versao1 is None:
                versao1 = re.search('>SIS83.*<', tudo).group()
                versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
                return versao1
        return str(date.today()).replace('-', '')[-6:]
    except Exception as e:
        logging.error(f'Erro ao extrair versão S1: {e}')

###############################################
############# FUNÇÔES CAN #######################

def versao_can(tudo):
    try:
        versao = re.search('>STP02.*<', tudo)
        if versao is not None:
            versao1 = re.search('-+', versao.group())
            if versao1 is None:
                versao1 = re.search('>STP02.*<', tudo).group()
                versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
                versao = versao1
        if versao is None:
            versao = str(date.today())
            versao = versao.replace('-', '')[-6:]
        return versao
    except Exception as e:
        logging.error(f'Erro ao extrair versão CAN: {e}')

def velocidade_s3(comandos):
    try:
        for i in range(len(comandos)):
            velocidade = re.search('>S19.*<', comandos[i])
            if velocidade is not None:
                velocidade = velocidade.group().split(',')[2]
                velocidade = re.search('48', velocidade)
                if velocidade is not None:
                    return 'CAN'
        return 'SENSOR'
    except Exception as e:
        logging.error(f'Erro ao extrair velocidade S3: {e}')

def rpm_s3(comandos):
    try:
        for i in range(len(comandos)):
            rpm = re.search('>S19.*<', comandos[i])
            if rpm is not None:
                rpm = rpm.group().split(',')[2]
                rpm = re.search('26', rpm)
                if rpm is not None:
                    return 'CAN'
        return 'SENSOR'
    except Exception as e:
        logging.error(f'Erro ao extrair RPM S3: {e}')

def extrair_limpador(comandos):
    try:
        for i in range(len(comandos)):
            limpador = re.search('>SUT02,QCT80.*<', comandos[i])
            if limpador is not None:
                return 'CAN'
            
            limpador = re.search('>SUT02,QIN.*<', comandos[i])
            if limpador is not None:
                return 'SENSOR'
        
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair limpador: {e}')

def odometro_s3(comandos):
    try:
        for i in range(len(comandos)):
            odometro = re.search('>S19.*<', comandos[i])
            if odometro is not None:
                odometro = odometro.group().split(',')[2]
                odometro = re.search('49', odometro)
                if odometro is not None:
                    return 'CAN'
            
            odometro = re.search('>SUT50,QCT03,07,15,0,1.*<', comandos[i])
            if odometro is not None:
                return 'SENSOR'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair odometro: {e}')


def horimetro_s3(comandos):
    try:
        for i in range(len(comandos)):
            horimetro = re.search('>S19.*<', comandos[i])
            if horimetro is not None:
                horimetro = horimetro.group().split(',')[2]
                horimetro1 = re.search('29', horimetro)
                horimetro2 = re.search('28', horimetro)
                if horimetro1 is not None or horimetro2 is not None:
                    return 'CAN'            
            horimetro = re.search('>SED119.*<', comandos[i])
            if horimetro is not None:
                return 'CALCULADO'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair horimetro S3: {e}')

def freio_s3(comandos):
    try:
        for i in range(len(comandos)):
            freio = re.search('>S19.*<', comandos[i])
            if freio is not None:
                freio = freio.group().split(',')[2]
                freio = re.search('81', freio)
                if freio is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair freio S3: {e}')

def farol_s3(comandos):
    try:
        for comando in comandos:
            farol = re.search('>S19.*<', comando)
            if farol is not None:
                farol = farol.group().split(',')[2]
                farol = re.search('82', farol)
                if farol is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair farol S3: {e}')

def cinto_s3(comandos):
    try:
        for comando in comandos:
            cinto = re.search('>S19.*<', comando)
            if cinto is not None:
                cinto = cinto.group().split(',')[2]
                cinto = re.search('83', cinto)
                if cinto is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair cinto S3: {e}')

def freio_mao_s3(comandos):
    try:
        for comando in comandos:
            freio_mao = re.search('>S19.*<', comando)
            if freio_mao is not None:
                freio_mao = freio_mao.group().split(',')[2]
                freio_mao = re.search('84', freio_mao)
                if freio_mao is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair freio de mao S3: {e}')

def litrometro(comandos):
    try:
        for comando in comandos:
            if re.search('>SED22.*',comando) is not None:
                return 'CAN'
            if re.search('>SED36.*',comando) is not None:
                return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair litrometro: {e}')


# def versao_can_s1(tudo):
#     versao = re.search('>SIS83.*<', tudo)
#     if versao is not None:
#         versao1 = re.search('-+', versao.group())
#         if versao1 is None:
#             versao1 = re.search('>SIS83.*<', tudo).group()
#             versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
#             return versao1
    
#     return str(date.today()).replace('-', '')[-6:]

def velocidade_s1(comandos):
    try:
        for comando in comandos:
            velocidade = re.search('(>VS19\d.*<)', comando)
            if velocidade is not None:
                velocidade = (velocidade.group().split(',')[4])
                velocidade1 = re.search('05', velocidade)
                velocidade = re.search('04', velocidade)
                if velocidade is not None or velocidade1 is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair velocidade S1: {e}')

def rpm_s1(comandos):
    try:
        for comando in comandos:
            rpm = re.search('(>VS19\d.*<)', comando)
            if rpm is not None:
                rpm = rpm.group().split(',')[4]
                rpm = re.search('03', rpm)
                if rpm is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair RPM S1: {e}')

def odometro_s1(comandos):
    try:
        for comando in comandos:
            odometro = re.search('(>VS19\d.*<)', comando)
            odometroSUT = re.search('>SUT05,QCT07.*<', comando)
            if odometro is not None:
                odometro = odometro.group().split(',')[4]
                odometro1 = re.search('07', odometro)
                odometro = re.search('01', odometro)
                if odometro is not None:
                    return 'CAN'
                if odometro1 is not None:
                    odometro_event = re.search('>SED06U<', comando)
                    if odometro_event is None:
                        return 'CAN'
            if odometroSUT is not None:
                return 'CALCULADO'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair odometro S1: {e}')

# def velocidade_s8(comandos):
#     for comando in comandos:
#         velocidade = re.search('>VS29\d\d,.*<', comando)
#         if velocidade is not None:
#             velocidade = velocidade.group().split(',')[4]
#             velocidade1 = re.search('64', velocidade)
#             if re.search('64', velocidade) is None:
#                 velocidade2 = re.search('48', velocidade)
#             if velocidade1 is not None or velocidade2 is not None:
#                 return 'CAN'
#         velocidade = re.search('>VS29\d\d,.*<', comando)
#         if velocidade is not None:       
#             velocidade = velocidade.group().split(',')[11]
#             if velocidade is not None:
#                 velocidade1 = re.search('64', velocidade)
#                 if re.search('64', velocidade) is None:
#                     velocidade2 = re.search('48', velocidade)
#                 if velocidade1 is not None or velocidade2 is not None:
#                     return 'CAN'
#     return None
        
def velocidade_s8(comandos):
    try:
        for comando in comandos:
            match = re.search('>VS29\d\d,.*<', comando)
            if match is not None:
                if len(match.group().split(',')) == 11:
                    velocidade = match.group().split(',')[4]
                    if re.search('(64|48)', velocidade):
                        return 'CAN'
                if len(match.group().split(',')) > 11:
                    velocidade = match.group().split(',')[11]
                if velocidade is not None and re.search('(64|48)', velocidade):
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair velocidade S8: {e}')

def rpm_s8(comandos):
    try:
        for comando in comandos:
            match = re.search('>VS29\d\d,.*<', comando)
            if match is not None:
                try:
                    rpm = match.group().split(',')[4]
                    if re.search('27', rpm) is not None:
                        return 'CAN'
                    rpm = match.group().split(',')[11]
                    if re.search('27', rpm) is not None:
                        return 'CAN'
                except IndexError:
                    continue
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair RPM S8: {e}')

def odometro_s8(comandos):
    try:
        for comando in comandos:
            odometro = re.search('>VS29\d\d,.*<', comando)
            if odometro is not None:
                odometro = odometro.group().split(',')[4]
                odometro = re.search('01', odometro)
                if odometro is not None:
                    return 'CAN'
            odometro = re.search('>SUT50,QCT03,07,15,0,1.*<', comando)
            if odometro is not None:
                return 'SENSOR'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair odometro S8: {e}')

def horimetro_s8(comandos):
    try:
        for comando in comandos:
            horimetro = re.search('>VS29\d\d,.*<', comando)
            if horimetro is not None:
                horimetro = horimetro.group().split(',')[4]
                horimetro = re.search('02', horimetro)
                if horimetro is not None:
                    return 'CAN'
            horimetro = re.search('>SED119.*<', comando)
            if horimetro is not None:
                return 'CALCULADO'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair horimetro S8: {e}')

def freio_s8(comandos):
    try:
        for comando in comandos:
            match = re.search('>VS29\d\d,.*<', comando)
            if match is not None:
                try:
                    freio = match.group().split(',')[4]
                    if re.search('81', freio) is not None:
                        return 'CAN'
                    freio = match.group().split(',')[11]
                    if re.search('81', freio) is not None:
                        return 'CAN'
                except IndexError:
                    continue
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair freio S8: {e}')

def farol_s8(comandos):
    try:
        for comando in comandos:
            farol = re.search('>VS29\d\d,.*<', comando)
            if farol is not None:
                farol = farol.group().split(',')[4]
                farol = re.search('82', farol)
                if farol is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair farol S8: {e}')

def cinto_s8(comandos):
    try:
        for comando in comandos:
            cinto = re.search('>VS29\d\d,.*<', comando)
            if cinto is not None:
                cinto = cinto.group().split(',')[4]
                cinto = re.search('83', cinto)
                if cinto is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair cinto S8: {e}')

def freio_mao_s8(comandos):
    try:
        for comando in comandos:
            freio_mao = re.search('>VS29\d\d,.*<', comando)
            if freio_mao is not None:
                freio_mao = freio_mao.group().split(',')[4]
                freio_mao = re.search('84', freio_mao)
                if freio_mao is not None:
                    return 'CAN'
        return None
    except Exception as e:
        logging.error(f'Erro ao extrair freio de mao S8: {e}')
