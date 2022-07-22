from .ativo import Ativo
import sqlite3

class Repositorio:
    '''Classe responsável por organizar o bando de dados SQL.'''
    def __init__(self):
        self.conn = sqlite3.connect('data/bd.db')
        self.cursor = self.conn.cursor()

    def criar_novo_ativo(self, ativo: Ativo, indice_categoria: int):
        '''
        Categorias:
        indice 0 = Ações -
        indice 1 = FIIs - 
        indice 2 = Renda Fixa -
        indice 3 = Tesouro Direto -
        indice 4 = Reserva de Emergência
        '''
        ativo_categoria = Ativo.categoria[indice_categoria]
        func = 'INSERT INTO repositorio (nome, codigo, categoria, quantidade, valor_u, valor_t) VALUES (?, ?, ?, ?, ?, ?)'
        self.cursor.execute(func, (ativo.nome, ativo.codigo, ativo_categoria,ativo.quantidade, ativo.valor_u, ativo.valor_t))
        self.conn.commit()
    
    def atualizar_dados_ativo(self, codigo, nova_categoria: int):
        '''Função para alterar os dados do ativo.
        Informações a serem alteradas: nome, código e categoria.'''
        id = self.get_id_e_existe(codigo)
        if self.vazio() == True:
            print('Nenhum ativo cadastrado')
        elif id == -1:
            print('Ativo não cadastrado.')
            print('Verifique as informações digitadas.')
        else:
            novo_nome = str(input('Nome: ')).title()
            novo_codigo = str(input('Código: ')).upper()
            if novo_nome == '' or novo_codigo == '':
                print('Preencha todos os dados.')
            else:
                categoria_ativo = Ativo.categoria[nova_categoria]
                func = 'UPDATE repositorio SET nome=?, codigo=?, categoria=? WHERE id=?'
                self.cursor.execute(func, (novo_nome, novo_codigo, categoria_ativo, id))
                self.conn.commit()
                print('Dados atualizados com sucesso.')

    def comprar_ativo(self, codigo, quantidade: int, valor_u: float):
        '''Pega o id do ativo pelo seu código e verifica se ele existe.
        Se ele existir, a função altera a quantidade, valor unitário e valor total do ativo'''
        id = self.get_id_e_existe(codigo)
        valor_tot = 0
        if id != -1: 
            func = 'SELECT * FROM repositorio WHERE codigo LIKE ?'
            self.cursor.execute(func, (codigo,))
            for ativo in self.cursor.fetchall():
                quantidade_atual = ativo[4]
                valor_unit_atual = ativo[5]
                valor_tot_atual = ativo[6]

                quantidade += quantidade_atual
                if valor_unit_atual == 0:
                    valor_f = valor_u
                else:
                    valor_f = ((valor_u + valor_unit_atual) / 2)

                valor_tot = quantidade * valor_u
                valor_tot += valor_tot_atual

                func_2 = 'UPDATE repositorio SET quantidade=?, valor_u=?, valor_t=? WHERE id=?'
                self.cursor.execute(func_2, (quantidade, valor_f, valor_tot, id))
                self.conn.commit()
        else:
            print('Ativo não encontrado.')

    def vender_ativo(self, codigo, quantidade: int, valor_u: float):
        '''Pega o id do ativo pelo seu código e verifica se ele existe.
        Se ele existir, a função altera a quantidade, valor unitário e valor total do ativo'''
        id = self.get_id_e_existe(codigo)
        if id != -1: 
            func = 'SELECT * FROM repositorio WHERE codigo LIKE ?'
            self.cursor.execute(func, (codigo,))
            for ativo in self.cursor.fetchall():
                quantidade_atual = ativo[4]
                valor_u_atual = ativo[5]
                valor_tot_atual = ativo[6]

                if quantidade_atual <= 0 or (quantidade_atual - quantidade) < 0 :
                    print('Você não possui quantidade suficiente para esta operação.')
                else:
                    quantidade_atual -= quantidade
                    valor_tot_atual = (valor_u * quantidade_atual)

                    func_2 = 'UPDATE repositorio SET quantidade=?, valor_u=?, valor_t=? WHERE id=?'
                    self.cursor.execute(func_2, (quantidade_atual, valor_u, valor_tot_atual, id))
                    self.conn.commit()

                    print('Venda realizada com sucesso.')
        else:
            print('Ativo não encontrado.')

    def deletar_ativo(self, codigo):
        '''Deleta o ativo pelo seu código.'''
        id = self.get_id_e_existe(codigo)
        if id != -1:
            func = "DELETE FROM repositorio WHERE id=?"
            self.cursor.execute(func, (id,))
            self.conn.commit()
        else:
            print('Ativo não localizado.')

    def get_id_e_existe(self, codigo: Ativo) -> int:
        '''Retorna o id do ativo ou -1'''
        resultado = -1
        func = 'SELECT * FROM repositorio WHERE codigo LIKE ?'
        self.cursor.execute(func, (codigo,))
        for ativo in self.cursor.fetchall():
            if codigo == ativo[2]:
                resultado = ativo[0]
        return resultado

    def filtrar_por_categoria(self, categoria: str):
        '''
        Categorias:
        indice 0 = Ações -
        indice 1 = FIIs - 
        indice 2 = Renda Fixa -
        indice 3 = Tesouro Direto -
        indice 4 = Reserva de Emergência
        '''
        categoria_ativo = Ativo.categoria[categoria]
        if self.vazio() == True:
            print('Nenhum ativo cadastrado.')
        else:
            print(f'---ATIVOS NA CATEGORIA "{categoria_ativo}"---')
            print('')
            tot = 0
            func = 'SELECT * FROM repositorio WHERE categoria=?'
            self.cursor.execute(func, (categoria_ativo,))
            for ativo in self.cursor.fetchall():
                ident, n, cod, cat, q, vu, vt = ativo
                print(''
                f'Id: {ident}\n'
                f'Nome: {n}\n'
                f'Código: {cod}\n'
                f'Categoria: {cat}\n'
                f'Quantidade: {q:.2f}\n'
                f'Valor por ação: R$ {vu:.2f}\n'
                f'Valor total: R$ {vt:.2f}'
                )
                tot += vt
                print('')
            
            print(f'TOTAL INVESTIDO NA CATEGORIA "{categoria_ativo}": R$ {tot:.2f}.')

    def resumo_parcial(self, categoria: int) -> int:
        '''
        Retorna o valor total investido por categoria de ativo.
        Categorias:
        indice 0 = Ações -
        indice 1 = FIIs - 
        indice 2 = Renda Fixa -
        indice 3 = Tesouro Direto -
        indice 4 = Reserva de Emergência
        '''
        categoria_ativo = Ativo.categoria[categoria]
        tot = 0
        func = 'SELECT * FROM repositorio WHERE categoria=?'
        self.cursor.execute(func, (categoria_ativo,))
        for ativo in self.cursor.fetchall():
            tot += ativo[6]
        return tot

    def resumo_total(self) -> int:
        '''Retorna o valor total investido em todas as categorias.'''
        tot = 0
        self.cursor.execute('SELECT * FROM repositorio')
        for ativo in self.cursor.fetchall():
            tot += ativo[6]
        return tot

    def vazio(self) -> bool:
        '''Se o repositório estiver vazio retorna True,
        senão, retorna False.'''
        resultado = True
        self.cursor.execute('SELECT * FROM repositorio')
        contador = 0
        for item in self.cursor.fetchall():
            contador += 1
        if contador != 0:
            resultado = False
        return resultado

    def sair(self):
        '''Finaliza a conexão com o banco de dados.'''
        self.conn.close()
