const Attendance = require('../models/Attendance');
const { toCsv } = require('../utils/csv');
const { buildPdfBuffer } = require('../utils/pdf');

const getReportRows = async ({ studentId, classId, subjectId }) => {
  const query = {};
  if (studentId) query.studentId = studentId;
  if (classId) query.classId = classId;
  if (subjectId) query.subjectId = subjectId;

  const rows = await Attendance.find(query)
    .populate('studentId', 'name email')
    .populate('subjectId', 'subjectName')
    .populate('classId', 'className semester department')
    .sort({ date: -1 });

  return rows.map((row) => ({
    date: row.date.toISOString().slice(0, 10),
    student: row.studentId?.name || '',
    email: row.studentId?.email || '',
    class: row.classId ? `${row.classId.className} Sem-${row.classId.semester}` : '',
    subject: row.subjectId?.subjectName || '',
    status: row.status
  }));
};

const exportAttendance = async (req, res, next) => {
  try {
    const format = (req.query.format || 'csv').toLowerCase();
    const rows = await getReportRows(req.query);

    if (format === 'pdf') {
      const buffer = await buildPdfBuffer('Attendance Report', rows);
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader('Content-Disposition', 'attachment; filename=attendance-report.pdf');
      return res.send(buffer);
    }

    const csv = toCsv(rows);
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename=attendance-report.csv');
    return res.send(csv);
  } catch (error) {
    next(error);
  }
};

module.exports = { exportAttendance };
