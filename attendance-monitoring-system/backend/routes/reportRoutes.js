const express = require('express');
const { exportAttendance } = require('../controllers/reportController');
const { protect, authorize } = require('../middleware/authMiddleware');

const router = express.Router();

router.get('/attendance/export', protect, authorize('admin', 'faculty'), exportAttendance);

module.exports = router;
