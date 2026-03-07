const mongoose = require('mongoose');

const classSchema = new mongoose.Schema(
  {
    className: { type: String, required: true, trim: true },
    semester: { type: Number, required: true, min: 1, max: 12 },
    department: { type: String, required: true, trim: true }
  },
  { timestamps: true }
);

classSchema.index({ className: 1, semester: 1, department: 1 }, { unique: true });

module.exports = mongoose.model('Class', classSchema);
