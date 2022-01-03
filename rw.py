import csv
import json
from datetime import date, datetime

final_data = []


def count_Offences(array, offence : str, value : int):
    """Conta a quantidade de ocorrências para uma mesma infração.
        
        Procura dentro do array para encontrar a infração específica.

        Converte o valor armazenado para inteiro.

        Soma o valor armazenado com o parâmetro value.

        Armazena o total de ocorrências.

        Parâmetros
        ----------
        array : list
            Dados que estão armazenados na lista

        offence : str
            O número do beneficiário que irá receber a transferência

        value : int
            A quantidade a ser transferida de conta.
    """
    for item in array: 
        if item['crime'] == offence:
            x = int(item['count']) 
            total_Offences = x + value 
            item['count'] = total_Offences 

def find_Regions(array):
    """Determina todas as regiões existentes dentro da base de dados.
        
        Procura dentro do array para encontrar as regiões.

        Caso uma região não tenha esteja na list de regiões ela será adicionada.

        Para cada região é chamada o metódo filter_offences() para verificar se 
        dentro da localidade ocorreram mais de duas infrações.

        Se o retorno for True a região é adiciona a uma outra list que por fim é
        retornada ao local de chamada do metódo find_Regions().

        Parâmetros
        ----------
        array : list
            Dados que estão armazenados na lista.
    """
    regions = []
    filtered_regions = []

    for x in range(1,len(array)):
        if array[x]['Region'] not in regions:
            regions.append(array[x]['Region'])

    for region in regions:
        resp = filter_offences(array,region)
        if resp == True:
            filtered_regions.append(region)

    return filtered_regions

def filter_offences(array,region):
    """Determina se dentro da região houve mais de dois tipos de infração.
        
        Para cada infração encontrada na região armazena-se em uma list.

        Caso haja os valores na list não sejam iguais é definido True para a
        variavél requisito.

        Por fim requisito é retornado ao local de chamada do metódo find_offences().

        Parâmetros
        ----------
        array : list
            Base de dados que estão armazenados na lista.
        region : str
            Região específica.
    """
    all_offences = []
    requisito = False
    
    for x in range(1,len(array)):
        if array[x]['Region'] == region:    
           all_offences.append(array[x]['Offence'])
           if len(set(all_offences)) != 1:
               requisito = True
               break
        
    return requisito

def group_by_crimes(dictionarys, region):
    """Agrupa das infrações por região.
        
        Para cada infração encontrada na região armazena-se em uma list.

        Só são consideradas as infrações que ocorreram mais de 10 vezes.
        
        Caso haja a mesma infração tenha ocorrido novamente será contabilizada
        a quantidade de ocorrências por meio da count_offences().

        Por fim é retornado a list de crimes para o chamado de group_by_crimes().

        Parâmetros
        ----------
        dictionarys : list
            Base de dados que estão armazenados na lista.
        region : str
            Região específica.
    """
    crimes = []
    all_crimes = [] 
    new_dic = {} 

    for x in range(1,len(dictionarys)):
        if dictionarys[x]['Region'] == region:    

            if dictionarys[x]['Offence'] not in all_crimes: 
                all_crimes.append(dictionarys[x]['Offence'])

                if int(dictionarys[x]['Rolling year total number of offences'])>= 10: 
                    new_dic = {'crime': dictionarys[x]["Offence"], 'count' : dictionarys[x]["Rolling year total number of offences"]}
                    crimes.append(new_dic)

            elif dictionarys[x]['Offence'] in all_crimes: 
                count_Offences(crimes,dictionarys[x]['Offence'],int(dictionarys[x]["Rolling year total number of offences"])) 
    return crimes

def group_by_regions(dictionarys,regions):
    """Agrupamento das infrações para todas regiões.
        
        Para cada região chama-se group_by_crimes().

        Ao receber o retorno do group_by_crimes() cria-se um dicionário 
        contendo a data de processamento, região e os crimes cometidos nela.

        Acrescenta-se esse dicionário a uma list que por fim é retornada ao 
        lugar que chamou a group_by_regions().

        Parâmetros
        ----------
        dictionarys : list
            Base de dados que estão armazenados na lista.
        regions : list
            Lista contendo todas as regiões que atendem as requisitos.
    """
    process = []
    crimes = []
    new_dic = {} 

    today = datetime.now()
    process_date = today.strftime("%d/%m/%Y %H:%M")

    for region in regions:
        crimes = group_by_crimes(dictionarys,region)
        new_dic = {'process_time':process_date,'region': region, 'crimes': crimes}
        process.append(new_dic)

    return process

with open("reccrimepfa-210901-151708.csv","r") as file:
    reader = csv.reader(file,skipinitialspace=True)

    i = 0
    dic = {}

    for row in reader:
        if i == 0:
            header=row #pegando as colunas ['12 months ending', 'PFA', 'Region', 'Offence', 'Rolling year total number of offences']
        elif i>1:
            dic[i-1] = dict(zip((header),row)) #transformando tudo em dicionário
        i+=1

    regions = find_Regions(dic)

    final_data = group_by_regions(dic, regions)


with open("reccrimepfa-210901-151708.csv","w") as file:
    """Para cada indíce da list final_data será feito uma quebra de linha"""
    for i in range(len(final_data)):
        file.write('\n')
        json.dump(final_data[i],file)