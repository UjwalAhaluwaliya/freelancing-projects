const { stringify } = require('csv-stringify/sync');

const toCsv = (rows) => {
  return stringify(rows, { header: true });
};

module.exports = { toCsv };
