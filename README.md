# Detecção de Bad Smells e Refatoração Segura

Entrega: https://github.com/gabrielchagas13/bad-smells-js-refactoring

Base: https://github.com/CleitonSilvaT/bad-smells-js-refactoring

## Executar

Requer Node.js 18 ou superior. Instale com `npm ci`.

- `npm test -- --runInBand`: executa as duas versões (9/10 testes passam; veja a falha preexistente abaixo).
- `npm run test:refactored`: 5/5 testes da versão refatorada passam.
- `npm run lint:refactored`: nenhum erro.
- `npm run lint`: analisa ambas as versões; os dois erros do original permanecem visíveis.
- `node scripts/verificar-equivalencia.js`: compara 162 cenários de papéis, formatos, limites e prioridades.

## Falha preexistente e preservação dos originais

O projeto-base usa ES Modules, mas seu comando Jest não os habilitava. O script de execução foi ajustado, sem modificar testes.
Após esse ajuste, o original passa em 4/5 testes: a linha HTML sem prioridade produz `<tr >`, enquanto o teste espera `<tr>`.
`src/ReportGenerator.js` e `tests/ReportGenerator.test.js` permanecem intactos.
A cópia `tests/ReportGenerator.refactored.test.js` difere somente no import.
A versão refatorada corrige o espaço na abertura de `<tr>` e passa nos cinco testes.
Essa correção é uma mudança textual deliberada, além da refatoração, e está documentada no relatório.
Não se afirma que a suíte completa passa: para isso seria necessário corrigir o original, contrariando a exigência de preservá-lo.

## Refatoração e análise

Método longo e condicionais aninhadas foram separados em funções de autorização, prioridade e formatadores CSV/HTML.
As linhas e o cálculo do total passaram a ser compartilhados entre os papéis. Os limites 500 e 1000 receberam nomes.
A mutação de `item.priority`, o construtor e o tratamento de formatos e papéis desconhecidos foram preservados.
O limite de complexidade cognitiva foi configurado em 15, como no PDF (a base usava 5).
O original tem complexidade cognitiva 27 e outro erro `sonarjs/no-collapsible-if`; o refatorado não apresenta erros.

O relatório de quatro páginas está em `output/pdf/relatorio-bad-smells.pdf`.
**Antes de entregar:** preencher nome completo e matrícula na capa pelo gerador `scripts/gerar-relatorio.py`.
Saídas reais dos comandos e commit da base estão em `evidencias/`.
A imagem do ESLint no relatório é uma reprodução visual da saída capturada, não uma captura de tela do terminal.

A suíte fornecida tem apenas cinco testes e não comprova correção para toda entrada possível. A comparação adicional cobre 162 combinações e preservação das mutações, sem substituir os testes originais.
