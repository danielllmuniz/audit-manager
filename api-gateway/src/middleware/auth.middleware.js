const jwt = require('jsonwebtoken');
const jwtConfig = require('../config/jwt.config');

const authMiddleware = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    return res.status(401).json({
      errors: [{
        title: 'Unauthorized',
        detail: 'No authorization token provided'
      }]
    });
  }

  const parts = authHeader.split(' ');

  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    return res.status(401).json({
      errors: [{
        title: 'Unauthorized',
        detail: 'Token format invalid. Use: Bearer <token>'
      }]
    });
  }

  const token = parts[1];

  try {
    const decoded = jwt.verify(token, jwtConfig.secret);

    req.user = decoded;
    req.headers['x-user-role'] = decoded.role;
    req.headers['x-user-email'] = decoded.email;

    next();
  } catch (error) {
    return res.status(401).json({
      errors: [{
        title: 'Unauthorized',
        detail: 'Invalid or expired token'
      }]
    });
  }
};

module.exports = authMiddleware;
