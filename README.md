
# 📄 Projeto: Leitor de Boletos em PDF

## 🧾 Objetivo

Desenvolver um sistema para **ler boletos bancários em formato PDF**, extrair informações essenciais e classificar os boletos de acordo com o CNPJ do beneficiário ou pagador.

Este projeto retorna os boletos com os dados extraídos em um arquivo **CSV** e também salva as informações em um **banco de dados SQLite**. Esses dados alimentam um outro sistema de **agendamento e alerta de vencimento** de contas.

---

## 📂 Estrutura de Pastas

```
utils/
├── scripts_models/
│   ├── sicredi_v1.py
│   ├── sicredi_v2.py
│   ├── bb_v1.py
│   ├── bradesco_v1.py
│   └── itau_v1.py
├── regex.py
├── normalizar_cnpj.py
```

Cada arquivo representa um modelo específico de leitura, adaptado ao layout do banco emissor.

---

## 🏦 Suporte a Múltiplos Bancos

O sistema foi desenvolvido para lidar com boletos de diversas instituições financeiras, incluindo:

- **Sicredi**
- **Banco do Brasil (BB)**
- **Bradesco**
- **Itaú**

Cada banco possui **formatações diferentes nos boletos**. Nem sempre os dados estão na mesma posição ou "caixa" visual. Por isso, foram criadas **diferentes versões de leitura** (como `v1`, `v2`, etc.) para lidar corretamente com cada variação de layout.

Essas variações são identificadas automaticamente a partir do **texto extraído do PDF (via .txt)**.

---

## 🔍 Identificação de Layout

A função `identificar_layout(texto)` detecta o layout do boleto com base em palavras-chave, como `Sicredi`, `748-X`, `CNPJ:`, e `Corte na linha abaixo`:

```python
def identificar_layout(texto):
    if "Sicredi" in texto or "748-X" in texto:
        if "CNPJ:" in texto and "Corte na linha abaixo" in texto:
            return "sicredi_v2"
        elif "748-X Recibo do Pagador" in texto:
            return "sicredi_v1"
```

---

## 📌 Campos Extraídos

### ✅ Data de Processamento
```python
if "Data Processamento" in linha or "Data de Processamento" in linha:
    data_proc = buscar_regex(r'\d{2}/\d{2}/\d{4}', linhas[i+1])
    if data_proc:
        dados["data_processamento"] = data_proc[-1]
```

### ✅ Número do Documento e Nosso Número
```python
if re.search(r'\d{2}/\d{2}/\d{4}.*?DMI', linha):
    dados["numero_documento"] = buscar_regex(r'\d{2}/\d{2}/\d{4}\s+([0-9\-]+)', linha)
    dados["nosso_numero"] = buscar_regex(r'(25/\d{6}-\d)', linha)
```

### ✅ Valor do Documento
```python
dados["valor_documento"] = buscar_regex(r'R\$?\s*([\d\.,]+)', linhas[i+1])
```

---

## 🔍 Classificação do Boleto

Com base no CNPJ de sua empresa, o sistema classifica:

- **Cobrança** → quando este CNPJ é o **beneficiário**
- **Pagamento** → quando este CNPJ é o **pagador**

---

## 🛠️ Outras Funcionalidades

- Importação dinâmica de modelos de layout
- Normalização de CNPJ e remoção de ruído com regex
- Estratégias de extração por linha com base em contexto (ex: `i+1` para pegar valores abaixo dos títulos)
- Organização modular por layout
- Exportação de dados para `.csv` e base de dados `.db` (SQLite)


---

## 🤖 Futuro com Machine Learning

O projeto foi pensado para ser **escalável e adaptável**. Futuramente, o objetivo é incorporar técnicas de **Machine Learning (ML)** para:

- Detectar **novos padrões de boletos** automaticamente
- Substituir a identificação manual de layout por modelos treinados
- Tornar a extração mais inteligente, mesmo com layouts pouco estruturados

### 📁 Salvamento dos `.txt`

Todos os textos extraídos dos PDFs são **automaticamente salvos em uma pasta específica**. Isso cria uma **base de dados de exemplos reais**, que servirá para **treinar modelos de ML** no futuro.

Dessa forma, ao invés do programador precisar ler e identificar os padrões manualmente, um modelo poderá ser treinado para **reconhecer layouts e extrair campos dinamicamente**, aumentando a escalabilidade do sistema.

---

