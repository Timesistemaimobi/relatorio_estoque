# Relatório de Estoque VCA

Projeto para gerar automaticamente o relatório Excel zebrado de estoque de unidades a partir de CSVs locais e da API CVCRM.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração do `.env`

1. Copie o arquivo `.env.example` para `.env`.
2. Preencha `CVCRM_EMAIL` e `CVCRM_TOKEN` com suas credenciais.

```bash
cp .env.example .env
```

## Entradas

Coloque os arquivos de entrada em:

- `data/unidade.csv`
- `data/bloqueio.csv`
- `templates/RELATORIO_TEMPLATE.xlsx`

### Exemplo de colunas necessárias (`unidade.csv`)

Separador `;`.

- Empreendimento
- Etapa
- Bloco
- Unidade
- Tipologia
- Situação
- Código interno da unidade (idunidade do CVCRM)
- ID. Empreendimento

### Exemplo de colunas necessárias (`bloqueio.csv`)

Separador `;`.

- Empreendimento
- Etapa
- Bloco
- Unidade
- Motivo do Bloqueio
- (Opcional) Data do Bloqueio

## Execução

```bash
python -m src.main
```

O arquivo gerado será salvo em `output/` com data no nome (YYYY-MM-DD).
