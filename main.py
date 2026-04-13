from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Tente desta forma se a anterior persistir no erro:
BancodeDados = "postgresql://postgres.rzwigyotqpmejnesahak:ruran1234rabell7@aws-1-us-west-2.pooler.supabase.com:6543/postgres"
                                                                                                                                                                # String de conexão com o banco

engine = create_engine(BancodeDados, pool_pre_ping=True)                                                                                                        # Cria a conexão com o banco usando o SQLAlchemy.
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
        

@app.post("/calcular_cashback/")
def calcular_cashback(dados: DadosEntrada, request: Request):
    db = SessionLocal()
    try:
        ip_cliente = request.client.host if request.client else "127.0.0.1"

        Cashback = ValorCashback(
            TipoCliente=dados.TipoCliente,
            ValorCompra=dados.ValorCompra,
            cupom=dados.cupom
        )

        novo_ConsultaSQL = ConsultaSQL(
            ip=ip_cliente,
            Tipo_Cliente=dados.TipoCliente,
            ValorCompra=dados.ValorCompra,
            valorCashback=Cashback
        )

        db.add(novo_ConsultaSQL)
        db.commit()
        db.refresh(novo_ConsultaSQL)

        return {"cashback": Cashback}

    finally:
        db.close()


@app.get("/Historico_ip")
def historico_ip(request: Request):
    db = SessionLocal()
    try:
        ip = request.client.host if request.client else "127.0.0.1"

        consultas = db.query(ConsultaSQL).filter(
            ConsultaSQL.ip == ip
        ).all()

        return {
            "historico": [
                {
                    "Tipo_Cliente": c.Tipo_Cliente,
                    "ValorCompra": c.ValorCompra,
                    "valorCashback": c.valorCashback
                }
                for c in consultas
            ]
        }

    finally:
        db.close()                                                                                                                         # Retorna o histórico de consultas para o cliente.