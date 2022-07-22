from modulos.ativo import Ativo
from modulos.regras_negocio import CadastroAtivos


class GerenciadorAtivos:
    '''Classe responsável por gerenciar todos os ativos'''
    def __init__(self):
        self.investimentos = CadastroAtivos()
        self.loop_infitio = self.loop_infinito()

    def loop_infinito(self):
        '''Método responsável por gerenciar as opções do usuário'''
        while True:
            self.limpar_tela()
            self.menu()
            escolha = self.opcao()
            self.limpar_tela()
            if escolha == 1:
                nome = str(input('Nome do produto: ')).title()
                codigo = str(input('Código do ativo: ')).upper()
                print('')
                print('Agora escolha a categoria do investimento: \n'
                    '[ 0 ] Ações\n'
                    '[ 1 ] FIIs\n'
                    '[ 2 ] Renda Fixa\n'
                    '[ 3 ] Tesouro Direto\n'
                    '[ 4 ] Reserva de Emergência\n'
                    '\n')

                categoria = str(input('Escolha a categoria do investimento: '))

                if nome == '' or codigo == '' or categoria == '':
                    print('Preencha todos os dados.')
                    self.continuar()
                elif categoria not in '01234':
                    print('Categoria inválida. Tente novamente.')
                    self.continuar()
                else:
                    ativo = Ativo(nome, codigo)
                    qtde = str(input('Quantidade a ser comprada: '))
                    valor_u = str(input('Valor por ação: R$ '))

                    if qtde == '' or valor_u == '':
                        print('Revise os dados informados...')
                        self.continuar()
                    else:
                        qtde = int(qtde)
                        valor_u = float(valor_u)
                        categoria = int(categoria)
                        self.investimentos.comprar_ativo(ativo, categoria, qtde, valor_u)
                        self.continuar()

            elif escolha == 2:
                codigo = str(input('Código do ativo: ')).upper()
                qtde = str(input('Quantidade: '))
                valor = str(input('Valor: R$ '))

                if codigo == '' or qtde == '' or valor == '':
                    print('Preencha todos os dados.')
                    self.continuar()
                else:
                    qtde = int(qtde)
                    valor = float(valor)
                    self.investimentos.vender_ativo(codigo, qtde, valor)
                    self.continuar()

            elif escolha == 3:
                codigo = str(input('Código do ativo: ')).upper()
                if codigo == '':
                    print('Digite o nome do ativo.')
                    self.continuar()
                else:
                    if self.investimentos.get_id(codigo) != -1:
                        print('\n')
                        print('Agora escolha a categoria do investimento: \n'
                            '[ 0 ] Ações\n'
                            '[ 1 ] FIIs\n'
                            '[ 2 ] Renda Fixa\n'
                            '[ 3 ] Tesouro Direto\n'
                            '[ 4 ] Reserva de Emergência\n'
                            '\n')
                        categoria = str(input('Categoria: '))
                        if codigo == '' or categoria == '':
                            print('Preencha todos os dados.')
                            self.continuar()
                        else:
                            categoria = int(categoria)
                            self.investimentos.atualizar_dados_ativo(codigo.upper(), categoria)
                            self.continuar()
                    else:
                        print('Ativo não encontrado.')
                        self.continuar()

            elif escolha == 4:
                codigo = str(input('Código do ativo a ser deletado: ')).upper()
                if codigo == '':
                    print('Preencha todos os dados.')
                    self.continuar()
                else:
                    if self.investimentos.get_id(codigo) != -1:
                        escolha = str(input(f'Deseja realmente deletar sua posição em "{codigo}"? [S/N]: ')).upper()
                        if escolha not in 'SN':
                            print('Opção inválida. Tente novamente.')
                            self.continuar()
                        elif escolha == 'S':
                            self.investimentos.deletar_ativo(codigo)
                            self.continuar()
                        elif escolha == 'N':
                            print('Operação cancelada com sucesso.')
                            self.continuar()
                    else:
                        print('Ativo não encontrado.')
                        self.continuar()

            elif escolha == 5:
                print('Categorias cadastradas:\n'
                    '[ 0 ] Ações\n'
                    '[ 1 ] FIIs\n'
                    '[ 2 ] Renda Fixa\n'
                    '[ 3 ] Tesouro Direto\n'
                    '[ 4 ] Reserva de Emergência\n'
                    '\n'
                    )
                categoria = str(input('Opção desejada: '))
                if categoria == '':
                    print('Escolha uma opção de categoria.')
                    self.continuar()
                else:
                    if categoria not in '01234':
                        print('Opção inválida. Tente novamente.')
                        self.continuar()
                    else:
                        categoria = int(categoria)
                        self.limpar_tela()
                        self.investimentos.filtar_por_categoria(categoria)
                        self.continuar()
                
            elif escolha == 6:
                self.investimentos.sair()
                break
        print('Programa encerrado')

    def opcao(self) -> int:
        try:
            opcao = str(input('Escolha a opção desejada: '))
            if opcao == '' or opcao not in '123456':
                print('Opção inválida.')
                self.continuar()
        except ValueError as error:
            pass
        else:
            if opcao in '123456':
                opcao = int(opcao)
            else:
                opcao = 0
            return opcao

    def limpar_tela(self):
        print('\n' * 100)

    def menu(self):
        print('------RESUMO DOS SEUS INVESTIMENTOS------\n')
        tot = self.investimentos.resumo_total()
        ac = self.investimentos.resumo_parcial_por_categoria(0)
        fii = self.investimentos.resumo_parcial_por_categoria(1)
        rf = self.investimentos.resumo_parcial_por_categoria(2)
        td = self.investimentos.resumo_parcial_por_categoria(3)
        re = self.investimentos.resumo_parcial_por_categoria(4)

        print(f'**VALOR TOTAL DO PATRIMÔNIO: R$ {tot:.2f}**\n'
            '\n'
            f'AÇÕES: R$ {ac:.2f}\n'
            f'FIIs: R$ {fii:.2f}\n'
            f'RENDA FIXA: R$ {rf:.2f}\n'
            f'TESOURO DIRETO: R$ {td:.2f}\n'
            f'RESERVA DE EMERGÊNCIA: R$ {re:.2f}\n'
            '------------------------------------------\n'
            )

        print('Escolha a opção desejada:\n'
            '\n'
            '[ 1 ] Investir\n'
            '[ 2 ] Vender\n'
            '[ 3 ] Alterar dados cadastrais de um ativo\n'
            '[ 4 ] Encerrar posição em um investimento\n'
            '[ 5 ] Relatório por categoria de ativo\n'
            '[ 6 ] Encerrar programa\n'
            '\n'
            )

    def continuar(self):
        input('Precione ENTER para continuar...')

GerenciadorAtivos()
