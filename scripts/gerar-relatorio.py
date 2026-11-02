"""Requer reportlab e pillow. Executar na raiz do projeto."""
import os
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
NAME=os.environ.get('ALUNO_NOME','Nome completo: a preencher')
REG=os.environ.get('ALUNO_MATRICULA','Matrícula: a preencher')
FONT='/System/Library/Fonts/Supplemental/'
pdfmetrics.registerFont(TTFont('Arial',FONT+'Arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold',FONT+'Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('Mono','/System/Library/Fonts/Monaco.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyPT',fontName='Arial',fontSize=10.5,leading=15,spaceAfter=10))
styles.add(ParagraphStyle(name='TitlePT',fontName='ArialBold',fontSize=26,leading=32,textColor=HexColor('#163c54'),spaceAfter=24))
styles.add(ParagraphStyle(name='HeadingPT',fontName='ArialBold',fontSize=16,leading=21,textColor=HexColor('#163c54'),spaceAfter=14))
styles.add(ParagraphStyle(name='CodePT',fontName='Mono',fontSize=7.3,leading=11,backColor=HexColor('#f0f3f6'),borderPadding=8,spaceAfter=14))
story=[]
def p(s): story.append(Paragraph(s,styles['BodyPT']))
def h(s): story.append(Paragraph(s,styles['HeadingPT']))
def code(s): story.append(Preformatted(s,styles['CodePT']))
def page(): story.append(PageBreak())

story.append(Spacer(1,55))
p('PUC | Teste de Software')
story.append(Paragraph('Detecção de Bad Smells<br/>e Refatoração Segura',styles['TitlePT']))
p('Trabalho prático 03 | Serviço de geração de relatórios em JavaScript')
story.append(Spacer(1,35))
p(escape(NAME)); p(escape(REG))
story.append(Spacer(1,35))
p('Repositório da entrega:<br/><link href="https://github.com/gabrielchagas13/bad-smells-js-refactoring">github.com/gabrielchagas13/bad-smells-js-refactoring</link>')
p('Data: 2 de novembro de 2026')
p('Base analisada: CleitonSilvaT/bad-smells-js-refactoring<br/>Commit: '+Path('evidencias/commit-base.txt').read_text().strip())
page()
h('1. Análise manual e detecção automática')
p('<b>Método longo e múltiplas responsabilidades.</b> generateReport mistura cabeçalho, autorização, prioridade, formatação e totalização. Uma mudança de apresentação exige percorrer regras de negócio; testar uma regra isolada fica difícil e os cenários se multiplicam.')
p('<b>Condicionais aninhadas.</b> O laço combina papel do usuário, valor do item e formato. Esse encadeamento aumenta o esforço para entender caminhos e identificar combinações não exercitadas pelos testes. O SonarJS mediu complexidade cognitiva 27, acima do limite 15.')
p('<b>Duplicação de lógica.</b> A linha CSV e a soma do total aparecem nos caminhos ADMIN e USER; a estrutura HTML também se repete. Alterar só um caminho pode gerar inconsistência entre os relatórios e exigir casos de teste redundantes.')
p('<b>Observação adicional.</b> Os valores 500 e 1000 são números mágicos: representam limites de visibilidade e prioridade. Constantes com nomes tornam a intenção explícita.')
p('Configuração: ESLint 8 e SonarJS 0.21, com eslint:recommended e plugin:sonarjs/recommended. Foram mantidas as regras adicionais da base; a complexidade foi ajustada de 5 para 15, conforme o enunciado. O original continua com dois erros.')
log=Path('evidencias/eslint-antes.txt').read_text()
# Reprodução visual fiel dos diagnósticos, com quebra das linhas para leitura.
lines=['$ npx eslint src/', 'src/ReportGenerator.js', '',
'11:3 error  Refactor this function to reduce its Cognitive',
'            Complexity from 27 to the 15 allowed',
'            sonarjs/cognitive-complexity',
'43:14 error Merge this if statement with the nested one',
'            sonarjs/no-collapsible-if', '', '2 problems (2 errors, 0 warnings)']
assert '27 to the 15 allowed' in log and 'sonarjs/no-collapsible-if' in log
img=PILImage.new('RGB',(1250,345),'#14202b'); draw=ImageDraw.Draw(img)
font=ImageFont.truetype('/System/Library/Fonts/Monaco.ttf',20)
for i,line in enumerate(lines): draw.text((22,18+i*30),line,font=font,fill='#e9f0f5')
img.save('evidencias/eslint-antes.png')
story.append(Image('evidencias/eslint-antes.png',width=475,height=131))
p('Figura 1. Reprodução visual da saída real capturada em evidencias/eslint-antes.txt; não é captura de tela. O SonarJS quantificou o aninhamento percebido manualmente e indicou a possibilidade de juntar condicionais. A duplicação e os números mágicos foram achados manuais, sem alerta específico nesta execução.')
page()
h('2. Processo de refatoração')
p('O ponto mais crítico foi a combinação de autorização e formatação no mesmo método. Foram aplicadas <b>Extract Method</b> e <b>Decompose Conditional</b>: canViewItem decide visibilidade; markPriority concentra o efeito colateral; selectFormatter escolhe um objeto de estratégia para CSV ou HTML. A formatação deixa de ser repetida em cada papel.')
p('<b>Antes</b> - trecho do ramo ADMIN em generateReport:')
code('''if (user.role === 'ADMIN') {
  if (item.value > 1000) {
    item.priority = true;
  }
  if (reportType === 'CSV') {
    report += `${item.id},${item.name},${item.value},${user.name}\\n`;
    total += item.value;
  } else if (reportType === 'HTML') {
    // Formata HTML e soma novamente.
  }
} // O ramo USER repete formatação e soma.''')
p('<b>Depois</b> - fluxo compartilhado da versão refatorada:')
code('''for (const item of items) {
  markPriority(user, item);
  if (!formatter || !canViewItem(user, item)) continue;
  report += formatter.row(item, user);
  total += item.value;
}''')
p('Os limites receberam os nomes STANDARD_USER_VALUE_LIMIT (500) e ADMIN_PRIORITY_THRESHOLD (1000). O construtor e a mutação de item.priority foram preservados, inclusive no caso de formato desconhecido, que continua retornando texto vazio.')
p('<b>Correção adicional, separada da refatoração:</b> o original emite &lt;tr &gt; para ADMIN sem prioridade; seu próprio teste exige &lt;tr&gt;. Na versão nova, o espaço faz parte do atributo opcional:')
code('''const style = user.role === 'ADMIN' && item.priority
  ? ' style="font-weight:bold;"' : '';
return `<tr${style}><td>${item.id}</td><td>${item.name}</td>` +
  `<td>${item.value}</td></tr>\\n`;''')
p('Essa mudança textual corrige a falha existente; portanto não se afirma equivalência byte a byte com o original. Nenhum arquivo original de produção ou de teste foi alterado.')
page()
h('3. Validação, limites e conclusão')
p('A instalação foi realizada com npm install. A primeira execução de npm test não carregava os imports ES Modules. O script passou a chamar o Jest com node --experimental-vm-modules, mantendo os testes intactos. Depois desse ajuste, a linha de base mostrou 4 testes aprovados e 1 falha preexistente no HTML de ADMIN.')
p('<b>Resultados efetivamente observados:</b>')
code('''Original:                          4/5 testes aprovados
Refatorado:                        5/5 testes aprovados
Suíte completa:                   9/10 testes aprovados
ESLint original:                   2 erros
ESLint refatorado:                 0 erros
Comparação complementar:          162 cenários aprovados''')
p('A cópia do teste difere somente no import para ReportGenerator.refactored.js. O original continua falhando pelo espaço em &lt;tr &gt;; corrigir esse arquivo violaria a orientação de preservá-lo. Assim, a exigência de 100% da suíte completa não é atendida pela base fornecida. O relatório não apresenta essa falha como regressão nem como sucesso.')
p('A comparação complementar percorreu três papéis (ADMIN, USER e OTHER), três formatos (CSV, HTML e INVALID), seis valores (0, 499, 500, 501, 1000 e 1001) e três estados de prioridade. Verificou igualdade de saída após normalizar somente &lt;tr &gt; e igualdade das mutações nos itens. Ela é reproduzível com node scripts/verificar-equivalencia.js.')
p('As evidências dos testes e do lint estão em evidencias/. Os comandos npm run test:refactored e npm run lint:refactored validam a implementação nova. npm test -- --runInBand mantém visível a falha preexistente; npm run lint também mantém os erros do original.')
p('<b>Conclusão.</b> Testes como rede de segurança precisam ser executados antes da mudança: foi essa etapa que revelou que a base não estava totalmente verde. A refatoração separou decisões e apresentação, reduziu o aninhamento e centralizou a lógica repetida. Os cinco testes fornecidos e a comparação adicional sustentam a mudança nos cenários cobertos, sem provar correção para todas as entradas possíveis. O erro do original deve ser discutido com o professor para conciliar sua preservação com a exigência de aprovação total.')
p('<b>Referências:</b> enunciado “Detecção de Bad Smells e Refatoração Segura”; repositório-base CleitonSilvaT/bad-smells-js-refactoring; Fowler, Martin. Refatoração: Aperfeiçoando o Design de Códigos Existentes. 2. ed., Novatec, 2019 (referência indicada no enunciado).')

def footer(c,doc):
    c.setStrokeColor(HexColor('#dce4e9')); c.line(58,45,537,45)
    c.setFont('Arial',8); c.setFillColor(HexColor('#526575'))
    c.drawString(58,31,'Teste de Software | Bad Smells e Refatoração Segura')
    c.drawRightString(537,31,str(doc.page))
SimpleDocTemplate('output/pdf/relatorio-bad-smells.pdf',pagesize=(595.28,841.89),rightMargin=58,leftMargin=58,topMargin=52,bottomMargin=60).build(story,onFirstPage=footer,onLaterPages=footer)
