import mysql.connector
from mysql.connector import Error
import PySimpleGUI as sg

loginCheck = False

try:
    cnx = mysql.connector.connect(user='root',
                                database='pysimpleguitest',
                                charset='utf8mb4')

    criar_tabela_SQL = """CREATE TABLE tbl_users (
                          userId int(3) NOT NULL AUTO_INCREMENT,
                          login varchar(20) NOT NULL,
                          senha varchar(20) NOT NULL,
                          email varchar(100) NOT NULL,
                          PRIMARY KEY (userId))"""

    cursor = cnx.cursor()
    cursor.execute(criar_tabela_SQL)
    print('Tabela de Usuarios foi criada com sucesso!')
except mysql.connector.Error as erro:
    print(f'Falha ao criar tabela no MySql o erro foi:> {erro}')
finally:
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print('Conexão ao MySQL finalizada.')

###############################################################

def makeWindow1(theme='Dark'):
    sg.theme(theme)

    tela_1 = [[sg.T('Login:'), sg.Input(k='-LOGIN-')],
              [sg.T('Senha:'), sg.Input(k='-SENHA-', password_char='*')],
              [sg.T('Email:'), sg.Input(k='-EMAIL-')],
              [sg.Button('Criar conta'), sg.Button('Já tenho uma conta')]]

    return sg.Window('Cadastro', layout=tela_1, finalize=True)

def makeWindow2(theme='Dark'):
    sg.theme(theme)

    tela_2 = [[sg.T('Login:'), sg.Input(k='-CLOGIN-')],
              [sg.T('Senha:'), sg.Input(k='-CSENHA-', password_char='*')],
              [sg.Button('Logar'), sg.Button('Voltar')]]

    return sg.Window('Login', layout=tela_2, finalize=True)

def makeWindow3(theme='Dark'):
    sg.theme(theme)

    tela_3 = [[sg.T('Parabens, você conseguiu!')]]

    return sg.Window('Login', layout=tela_3, finalize=True)

janela1, janela2, janela3 = makeWindow1('Dark'), None, None



while True:
    window, event, values = sg.read_all_windows()

    # Fechando a interface
    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    if event == 'Criar conta':
        login = values['-LOGIN-']
        senha = values['-SENHA-']
        email = values['-EMAIL-']
        if login == '' or senha == '' or email == '':
            sg.popup('Falha ao cadastrar, por favor preencha todos os campos! ')
        else:
            sg.popup('Cadastro realizado com sucesso!')

            try:
                cnx = mysql.connector.connect(user='root',
                                              database='pysimpleguitest')

                declaracao = "INSERT INTO tbl_users (login, senha, email) VALUES (%s, %s, %s);"

                cursor = cnx.cursor()
                cursor.execute(declaracao,(login,senha,email,))
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

    if event == 'Já tenho uma conta':
        janela1.hide()
        janela2 = makeWindow2()

    if window == janela2 and event == 'Logar':
        def read_query(cnx, query):
            cursor = cnx.cursor()
            result = None
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
            except Error as err:
                print(f"Error: '{err}'")


        puxarDados = """
        SELECT *
        FROM tbl_users;
        """

        cnx = mysql.connector.connect(user='root',
                                      database='pysimpleguitest',
                                      charset='utf8mb4')
        results = read_query(cnx, puxarDados)

        for result in results:
            if values['-CLOGIN-'] == result[1] and values['-CSENHA-'] == result[2]:
                sg.popup('Login realizado com sucesso!')
                nameUser = values['-CLOGIN-']
                loginCheck = True
            else:
                sg.popup('Dados invalidos!')
                loginCheck = False

    if loginCheck == True:
        janela2.hide()
        janela3 = makeWindow3()
