const express = require('express');
const {
  createStudent,
  createFaculty,
  createClass,
  createSubject,
  getClasses,
  getFacultyList,
  getOverviewReport,
  sendAnnouncement
} = require('../controllers/adminController');
const { protect, authorize } = require('../middleware/authMiddleware');

const router = express.Router();

router.use(protect, authorize('admin'));

router.post('/students', createStudent);
router.post('/faculty', createFaculty);
router.post('/classes', createClass);
router.post('/subjects', createSubject);
router.get('/classes', getClasses);
router.get('/faculty/list', getFacultyList);
router.get('/reports/overview', getOverviewReport);
router.post('/announcements', sendAnnouncement);

module.exports = router;
