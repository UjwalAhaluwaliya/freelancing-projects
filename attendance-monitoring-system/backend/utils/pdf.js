const PDFDocument = require('pdfkit');

const buildPdfBuffer = (title, rows) => {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument({ margin: 40 });
    const chunks = [];

    doc.on('data', (chunk) => chunks.push(chunk));
    doc.on('end', () => resolve(Buffer.concat(chunks)));
    doc.on('error', reject);

    doc.fontSize(18).text(title);
    doc.moveDown();

    rows.forEach((row) => {
      doc.fontSize(11).text(Object.entries(row).map(([k, v]) => `${k}: ${v}`).join(' | '));
      doc.moveDown(0.5);
    });

    doc.end();
  });
};

module.exports = { buildPdfBuffer };
