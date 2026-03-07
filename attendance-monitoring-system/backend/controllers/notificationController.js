const Notification = require('../models/Notification');
const User = require('../models/User');
const { createNotification } = require('../services/notificationService');

const getNotifications = async (req, res, next) => {
  try {
    const notifications = await Notification.find({ userId: req.user._id }).sort({ createdAt: -1 });
    res.json({ notifications });
  } catch (error) {
    next(error);
  }
};

const createNotifications = async (req, res, next) => {
  try {
    const { userId, role, message, type } = req.body;
    if (!message) return res.status(400).json({ message: 'message is required' });

    if (userId) {
      await createNotification({ userId, message, type: type || 'system' });
      return res.status(201).json({ message: 'Notification sent' });
    }

    if (role) {
      const users = await User.find({ role }).select('_id');
      await Promise.all(users.map((u) => createNotification({ userId: u._id, message, type: type || 'system' })));
      return res.status(201).json({ message: `Notification sent to ${users.length} ${role} users` });
    }

    return res.status(400).json({ message: 'Provide userId or role' });
  } catch (error) {
    next(error);
  }
};

const markAsRead = async (req, res, next) => {
  try {
    const { id } = req.params;
    const notification = await Notification.findOneAndUpdate(
      { _id: id, userId: req.user._id },
      { read: true },
      { new: true }
    );

    if (!notification) return res.status(404).json({ message: 'Notification not found' });

    res.json({ message: 'Notification marked as read' });
  } catch (error) {
    next(error);
  }
};

module.exports = { getNotifications, createNotifications, markAsRead };
