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

def view_database():
    bancos = session.query(Bancos).all()

    # for banco in bancos:
    #     print(f'ID: {banco.id} | Variação: {banco.variacao} | Nome padrão: {banco.nome_padronizado}')
    
    for novo_id, banco in enumerate(bancos, start=1):
        banco.id = novo_id

    session.commit()

# def zerar():
#     session.execute("DELETE FROM sqlite_sequence WHERE name='bancos'")
#     session.commit()

if __name__ == '__main__':
    # remover_banco('teste agora')
    # adicionar_banco('bco do brasil', 'Banco do Brasil')
    view_database()
    # zerar()