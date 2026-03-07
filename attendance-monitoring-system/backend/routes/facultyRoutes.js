const express = require('express');
const {
  getAssignedClasses,
  getStudentsByClass,
  markAttendance,
  updateAttendance,
  getClassAttendance,
  getLeaveRequests,
  updateLeaveRequestStatus
} = require('../controllers/facultyController');
const { protect, authorize } = require('../middleware/authMiddleware');

const router = express.Router();

router.use(protect, authorize('faculty'));

router.get('/classes', getAssignedClasses);
router.get('/classes/:classId/students', getStudentsByClass);
router.post('/attendance', markAttendance);
router.put('/attendance/update', updateAttendance);
router.get('/attendance/class', getClassAttendance);
router.get('/leave-requests', getLeaveRequests);
router.put('/leave-requests/status', updateLeaveRequestStatus);

module.exports = router;
