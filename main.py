from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Tente desta forma se a anterior persistir no erro:
BancodeDados = "postgresql://postgres.rzwigyotqpmejnesahak:ruran1234rabell7@aws-1-us-west-2.pooler.supabase.com:6543/postgres"
                                                                                                                                                                

engine = create_engine(BancodeDados, pool_size=10, max_overflow=20, pool_pre_ping=True)                                                                                                        
SessionLocal = sessionmaker(bind=engine)                                                                                                                        
Base = declarative_base()                                                                                                                                       


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConsultaSQL(Base):                                                                                                                                        
    __tablename__  = "Cashback"                                                                                                                                                                    

    id  = Column(Integer, primary_key=True, index=True)                                                                                                        
    ip = Column(String, index=True)                                                                                                                             
    Tipo_Cliente = Column(String, index=True)
    ValorCompra = Column(Float, index=True)
    valorCashback = Column(Float, index=True)

Base.metadata.create_all(bind=engine)                                                                                                                           


class DadosEntrada(BaseModel):                                                                                                                                 
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
        

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/calcular_cashback/")
def calcular_cashback(dados: DadosEntrada, request: Request, db: Session = Depends(get_db)):
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
        

        return {"cashback": Cashback}

    finally:
        db.close()

@app.get("/Historico_ip")
def historico_ip(request: Request, db: Session = Depends(get_db)):

    ip = request.client.host if request.client else "127.0.0.1"

    consultas = db.query(ConsultaSQL)\
        .filter(ConsultaSQL.ip == ip)\
        .order_by(ConsultaSQL.id.desc())\
        .limit(10)\
        .all()

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