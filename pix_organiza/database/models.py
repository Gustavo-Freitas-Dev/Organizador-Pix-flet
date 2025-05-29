import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.connection import Base, session
from sqlalchemy import Column, String, Integer

class Bancos(Base):
    __tablename__ = 'bancos'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    variacao = Column('variacao', String)
    nome_padronizado = Column('nome_padronizado', String)

    def __init__(self, variacao, nome_padronizado):
        self.variacao = variacao
        self.nome_padronizado = nome_padronizado


def adicionar_banco(variacao, nome_padronizado):
    #Salvando no banco
    consultando = session.query(Bancos).filter(Bancos.variacao.ilike(variacao)).first()
    if consultando:
        print('Nome de Variação já existente')
        return False
    else:
        banco = Bancos(variacao, nome_padronizado)
        session.add(banco)
        session.commit()
        return True


def remover_banco(variacao):
    consulta = session.query(Bancos).filter_by(variacao = variacao).first() 

    if consulta:
        session.delete(consulta)
        session.commit()

# def consultar(variacao):
#     # variacao = str(input('Variação do nome do banco: '))
     
#     consulta = session.query(Bancos).filter_by(variacao = variacao).first() 

#     print(consulta.nome_padronizado)

if __name__ == '__main__':
    remover_banco('teste agora')
    # adicionar_banco('teste agora', 'agora teste')

