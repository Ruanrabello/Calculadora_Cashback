# Calculadora_Cashback

# 💰 Cashback App

Aplicação web full stack desenvolvida para cálculo de cashback, utilizando **FastAPI no backend** e **HTML + JavaScript no frontend**, com arquitetura baseada em API.

---

## 🚀 Funcionalidades

* Cálculo de cashback com base em regras de negócio
* Suporte a cliente **Normal** e **VIP**
* Aplicação de cupons de desconto
* Registro de consultas em banco de dados
* Histórico de consultas por endereço IP
* Integração frontend → backend via requisições HTTP

---

## 🧠 Regras de Negócio

* O cashback é calculado sobre o **valor final da compra (após desconto)**
* Cashback base: **5%**
* Compras **acima de R$ 500** recebem cashback **dobrado (10%)**
* Clientes VIP recebem **+10% de bônus sobre o cashback**

---

## 🧱 Arquitetura

```
Frontend (HTML/JavaScript)
        ↓
   API (FastAPI)
        ↓
Banco de Dados (SQLite)
```

---

## 🛠 Tecnologias Utilizadas

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* HTML
* JavaScript

---

## 🌐 Como Executar o Projeto Localmente

### 🔹 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

---

### 🔹 2. Criar ambiente virtual

```bash
python -m venv venv
```

#### Ativar o ambiente:

* Windows:

```bash
venv\Scripts\activate
```

* Linux/Mac:

```bash
source venv/bin/activate
```

---

### 🔹 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 🔹 4. Rodar o backend

```bash
uvicorn main:app --reload
```

---

### 🔹 5. Acessar a API

* Documentação automática (Swagger):

```
http://127.0.0.1:8000/docs
```

---

### 🔹 6. Rodar o frontend

Abra o arquivo:

```
index.html
```

no navegador

---

## ☁️ Deploy

* Backend hospedado no Render
* Frontend hospedado no Vercel

---

## 📡 Integração entre Frontend e Backend

O frontend realiza requisições HTTP utilizando `fetch()` para enviar dados ao backend.

O backend:

* recebe os dados
* processa a lógica de cashback
* salva no banco de dados
* retorna o resultado em formato JSON

O frontend então exibe o resultado na tela para o usuário.

---

## 🎯 Objetivo do Projeto

Projeto desenvolvido como desafio técnico com foco em demonstrar:

* Criação de APIs com FastAPI
* Validação de dados com Pydantic
* Integração com banco via SQLAlchemy
* Comunicação entre frontend e backend
* Estruturação de aplicações web modernas

---

## 🌍 Acesso ao Projeto (após deploy)

https://calculadora-cashback-w34p.vercel.app

---

## 👨‍💻 Autor

Ruan Rabello
