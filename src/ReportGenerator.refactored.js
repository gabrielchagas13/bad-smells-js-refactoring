const STANDARD_USER_VALUE_LIMIT = 500;
const ADMIN_PRIORITY_THRESHOLD = 1000;

function canViewItem(user, item) {
  return user.role === 'ADMIN' ||
    (user.role === 'USER' && item.value <= STANDARD_USER_VALUE_LIMIT);
}

function markPriority(user, item) {
  if (user.role === 'ADMIN' && item.value > ADMIN_PRIORITY_THRESHOLD) {
    item.priority = true;
  }
}

const csvFormatter = {
  header: () => 'ID,NOME,VALOR,USUARIO\n',
  row: (item, user) => `${item.id},${item.name},${item.value},${user.name}\n`,
  footer: total => `\nTotal,,\n${total},,\n`,
};

const htmlFormatter = {
  header: user => '<html><body>\n<h1>Relatório</h1>\n' +
    `<h2>Usuário: ${user.name}</h2>\n<table>\n` +
    '<tr><th>ID</th><th>Nome</th><th>Valor</th></tr>\n',
  row(item, user) {
    const style = user.role === 'ADMIN' && item.priority
      ? ' style="font-weight:bold;"' : '';
    return `<tr${style}><td>${item.id}</td><td>${item.name}</td>` +
      `<td>${item.value}</td></tr>\n`;
  },
  footer: total => `</table>\n<h3>Total: ${total}</h3>\n</body></html>\n`,
};

function selectFormatter(reportType) {
  if (reportType === 'CSV') return csvFormatter;
  if (reportType === 'HTML') return htmlFormatter;
  return null;
}

export class ReportGenerator {
  constructor(database) {
    this.db = database;
  }

  generateReport(reportType, user, items) {
    const formatter = selectFormatter(reportType);
    let report = formatter ? formatter.header(user) : '';
    let total = 0;

    for (const item of items) {
      // Preserve o efeito colateral original inclusive para formatos desconhecidos.
      markPriority(user, item);
      if (!formatter || !canViewItem(user, item)) continue;
      report += formatter.row(item, user);
      total += item.value;
    }

    if (formatter) report += formatter.footer(total);
    return report.trim();
  }
}
