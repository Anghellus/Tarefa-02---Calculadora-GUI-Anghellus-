# Calculadora com FreeSimpleGUI

Calculadora gráfica em Python para as quatro operações básicas. A aplicação usa
`Decimal` para preservar a precisão dos cálculos decimais, informa entradas e
operações inválidas, impede divisão por zero e apresenta as dez operações mais
recentes. O botão **C** limpa o display, o estado atual e o histórico; **←**
apaga o último caractere digitado. O display aceita até 16 caracteres,
operadores consecutivos são rejeitados e os erros são apresentados como
`Erro: Divisão por zero` ou `Erro: Expressão inválida`.

## Requisitos

- Python 3.10 ou superior
- FreeSimpleGUI

## Instalação e execução

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Em ambientes nos quais o comando `py` não esteja disponível, crie o ambiente
virtual com `python -m venv .venv`.

## Testes

Os testes da lógica não precisam abrir a janela gráfica:

```powershell
python -m unittest -v
```

## Organização

- `main.py`: janela, botões e tratamento de eventos/erros da GUI.
- `calculadora.py`: operações, estado, validações e histórico.
- `test_calculadora.py`: testes automatizados da lógica e dos casos de erro.

## GitHub e GitHub Copilot

Para publicar, crie um repositório **público** no GitHub, associe-o a esta pasta
e envie o histórico com `git push`. Distribua o desenvolvimento em pelo menos
cinco commits significativos (por exemplo: estrutura, lógica, operações e
validações, interface gráfica, testes e documentação); não crie commits vazios
apenas para atingir uma contagem.

O GitHub Copilot pode auxiliar na geração e revisão de código, na criação de
testes e na documentação. Nesta atividade, a implementação e seus testes foram
preparados com assistência do Copilot; revise e execute o código antes de
publicá-lo. Um exemplo de prompt para documentar esse uso em outros commits:

> Usei o GitHub Copilot para sugerir casos de teste para as operações
> decimais e o tratamento de divisão por zero. Revisei as sugestões e executei
> os testes automatizados antes de aceitar as alterações.
