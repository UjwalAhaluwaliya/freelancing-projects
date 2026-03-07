const express = require('express');
const {
  getNotifications,
  createNotifications,
  markAsRead
} = require('../controllers/notificationController');
const { protect, authorize } = require('../middleware/authMiddleware');

const router = express.Router();

router.get('/', protect, getNotifications);
router.post('/', protect, authorize('admin', 'faculty'), createNotifications);
router.patch('/:id/read', protect, markAsRead);

module.exports = router;
