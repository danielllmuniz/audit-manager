require('dotenv').config();

module.exports = {
  secret: process.env.JWT_SECRET || 'audit-manager-secret-key-2025',
  expiresIn: process.env.JWT_EXPIRES_IN || '24h'
};
