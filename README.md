# Analisador Léxico RPN (FSM) + Geração de Assembly ARMv7

Projeto da fase de compiladores com foco em:

- leitura de arquivo com expressões RPN (uma por linha);
- análise léxica com AFD/FSM (estado por função, sem regex);
- geração de vetor de tokens;
- emissão de Assembly ARMv7 compatível com o modelo DEC1-SOC(v16.1) no CPULATOR.

## Estrutura

- `src/main.py`: fluxo principal + `exibirResultados`.
- `src/lexer.py`: `parseExpressao`.
- `src/fsm_estados.py`: estados `estadoInicial`, `estadoNumero`, `estadoOperador`, `estadoIdentificador`, `estadoEspaco`, `estadoErro`.
- `src/executor.py`: `executarExpressao` para infraestrutura de validação, histórico (`RES`) e memória.
- `src/assembly_generator.py`: `gerarAssembly` e persistência do `.s`.
- `src/io_arquivo.py`: leitura/escrita dos artefatos.
- `inputs/`: três arquivos de teste (`teste1.txt`, `teste2.txt`, `teste3.txt`), cada um com 10 linhas.
- `outputs/tokens_ultima_execucao.txt`: tokens da última execução.
- `outputs/ultimo_assembly.s`: última versão do assembly gerado.
- `tests/`: testes unitários e de integração.

## Tokens suportados

- `LPAREN`
- `RPAREN`
- `NUMERO_REAL`
- `OPERADOR` (`+`, `-`, `*`, `/`, `//`, `%`, `^`)
- `IDENT_MEM`
- `KEYWORD_RES`

## Regras principais atendidas

- FSM determinística com estado por função.
- Sem uso de regex.
- Arquivo de entrada passado por argumento de linha de comando.
- Sem menu interativo.
- Funções exigidas preservadas: `parseExpressao`, `executarExpressao`, `gerarAssembly`, `exibirResultados`.
- Persistência dos artefatos finais em `outputs/`.

## Como executar

```bash
python -m src.main inputs/teste3.txt
```

Isso gera/atualiza:

- `outputs/tokens_ultima_execucao.txt`
- `outputs/ultimo_assembly.s`

## Como testar

```bash
python -m unittest discover -s tests -v
```

## Observações de implementação

- Números com vírgula e múltiplos pontos são rejeitados pelo lexer.
- Parênteses desbalanceados são reportados com linha/coluna.
- `RES` usa histórico de resultados (N linhas anteriores).
- Memória nomeada é tratada por identificadores maiúsculos (`IDENT_MEM`), com default `0.0` quando não inicializada.
