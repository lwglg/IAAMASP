# 🤖 IAAMSP – Exemplo

## TOC
- [🤖 IAAMSP – Exemplo](#-iaamsp--exemplo)
  - [TOC](#toc)
  - [Instalação de ambiente](#instalação-de-ambiente)
    - [Atualização de listagem de dependências](#atualização-de-listagem-de-dependências)
  - [O que deseja fazer?](#o-que-deseja-fazer)


## Instalação de ambiente

Para criar o ambiente virtual do Python na versão indicada e instalar as dependências de proejto, execute os seguintes comandos:

```bash
$ cd ./exemplo                              # Vai para a pasta do exemplo
exemplo$ python3 -m venv .venv              # Cria o ambiente virtual Python em .venv
exemplo$ source .venv/bin/activate          # Ativa o ambiente virtual no shell atual
exemplo$ pip install --ugrade pip           # Atualiza o PIP
exemplo$ pip install -r requirements.txt    # Instala as packages listadas em requirements.txt
```
> [!NOTE]
> Para testar o ambiente virtual, basta executar `python -V` e verificar se a versão é a correta.
>

### Atualização de listagem de dependências

Na pasta `exemplo`, execute o comando:

```bash
exemplo$ pip list --not-required --format freeze > requirements.txt
```

Isso apenas listará em `requirements.txt` as packages (e suas versões) primárias do projeto.

> [!NOTE]
> As dependências de desenvolvimento (stubs de tipos, `mypy` e `ruff` ) estão também listadas em `requirements.txt`. Talvez fosse interessante separá-las em um arquivo `requirements-dev.txt` ou até mesmo usar um package manager que facilite esse projeto, e.g. `poetry` ou `uv`.
>

--

## O que deseja fazer?
- [Voltar para a raíz](../README.md)
- [Voltar para a TOC](#toc)
