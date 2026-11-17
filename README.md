# 📦 SampFlow

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0%2B-092E20?logo=django)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)

> [English](#english-version) | [Português](#versão-em-português)

---

<a id="english-version"></a>
## 🌐 English Version

### 📖 About SampFlow
**SampFlow** is a modern, Django-based SaaS management platform designed to replace spreadsheet-heavy workflows for tracking, managing, and dispatching physical samples. 

While the system is currently developed using the green coffee export niche as its primary reference implementation, **SampFlow's architecture is versatile and modular**, making it easily adaptable to sample shipping workflows across a wide range of industries—including agricultural commodities, food and beverage, manufacturing, specialty chemicals, and textiles.

SampFlow centralizes end-to-end sample operations: from client registration and multi-stage courier tracking to real-time freight analytics and automated export document generation (Commercial Invoices).

---

### 🚀 Key Features

* **📦 Sample Management & Workflow Tracking**:
  * Track samples across multiple workflow stages: *Pré embarque* (Pre-shipment), *Embarque* (Shipment), and *Amostra Comercial* (Commercial Sample).
  * Real-time dispatch statuses: *Pendente* (Pending), *Aguardando coleta* (Awaiting collection), *Em Trânsito* (In Transit), and *Concluído* (Completed).
  * Comprehensive courier integration: carrier selection (FedEx, Correios, DHL, UPS), tracking codes, shipping/delivery dates, and standardized packaging choices.
  * Quality & specification fields: screen size / grading (*peneira*), sensory/cupping ratings, contract references, and reference month/batch.
  * Smart weight parser: automatic parsing and conversion of net weight and gross weight in grams (`g`) or kilograms (`kg`).
  * Image validation & storage: secure upload of PNG/JPEG sample photos, validated via Pillow and served dynamically with HTTP caching.
  * Real-time client-side search: instant search and filtering by contract ID, client name, or sample type.

* **👥 Client Management (CRM)**:
  * Centralized registry of domestic and international buyers, partners, and recipients.
  * Stores company name, destination country, full address, email, and phone contact.
  * Intuitive interface with modal-driven creation, inline editing, and deletion.

* **📄 Automated Commercial Invoice PDF Generation**:
  * One-click generation of standardized export Commercial Invoices.
  * Automatically calculates FCA USD values, gross/net weights, loading airport (*Viracopos, Brazil*), and discharge destination.
  * Generates pixel-perfect PDF layouts with **ReportLab** and merges them vectorially onto an official letterhead template (`letterhead.pdf`) using **PyMuPDF**.

* **📊 Interactive Freight & Logistics Dashboard**:
  * Monthly analytics of shipment expenses with currency formatting (BRL).
  * Key performance metrics: total logistics expenditure, total dispatched samples, and average cost per shipment.
  * Dynamic filtering by month, courier, client, and sample type without requiring page reloads.
  * Interactive progress bars visualizing cost distribution per client, alongside a detailed shipment data table.

* **🔒 Authentication & Security**:
  * Flexible authentication flow supporting login with either username or registered email.
  * Global route protection via a custom `LoginRequiredMiddleware`.
  * Secure session management and password recovery interface structure.

---

### 🛠️ Technologies Used

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | [Python 3.10+](https://www.python.org/) | Core programming language |
| **Framework** | [Django 6.0+](https://www.djangoproject.com/) | High-level Python web framework (MVT architecture) |
| **Configuration** | [python-decouple](https://github.com/HBNetwork/python-decouple) | Secure management of environment variables and secrets (`.env`) |
| **Database** | [SQLite3](https://www.sqlite.org/) | Relational database with query-optimized indexing |
| **PDF Processing** | [ReportLab](https://www.reportlab.com/) & [PyMuPDF](https://pymupdf.readthedocs.io/) | Dynamic document generation and vector letterhead overlay |
| **Image Processing** | [Pillow (PIL)](https://python-pillow.org/) | Image verification, security checks, and MIME type handling |
| **Frontend** | HTML5, Modern CSS3, JavaScript (ES6+) | Custom responsive layout, tab navigation, and `localStorage` state persistence |
| **Icons** | [Lucide Icons](https://lucide.dev/) | Clean, modern vector icon set |

---

### 📂 Project Structure

```text
SampFlow/
├── accounts/                  # Authentication app (login, logout, password recovery)
│   ├── templates/             # Auth-specific HTML templates
│   ├── views.py               # Authentication views (email/username login)
│   └── urls.py                # Accounts routing
├── home/                      # Core business logic app
│   ├── assets/                # PDF assets (letterhead.pdf template)
│   ├── invoice.py             # ReportLab & PyMuPDF invoice generation engine
│   ├── models.py              # Client and Sample models & business logic
│   ├── templates/             # Main application views (home.html)
│   ├── tests.py               # Automated test suite (invoices, weights, routes)
│   ├── urls.py                # CRUD and invoice endpoints
│   └── views.py               # Request handlers, validations, and dashboard datasets
├── sampflow/                  # Django project configuration
│   ├── middleware.py          # Custom LoginRequiredMiddleware
│   ├── settings.py            # Global project settings
│   ├── urls.py                # Root URL dispatcher
│   └── wsgi.py / asgi.py      # WSGI and ASGI entry points
├── templates/
│   └── static/                # Static assets (CSS, JS, images, favicon)
│       ├── accounts/          # Login and auth stylesheets/scripts
│       ├── home/              # Dashboard and samples scripts and styles
│       └── img/               # UI graphics and brand assets
├── .env.example               # Environment variables template
├── manage.py                  # Django CLI management script
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

---

### 💻 Getting Started & How to Run

#### 1. Prerequisites
* **Python 3.10** or higher installed.
* `git` installed.

#### 2. Clone the Repository
```bash
git clone <repository-url>
cd "Sample Project"
```

#### 3. Set Up a Virtual Environment
* **On Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Configure Environment Variables
Create a `.env` file in the project root based on `.env.example`:
```ini
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

#### 6. Run Migrations
Initialize the database schema:
```bash
python manage.py migrate
```

#### 7. Create an Admin User
```bash
python manage.py createsuperuser
```
Follow the interactive prompts to define your username, email, and password.

#### 8. Start the Development Server
```bash
python manage.py runserver
```
Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

### 🧭 How to Use SampFlow

1. **Sign In**: Access the login page and authenticate using your username or registered email address.
2. **Register Clients**:
   * Navigate to the **CLIENTES** tab.
   * Fill out the client form on the right (Company name, country, address, email, phone) and click **REGISTRAR CLIENTE**.
3. **Register & Track Samples**:
   * Navigate to the **AMOSTRAS** tab.
   * Click the **`+`** button to open the registration modal.
   * Select the client, specify contract numbers, sample type, status, courier, tracking code, quality metrics, weights, and optional sample photo.
   * Use the search bar to instantly filter samples by contract, client, or type.
   * Click **Detalhes** on any card to view extended information or edit records.
4. **Generate Invoices**:
   * On any sample card, click the **Gerar invoice** button.
   * An export-ready commercial invoice PDF will be generated immediately, pre-filled and merged onto the official letterhead.
5. **Analyze Logistics Costs**:
   * Go to the **DASHBOARDS** tab.
   * Filter costs by month, courier, client, or sample type to inspect total spending, average costs, and individual shipment histories.

---
---

<a id="versão-em-português"></a>
## 🇧🇷 Versão em Português

### 📖 Sobre o SampFlow
O **SampFlow** é uma plataforma SaaS moderna desenvolvida em Django concebida para substituir o controle manual em planilhas de envio, rastreamento e documentação de amostras físicas.

Embora o nicho de exportação de café verde seja atualmente utilizado como referência prática de desenvolvimento, **a arquitetura do SampFlow é flexível e modular**, aplicando-se com facilidade à gestão de remessa de amostras em diversas outras áreas — como commodities agrícolas em geral, alimentos e bebidas, manufatura, químicos especiais e têxtil.

O SampFlow centraliza toda a esteira operacional: do cadastro de clientes e acompanhamento com transportadoras até a análise em tempo real dos custos de frete e a emissão automatizada de documentos de exportação (*Commercial Invoices*).

---

### 🚀 Funcionalidades Principais

* **📦 Gestão e Rastreamento de Amostras**:
  * Organização do fluxo de amostras por etapas: *Pré embarque*, *Embarque* e *Amostra Comercial*.
  * Controle de status em tempo real: *Pendente*, *Aguardando coleta*, *Em Trânsito* e *Concluído*.
  * Gestão logística detalhada: transportadoras homologadas (FedEx, Correios, DHL, UPS), código de rastreio, datas de envio/entrega e tipos de embalagem padronizados.
  * Informações técnicas e de qualidade: classificação/tamanho de peneira, notas sensoriais/avaliação, número de contrato e lote/mês de referência.
  * Processamento inteligente de pesos: conversão e formatação automática de peso líquido e peso bruto em gramas (`g`) ou quilogramas (`kg`).
  * Validação e upload de fotos: envio seguro de imagens PNG/JPEG com verificação por Pillow e entrega com cabeçalhos de cache HTTP.
  * Busca instantânea no navegador: filtro em tempo real por número de contrato, cliente ou tipo de amostra.

* **👥 Gestão de Clientes (CRM)**:
  * Cadastro centralizado de compradores, parceiros comerciais e destinatários nacionais ou internacionais.
  * Armazenamento de empresa, país de destino, endereço completo, e-mail e telefone de contato.
  * Interface dinâmica com criação via formulário, edição em modal e exclusão segura.

* **📄 Emissão Automatizada de Commercial Invoice (PDF)**:
  * Emissão de faturas comerciais de exportação com apenas 1 clique.
  * Preenchimento automatizado de valores aduaneiros (FCA USD), pesos bruto e líquido, aeroporto de embarque (*Viracopos, Brasil*) e aeroporto/país de destino.
  * Geração dinâmica via **ReportLab** combinada com sobreposição vetorial ao modelo timbrado oficial (`letterhead.pdf`) através do **PyMuPDF**.

* **📊 Dashboard Financeiro e Logístico**:
  * Painel analítico mensal de custos de frete em Reais (BRL).
  * Indicadores-chave em tempo real: gasto logístico total, quantidade de remessas e custo médio por envio.
  * Filtros dinâmicos por mês, transportadora, cliente e tipo de amostra sem recarregar a página.
  * Barras de progresso com distribuição de custos por cliente e tabela detalhada de histórico de envios.

* **🔒 Autenticação e Segurança**:
  * Sistema de autenticação flexível com suporte a login por nome de usuário ou e-mail cadastrado.
  * Proteção global de rotas restritas via middleware dedicado (`LoginRequiredMiddleware`).
  * Encerramento de sessão seguro e estrutura preparada para recuperação de senha.

---

### 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia | Descrição |
| :--- | :--- | :--- |
| **Backend** | [Python 3.10+](https://www.python.org/) | Linguagem de programação principal |
| **Framework Web** | [Django 6.0+](https://www.djangoproject.com/) | Framework web em arquitetura MVT |
| **Configurações** | [python-decouple](https://github.com/HBNetwork/python-decouple) | Gestão segura de variáveis de ambiente e credenciais (`.env`) |
| **Banco de Dados** | [SQLite3](https://www.sqlite.org/) | Banco de dados relacional com índices otimizados |
| **Processamento de PDF** | [ReportLab](https://www.reportlab.com/) & [PyMuPDF](https://pymupdf.readthedocs.io/) | Criação de documentos PDF e mesclagem vetorial com papel timbrado |
| **Processamento de Imagens** | [Pillow (PIL)](https://python-pillow.org/) | Verificação de integridade, formato e tipos MIME de imagens |
| **Frontend** | HTML5, CSS3 Moderno, JavaScript (ES6+) | Layout responsivo, navegação por abas e persistência com `localStorage` |
| **Ícones** | [Lucide Icons](https://lucide.dev/) | Pacote moderno e leve de ícones vetoriais |

---

### 📂 Estrutura do Projeto

```text
SampFlow/
├── accounts/                  # Módulo de autenticação (login, logout, recuperação de senha)
│   ├── templates/             # Telas de login e redefinição
│   ├── views.py               # Lógica de autenticação com suporte a e-mail/usuário
│   └── urls.py                # Rotas do módulo accounts
├── home/                      # Módulo principal da aplicação
│   ├── assets/                # Arquivos base (letterhead.pdf timbrado)
│   ├── invoice.py             # Motor de geração de PDF com ReportLab e PyMuPDF
│   ├── models.py              # Modelos Client e Sample com propriedades de peso e imagem
│   ├── templates/             # Interface principal do sistema (home.html)
│   ├── tests.py               # Testes automatizados de invoices, pesos e rotas
│   ├── urls.py                # Rotas para CRUD de amostras, clientes e invoices
│   └── views.py               # Lógica de controle, validação de arquivos e dados do dashboard
├── sampflow/                  # Configuração do projeto Django
│   ├── middleware.py          # LoginRequiredMiddleware para proteção de rotas
│   ├── settings.py            # Configurações gerais do projeto
│   ├── urls.py                # Roteador raiz
│   └── wsgi.py / asgi.py      # Pontos de entrada para servidores de aplicação
├── templates/
│   └── static/                # Arquivos estáticos (CSS, JS, imagens, favicons)
│       ├── accounts/          # Estilos e scripts da área de login
│       ├── home/              # Estilos e scripts do painel, amostras e dashboard
│       └── img/               # Imagens de fundo e ícones
├── .env.example               # Modelo de variáveis de ambiente
├── manage.py                  # Utilitário de linha de comando do Django
├── requirements.txt           # Lista de dependências do Python
└── README.md                  # Documentação do projeto
```

---

### 💻 Instalação e Execução

#### 1. Pré-requisitos
* **Python 3.10** ou superior instalado.
* `git` instalado.

#### 2. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd "Sample Project"
```

#### 3. Criar e Ativar o Ambiente Virtual
* **No Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **No macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

#### 4. Instalar as Dependências
```bash
pip install -r requirements.txt
```

#### 5. Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`:
```ini
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
```

#### 6. Aplicar as Migrações do Banco de Dados
```bash
python manage.py migrate
```

#### 7. Criar um Superusuário (Administrador)
```bash
python manage.py createsuperuser
```
Siga as instruções no terminal para definir nome de usuário, e-mail e senha.

#### 8. Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```
Acesse no seu navegador: **`http://127.0.0.1:8000/`**

---

### 🧭 Como Usar o SampFlow

1. **Acessar o Sistema**: Faça login utilizando seu nome de usuário ou e-mail cadastrado.
2. **Cadastrar Clientes**:
   * Acesse a aba **CLIENTES**.
   * Preencha o formulário à direita (Nome da Empresa, País, Endereço, E-mail, Telefone) e clique em **REGISTRAR CLIENTE**.
3. **Cadastrar e Rastrear Amostras**:
   * Vá para a aba **AMOSTRAS**.
   * Clique no botão **`+`** para abrir o modal de cadastro.
   * Escolha o cliente, preencha os dados do contrato, tipo de amostra, status, transportadora, código de rastreio, peneira/classificação, notas técnicas, pesos (líquido e bruto) e anexe uma foto da amostra se desejar.
   * Utilize o campo de busca no topo para pesquisar rapidamente por contrato, cliente ou tipo.
   * Clique em **Detalhes** no card da amostra para visualizar os dados complementares, foto e opções de edição.
4. **Gerar Faturas Comerciais (Commercial Invoice)**:
   * No card da amostra desejada, clique em **Gerar invoice**.
   * O sistema gerará instantaneamente o arquivo PDF padronizado para exportação, mesclado com o papel timbrado oficial da empresa.
5. **Acompanhar os Custos no Dashboard**:
   * Acesse a aba **DASHBOARDS**.
   * Filtre por mês, transportadora, cliente ou tipo de amostra para avaliar os gastos totais, média de frete e listagem individual de remessas.

---

## 📄 License & Copyright / Licença e Direitos Autorais

Copyright (c) 2026 [Arthur Soares Abiviolo]. All rights reserved.

This software and associated documentation files (the "Software") are the proprietary property of [Arthur Soares Abiviolo]. Unauthorized copying, modification, distribution, or use of this file, via any medium, is strictly prohibited.
