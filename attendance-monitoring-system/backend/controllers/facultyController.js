const Attendance = require('../models/Attendance');
const Subject = require('../models/Subject');
const User = require('../models/User');
const LeaveRequest = require('../models/LeaveRequest');
const { createNotification } = require('../services/notificationService');

const calculatePercentage = async (studentId, subjectId) => {
  const rows = await Attendance.find({ studentId, subjectId });
  if (!rows.length) return 0;
  const present = rows.filter((item) => item.status === 'present').length;
  return (present / rows.length) * 100;
};

const getAssignedClasses = async (req, res, next) => {
  try {
    const subjects = await Subject.find({ facultyId: req.user._id }).populate('classId');
    res.json({ subjects });
  } catch (error) {
    next(error);
  }
};

const getStudentsByClass = async (req, res, next) => {
  try {
    const { classId } = req.params;
    const hasAccess = await Subject.exists({ facultyId: req.user._id, classId });

    if (!hasAccess) {
      return res.status(403).json({ message: 'No access to this class' });
    }

    const students = await User.find({ role: 'student', classId }).select('_id name email');
    res.json({ students });
  } catch (error) {
    next(error);
  }
};

const markAttendance = async (req, res, next) => {
  try {
    const { classId, subjectId, date, records } = req.body;

    if (!classId || !subjectId || !date || !Array.isArray(records) || !records.length) {
      return res.status(400).json({ message: 'classId, subjectId, date, records are required' });
    }

    const subject = await Subject.findOne({ _id: subjectId, facultyId: req.user._id, classId });
    if (!subject) {
      return res.status(403).json({ message: 'Subject is not assigned to this faculty for selected class' });
    }

    const attendanceDate = new Date(date);

    const existing = await Attendance.find({
      subjectId,
      classId,
      date: attendanceDate,
      studentId: { $in: records.map((r) => r.studentId) }
    });

    if (existing.length) {
      return res.status(409).json({ message: 'Attendance already exists for one or more students on this date' });
    }

    const payload = records.map((record) => ({
      studentId: record.studentId,
      subjectId,
      classId,
      date: attendanceDate,
      status: record.status,
      markedBy: req.user._id
    }));

    await Attendance.insertMany(payload);

    for (const record of records) {
      const pct = await calculatePercentage(record.studentId, subjectId);
      if (pct < 75) {
        await createNotification({
          userId: record.studentId,
          message: `Low attendance alert: ${pct.toFixed(1)}% in subject ${subject.subjectName}`,
          type: 'alert'
        });
      } else {
        await createNotification({
          userId: record.studentId,
          message: `Attendance updated for ${subject.subjectName}`,
          type: 'attendance'
        });
      }
    }

    res.status(201).json({ message: 'Attendance marked successfully' });
  } catch (error) {
    next(error);
  }
};

const updateAttendance = async (req, res, next) => {
  try {
    const { attendanceId, status } = req.body;
    if (!attendanceId || !status) {
      return res.status(400).json({ message: 'attendanceId and status are required' });
    }

    const row = await Attendance.findById(attendanceId).populate('subjectId');
    if (!row) return res.status(404).json({ message: 'Attendance record not found' });

    const subject = await Subject.findOne({ _id: row.subjectId._id, facultyId: req.user._id });
    if (!subject) return res.status(403).json({ message: 'Not allowed to edit this attendance' });

    row.status = status;
    await row.save();

    const pct = await calculatePercentage(row.studentId, row.subjectId._id);
    await createNotification({
      userId: row.studentId,
      message: `Attendance edited for ${row.subjectId.subjectName}. Current: ${pct.toFixed(1)}%`,
      type: 'attendance'
    });

    res.json({ message: 'Attendance updated' });
  } catch (error) {
    next(error);
  }
};

const getClassAttendance = async (req, res, next) => {
  try {
    const { classId, subjectId } = req.query;

    const subject = await Subject.findOne({ _id: subjectId, classId, facultyId: req.user._id });
    if (!subject) {
      return res.status(403).json({ message: 'No access to this class/subject report' });
    }

    const records = await Attendance.find({ classId, subjectId })
      .populate('studentId', 'name email')
      .sort({ date: -1 });

    res.json({ records });
  } catch (error) {
    next(error);
  }
};

const getLeaveRequests = async (req, res, next) => {
  try {
    const classIds = await Subject.find({ facultyId: req.user._id }).distinct('classId');
    const students = await User.find({ role: 'student', classId: { $in: classIds } }).select('_id');
    const studentIds = students.map((s) => s._id);

    const requests = await LeaveRequest.find({ studentId: { $in: studentIds } })
      .populate('studentId', 'name email classId')
      .sort({ createdAt: -1 });

    res.json({ requests });
  } catch (error) {
    next(error);
  }
};

const updateLeaveRequestStatus = async (req, res, next) => {
  try {
    const { leaveRequestId, status } = req.body;

    if (!leaveRequestId || !status) {
      return res.status(400).json({ message: 'leaveRequestId and status are required' });
    }

    if (!['approved', 'rejected'].includes(status)) {
      return res.status(400).json({ message: 'Status must be approved or rejected' });
    }

    const leaveRequest = await LeaveRequest.findById(leaveRequestId).populate('studentId', 'name classId');
    if (!leaveRequest) {
      return res.status(404).json({ message: 'Leave request not found' });
    }

    const hasAccess = await Subject.exists({
      facultyId: req.user._id,
      classId: leaveRequest.studentId?.classId
    });

    if (!hasAccess) {
      return res.status(403).json({ message: 'Not allowed to approve/reject this leave request' });
    }

    leaveRequest.status = status;
    await leaveRequest.save();

    await createNotification({
      userId: leaveRequest.studentId._id,
      message: `Your leave request for ${leaveRequest.date.toISOString().slice(0, 10)} was ${status}.`,
      type: 'system'
    });

    res.json({ message: `Leave request ${status}` });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getAssignedClasses,
  getStudentsByClass,
  markAttendance,
  updateAttendance,
  getClassAttendance,
  getLeaveRequests,
  updateLeaveRequestStatus
};
