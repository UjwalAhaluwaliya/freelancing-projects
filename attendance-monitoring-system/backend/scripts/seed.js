require('dotenv').config();
const mongoose = require('mongoose');
const connectDB = require('../config/db');
const User = require('../models/User');
const ClassModel = require('../models/Class');
const Subject = require('../models/Subject');
const Attendance = require('../models/Attendance');
const Notification = require('../models/Notification');

const seed = async () => {
  await connectDB();

  await Promise.all([
    User.deleteMany({}),
    ClassModel.deleteMany({}),
    Subject.deleteMany({}),
    Attendance.deleteMany({}),
    Notification.deleteMany({})
  ]);

  const [admin, faculty] = await User.create([
    {
      name: 'System Admin',
      email: 'admin@college.edu',
      password: 'admin123',
      role: 'admin',
      department: 'Administration'
    },
    {
      name: 'Dr. Meera Sharma',
      email: 'faculty@college.edu',
      password: 'faculty123',
      role: 'faculty',
      department: 'Computer Science'
    }
  ]);

  const cls = await ClassModel.create({
    className: 'B.Tech CSE A',
    semester: 6,
    department: 'Computer Science'
  });

  const [student1, student2] = await User.create([
    {
      name: 'Rahul Verma',
      email: 'student1@college.edu',
      password: 'student123',
      role: 'student',
      department: 'Computer Science',
      classId: cls._id
    },
    {
      name: 'Neha Singh',
      email: 'student2@college.edu',
      password: 'student123',
      role: 'student',
      department: 'Computer Science',
      classId: cls._id
    }
  ]);

  const subject = await Subject.create({
    subjectName: 'Database Management Systems',
    classId: cls._id,
    facultyId: faculty._id
  });

  await Attendance.create([
    {
      studentId: student1._id,
      subjectId: subject._id,
      classId: cls._id,
      date: new Date('2026-03-01'),
      status: 'present',
      markedBy: faculty._id
    },
    {
      studentId: student2._id,
      subjectId: subject._id,
      classId: cls._id,
      date: new Date('2026-03-01'),
      status: 'absent',
      markedBy: faculty._id
    }
  ]);

  await Notification.create({
    userId: student2._id,
    message: 'Low attendance alert: please attend upcoming classes regularly.',
    type: 'alert'
  });

  console.log('Seed complete');
  console.log('Admin:', admin.email, '/ admin123');
  console.log('Faculty:', faculty.email, '/ faculty123');
  console.log('Student:', student1.email, '/ student123');

  await mongoose.connection.close();
};

seed().catch(async (error) => {
  console.error(error);
  await mongoose.connection.close();
  process.exit(1);
});
