const express = require('express');
const { getMyAttendance, submitLeaveRequest, getMyLeaveRequests } = require('../controllers/studentController');
const { protect, authorize } = require('../middleware/authMiddleware');

const router = express.Router();

router.use(protect, authorize('student'));

router.get('/attendance/me', getMyAttendance);
router.post('/leave-request', submitLeaveRequest);
router.get('/leave-requests/me', getMyLeaveRequests);

module.exports = router;
