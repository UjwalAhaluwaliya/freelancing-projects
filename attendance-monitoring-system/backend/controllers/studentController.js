const Attendance = require('../models/Attendance');
const LeaveRequest = require('../models/LeaveRequest');
const Subject = require('../models/Subject');

const getMyAttendance = async (req, res, next) => {
  try {
    const rows = await Attendance.find({ studentId: req.user._id }).populate('subjectId', 'subjectName');

    const grouped = {};
    rows.forEach((row) => {
      const subjectName = row.subjectId?.subjectName || 'Unknown';
      if (!grouped[subjectName]) grouped[subjectName] = { present: 0, total: 0 };
      grouped[subjectName].total += 1;
      if (row.status === 'present') grouped[subjectName].present += 1;
    });

    const subjectWise = Object.entries(grouped).map(([subjectName, data]) => ({
      subjectName,
      percentage: Number(((data.present / data.total) * 100).toFixed(2)),
      present: data.present,
      total: data.total
    }));

    const totalPresent = rows.filter((row) => row.status === 'present').length;
    const overall = rows.length ? Number(((totalPresent / rows.length) * 100).toFixed(2)) : 0;

    res.json({ overallPercentage: overall, subjectWise, totalRecords: rows.length });
  } catch (error) {
    next(error);
  }
};

const submitLeaveRequest = async (req, res, next) => {
  try {
    const { date, reason } = req.body;
    if (!date || !reason) {
      return res.status(400).json({ message: 'date and reason are required' });
    }

    const leave = await LeaveRequest.create({
      studentId: req.user._id,
      date: new Date(date),
      reason,
      status: 'pending'
    });

    res.status(201).json({ message: 'Leave request submitted', leaveId: leave._id });
  } catch (error) {
    next(error);
  }
};

const getMyLeaveRequests = async (req, res, next) => {
  try {
    const requests = await LeaveRequest.find({ studentId: req.user._id }).sort({ createdAt: -1 });
    res.json({ requests });
  } catch (error) {
    next(error);
  }
};

module.exports = { getMyAttendance, submitLeaveRequest, getMyLeaveRequests };
