import xml.etree.ElementTree as ET
import cx_Oracle

if __name__ == '__main__':
    tree = ET.parse('file.xml')
    root = tree.getroot()

    ndfl_list = []

    for item in root.iter('СправДох'):
        contras = item.find('ПолучДох')
        dohod = item.find('СведДох')

        ndfl_dict = {
            'inn': contras.get('ИННФЛ'), 
            'f': contras[0].get('Фамилия'),
            'i': contras[0].get('Имя'),
            'o': contras[0].get('Отчество'),
            'all_money': float(dohod[0].get('СумДохОбщ')),
            'base': float(dohod[0].get('НалБаза')),
            'nalog': float(dohod[0].get('НалИсчисл')),
        }
        ndfl_list.append(ndfl_dict)

    user = input('Input user name:')
    password = input('Input password:')
    server = input('Input server:')

    with cx_Oracle.connect(user=user, password=password,
                                dsn=server) as connection:
        cursor = connection.cursor()
        for row in ndfl_list:
            cursor.execute('insert into vsm_ndfl_file values (:inn, :f, :i, :o, :all_money, :base, :nalog)',row)
                
        connection.commit()                           
