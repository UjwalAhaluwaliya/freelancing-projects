const mongoose = require('mongoose');

const subjectSchema = new mongoose.Schema(
  {
    subjectName: { type: String, required: true, trim: true },
    classId: { type: mongoose.Schema.Types.ObjectId, ref: 'Class', required: true },
    facultyId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true }
  },
  { timestamps: true }
);

subjectSchema.index({ subjectName: 1, classId: 1 }, { unique: true });

module.exports = mongoose.model('Subject', subjectSchema);
