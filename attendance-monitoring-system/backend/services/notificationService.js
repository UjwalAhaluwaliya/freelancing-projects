const Notification = require('../models/Notification');

const createNotification = async ({ userId, message, type = 'system' }) => {
  return Notification.create({ userId, message, type });
};

module.exports = { createNotification };
