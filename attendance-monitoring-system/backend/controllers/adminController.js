const User = require('../models/User');
const mongoose = require('mongoose');
const ClassModel = require('../models/Class');
const Subject = require('../models/Subject');
const Attendance = require('../models/Attendance');
const Notification = require('../models/Notification');
const { createNotification } = require('../services/notificationService');

const createStudent = async (req, res, next) => {
  try {
    const { name, email, password, department, classId } = req.body;
    const existing = await User.findOne({ email });
    if (existing) return res.status(409).json({ message: 'Email already exists' });

    const user = await User.create({ name, email, password, department, classId, role: 'student' });
    res.status(201).json({ message: 'Student created', userId: user._id });
  } catch (error) {
    next(error);
  }
};

const createFaculty = async (req, res, next) => {
  try {
    const { name, email, password, department } = req.body;
    const existing = await User.findOne({ email });
    if (existing) return res.status(409).json({ message: 'Email already exists' });

    const user = await User.create({ name, email, password, department, role: 'faculty' });
    res.status(201).json({ message: 'Faculty created', userId: user._id });
  } catch (error) {
    next(error);
  }
};

const createClass = async (req, res, next) => {
  try {
    const cls = await ClassModel.create(req.body);
    res.status(201).json({ message: 'Class created', classId: cls._id });
  } catch (error) {
    next(error);
  }
};

const createSubject = async (req, res, next) => {
  try {
    const { facultyId, classId, subjectName } = req.body;

    if (!subjectName || !facultyId || !classId) {
      return res.status(400).json({ message: 'subjectName, facultyId and classId are required' });
    }

    if (!mongoose.Types.ObjectId.isValid(facultyId) || !mongoose.Types.ObjectId.isValid(classId)) {
      return res.status(400).json({ message: 'Invalid facultyId or classId' });
    }

    const faculty = await User.findOne({ _id: facultyId, role: 'faculty' });
    if (!faculty) return res.status(400).json({ message: 'Invalid facultyId' });

    const classExists = await ClassModel.exists({ _id: classId });
    if (!classExists) return res.status(400).json({ message: 'Invalid classId' });

    const subject = await Subject.create(req.body);
    res.status(201).json({ message: 'Subject created', subjectId: subject._id });
  } catch (error) {
    next(error);
  }
};

const getClasses = async (req, res, next) => {
  try {
    const classes = await ClassModel.find({}).sort({ createdAt: -1 });
    res.json({ classes });
  } catch (error) {
    next(error);
  }
};

const getFacultyList = async (req, res, next) => {
  try {
    const faculty = await User.find({ role: 'faculty' }).select('_id name email department').sort({ createdAt: -1 });
    res.json({ faculty });
  } catch (error) {
    next(error);
  }
};

const getOverviewReport = async (req, res, next) => {
  try {
    const [totalStudents, totalFaculty, totalClasses, totalSubjects] = await Promise.all([
      User.countDocuments({ role: 'student' }),
      User.countDocuments({ role: 'faculty' }),
      ClassModel.countDocuments(),
      Subject.countDocuments()
    ]);

    const attendanceAgg = await Attendance.aggregate([
      {
        $group: {
          _id: '$studentId',
          present: {
            $sum: {
              $cond: [{ $eq: ['$status', 'present'] }, 1, 0]
            }
          },
          total: { $sum: 1 }
        }
      },
      {
        $project: {
          percentage: {
            $cond: [{ $eq: ['$total', 0] }, 0, { $multiply: [{ $divide: ['$present', '$total'] }, 100] }]
          }
        }
      },
      {
        $group: {
          _id: null,
          avgAttendance: { $avg: '$percentage' },
          lowAttendanceCount: {
            $sum: {
              $cond: [{ $lt: ['$percentage', 75] }, 1, 0]
            }
          }
        }
      }
    ]);

    const stats = attendanceAgg[0] || { avgAttendance: 0, lowAttendanceCount: 0 };

    res.json({
      totals: { totalStudents, totalFaculty, totalClasses, totalSubjects },
      analytics: {
        averageAttendancePercentage: Number((stats.avgAttendance || 0).toFixed(2)),
        lowAttendanceStudents: stats.lowAttendanceCount || 0
      }
    });
  } catch (error) {
    next(error);
  }
};

const sendAnnouncement = async (req, res, next) => {
  try {
    const { message, recipients = 'all' } = req.body;
    if (!message) return res.status(400).json({ message: 'Message is required' });

    const filter = recipients === 'all' ? {} : { role: recipients };
    const users = await User.find(filter).select('_id');

    await Promise.all(
      users.map((user) =>
        createNotification({ userId: user._id, message, type: 'announcement' })
      )
    );

    res.status(201).json({ message: `Announcement sent to ${users.length} users` });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  createStudent,
  createFaculty,
  createClass,
  createSubject,
  getClasses,
  getFacultyList,
  getOverviewReport,
  sendAnnouncement
};
