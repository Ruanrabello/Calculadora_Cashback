from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

BancodeDados = 'sqlite:///banco_de_dados.db'                                                                                                                    # String de conexão com o banco

engine = create_engine(BancodeDados, connect_args={"check_same_thread": False})                                                                                 # Cria a conexão com o banco usando o SQLAlchemy.
SessionLocal = sessionmaker(bind=engine)                                                                                                                        # Cria uma classe de sessão para interagir com o banco de dados. A sessão é usada para realizar operações como consultas e inserções no banco.
Base = declarative_base()                                                                                                                                       # Cria a classe base para os modelos do SQLAlchemy. Todos os modelos de banco de dados herdarão desta classe.



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConsultaSQL(Base):                                                                                                                                        # criando uma classe Python que representa uma tabela no banco usando o SQLAlchemy ORM (Object-Relational Mapping). Essa classe define a estrutura da tabela e os tipos de dados para cada coluna.
    __tablename__  = "Cashback"                                                                                                                                 # Define o nome da tabela no banco de dados como "Cashback".                                      

    id  = Column(Integer, primary_key=True, index=True)                                                                                                         # Define a coluna "id" como um inteiro, que é a chave primária da tabela e é indexada para melhorar o desempenho das consultas.
    ip = Column(String, index=True)                                                                                                                             # Define a coluna "ip" como uma string e a indexa para melhorar o desempenho das consultas. 
    Tipo_Cliente = Column(String, index=True)
    ValorCompra = Column(Float, index=True)
    valorCashback = Column(Float, index=True)

Base.metadata.create_all(bind=engine)                                                                                                                           # Cria a tabela no banco de dados com base na definição da classe ConsultaSQL. Se a tabela já existir, ela não será recriada.                                 


class DadosEntrada(BaseModel):                                                                                                                                  # O ip nao entra aqui pq no caso ele é gerado automaticamente, entao nao precisa ser passado pelo usuario.
    TipoCliente: str
    ValorCompra: float
    cupom: float

def ValorCashback(TipoCliente, ValorCompra, cupom):
    precoFinal = ValorCompra - (ValorCompra / 100) * cupom

    if TipoCliente.lower() == "normal":
        cashback = 0
        if precoFinal < 500:
            cashback = (precoFinal / 100) * 5
            return cashback
        else:
            cashback = (precoFinal / 100) * 10
            return cashback
    
    elif TipoCliente.lower() == "vip":
        cashback = 0
        if precoFinal < 500:
            cashback = ((precoFinal / 100) * 5) + ((((precoFinal / 100) * 5) / 100)* 10)
            return cashback
        else:
            cashback = ((precoFinal / 100) * 10) + ((((precoFinal / 100) * 10) / 100) * 10)
            return cashback
        

@app.post("/calcular_cashback/")                                                                                                                                    # Define um endpoint POST em "/calcular_cashback/" que recebe os dados de entrada para calcular o cashback.
def calcular_cashback(dados: DadosEntrada, request: Request):                                                                                                       # Define a função que será executada quando o endpoint for chamado. Ela recebe um objeto "dados" do tipo "DadosEntrada", que contém os dados necessários para calcular o cashback.
    db = SessionLocal()                                                                                                                                             # Cria uma nova sessão para interagir com o banco de dados.
    ip_cliente = request.client.host if request.client else "127.0.0.1"                                                                                             # Obtém o endereço IP do cliente que fez a solicitação usando a biblioteca "requests". O endereço IP é usado para registrar a origem da solicitação no banco de dados.

    Cashback = ValorCashback(TipoCliente=dados.TipoCliente, ValorCompra=dados.ValorCompra, cupom=dados.cupom)  
    novo_ConsultaSQL = ConsultaSQL(ip = ip_cliente, Tipo_Cliente=dados.TipoCliente, ValorCompra=dados.ValorCompra, valorCashback=Cashback)                          # Cria um novo objeto "ConsultaSQL" com os dados do cliente e o valor do cashback calculado.
    db.add(novo_ConsultaSQL)                                                                                                                                        # Adiciona o novo objeto "ConsultaSQL" à sessão do banco de dados.
    db.commit()                                                                                                                                                     # Salva as alterações no banco de dados, ou seja, insere o novo registro na tabela "Cashback".
    db.refresh(novo_ConsultaSQL)                                                                                                                                    # Atualiza o objeto "novo_ConsultaSQL" com os dados do banco de dados, como o ID gerado automaticamente.

    return {"cashback": Cashback}

@app.get("/Historico_ip")
def historico_ip(request: Request):
    db = SessionLocal()
    ip = request.client.host if request.client else "127.0.0.1"    
    consultas = db.query(ConsultaSQL).filter(ConsultaSQL.ip == ip).all()                                                                                            # Consulta o banco de dados para obter todas as consultas feitas pelo endereço IP do cliente.
    return {
    "historico": [
        {
            "Tipo_Cliente": c.Tipo_Cliente,
            "ValorCompra": c.ValorCompra,
            "valorCashback": c.valorCashback
        }
        for c in consultas
    ]
}                                                                                                                                # Retorna o histórico de consultas para o cliente.