from .repositorio import Repositorio
from time import sleep


class CadastroAtivos:
    '''Classe que organizar e gerencia as regras de negócio'''
    def __init__(self):
        self.repositorio = Repositorio()

    def comprar_ativo(self, ativo, categoria: int, qtde: int, valor: float):
        '''Função responsável por comprar mais ativos.
        Se o ativo em questão ainda não estiver cadastrado, a função
        criará o ativo no banco de dados.
        Categorias:
        indice 0 = Ações -
        indice 1 = FIIs - 
        indice 2 = Renda Fixa -
        indice 3 = Tesouro Direto -
        indice 4 = Reserva de Emergência'''
        id = self.repositorio.get_id_e_existe(ativo.codigo)
        if id == -1:
            print('Ativo ainda não cadastrado')
            sleep(1)
            print('Cadastrando novo ativo...')
            sleep(1)
            self.repositorio.criar_novo_ativo(ativo, categoria)
            self.repositorio.comprar_ativo(ativo.codigo, qtde, valor)
            sleep(1)
            print(f'Comprado {qtde} unidade(s) do ativo: "{ativo.codigo}"')
        else:
            self.repositorio.comprar_ativo(ativo.codigo, qtde, valor)
            sleep(1)
            print(f'Comprado {qtde} unidade(s) do ativo: "{ativo.codigo}"')

    def vender_ativo(self, codigo, quantidade: int, valor: float):
        '''Função que vende ativos'''
        if self.repositorio.get_id_e_existe(codigo) == -1:
            print('Ativo não encontrado')
        else:
            self.repositorio.vender_ativo(codigo, quantidade, valor)

    def atualizar_dados_ativo(self, codigo, categoria: int):
        '''Função que atualiza os dados do ativo.
        Categorias:
        indice 0 = Ações -
        indice 1 = FIIs - 
        indice 2 = Renda Fixa -
        indice 3 = Tesouro Direto -
        indice 4 = Reserva de Emergência'''
        if self.repositorio.get_id_e_existe(codigo) == -1:
            print('Ativo não encontrado.')
        else:
            self.repositorio.atualizar_dados_ativo(codigo, categoria)

    def deletar_ativo(self, codigo):
        '''Função que deleta ativos'''
        if self.repositorio.get_id_e_existe(codigo) == -1:
            print('Ativo não encontrado.')
        else:
            self.repositorio.deletar_ativo(codigo)
            print('Ativo deletado com sucesso.')

    def filtar_por_categoria(self, categoria):
        '''Apresenta um relatório de todos os ativos presentes 
        na categoria selecionada.
        Categorias:
        indice 0 = Ações -
        indice 1 = FIIs - 
        indice 2 = Renda Fixa -
        indice 3 = Tesouro Direto -
        indice 4 = Reserva de Emergência'''
        self.repositorio.filtrar_por_categoria(categoria)

    def resumo_parcial_por_categoria(self, categoria: int):
        '''Apresenta um relatório com o valor total investivo na
        categoria selecionada.
        Categorias:
        indice 0 = Ações -
        indice 1 = FIIs - 
        indice 2 = Renda Fixa -
        indice 3 = Tesouro Direto -
        indice 4 = Reserva de Emergência'''
        return self.repositorio.resumo_parcial(categoria)

    def resumo_total(self):
        '''Retorna o valor total investido somando todas
        as categorias de ativos.'''
        return self.repositorio.resumo_total()

    def get_id(self, codigo):
        '''Retorna o id do ativo ou -1'''
        id = self.repositorio.get_id_e_existe(codigo)
        return id
    
    def sair(self):
        '''Função responsável por finalizar a conexão com a banco de dados.'''
        self.repositorio.sair()
