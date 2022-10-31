import mysql.connector
from mysql.connector import Error
import PySimpleGUI as sg

try:
    cnx = mysql.connector.connect(user='root',
                                database='pysimpleguitest',
                                charset='utf8mb4')

    criar_tabela_SQL = """CREATE TABLE tbl_classes (
                          ClassId int(3) NOT NULL AUTO_INCREMENT,
                          ClassName varchar(40) NOT NULL,
                          PRIMARY KEY (ClassId))"""

    cursor = cnx.cursor()
    cursor.execute(criar_tabela_SQL)
    print('Tabela de Classes foi criada com sucesso!')
except mysql.connector.Error as erro:
    print(f'Falha ao criar tabela no MySql o erro foi:> {erro}')
finally:
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print('Conexão ao MySQL finalizada.')

###############################################################

def janela1(theme='Dark'):
    sg.theme(theme)

    tela_1 = [[sg.T('Classe:'), sg.Input(k='-CLASSNAME-')],
              [sg.Button('Enviar')]]

    return sg.Window('Classes', layout=tela_1, finalize=True)

janela1 = janela1('Dark')

while True:
    window, event, values = sg.read_all_windows()

    # Fechando a interface
    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    if event == 'Enviar':
        classId = ''
        className = values['-CLASSNAME-']
        print(type(className))

        try:
            cnx = mysql.connector.connect(user='root',
                                          database='pysimpleguitest')

            declaracao = "INSERT INTO tbl_classes (ClassName) VALUES (%s);"

            cursor = cnx.cursor()
            cursor.execute(declaracao,(className,))
            cnx.commit()
            print(cursor.rowcount, "registros inseridos na tabela!")
            cursor.close()
        except Error as erro:
            print(f'Falha ao inserir danos no MySQL, o erro foi:> {erro}')
        finally:
            if cnx.is_connected():
                cnx.close()
                print('Conexão ao MySQL finalizada com sucesso!')
                break
