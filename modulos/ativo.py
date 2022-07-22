class Ativo:
    '''Classe que cria um objeto do tipo Ativo'''
    categoria = ['Ações', 'FIIs', 'Renda Fixa', 'Tesouro Direto',
                'Reserva de Emergência']
    
    def __init__(self, nome: str, codigo: str):
        self.nome = nome
        self.codigo = codigo
        self.quantidade = 0
        self.valor_u = 0
        self.valor_t = 0

    def __str__(self):
        resultado = f'Nome: {self.nome}\nCódigo: {self.codigo}\nCategoria: {self.categoria}'
        return resultado
