const express = require('express');
const jwt = require('jsonwebtoken');
const jwtConfig = require('../config/jwt.config');
const fakeUsers = require('../data/users');

const router = express.Router();

router.post('/login/dev', (req, res) => {
  const user = fakeUsers.dev;

  const token = jwt.sign(
    {
      id: user.id,
      email: user.email,
      role: user.role,
      name: user.name
    },
    jwtConfig.secret,
    { expiresIn: jwtConfig.expiresIn }
  );

  return res.json({
    data: {
      type: 'auth',
      attributes: {
        token,
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role
        }
      }
    }
  });
});

router.post('/login/approver', (req, res) => {
  const user = fakeUsers.approver;

  const token = jwt.sign(
    {
      id: user.id,
      email: user.email,
      role: user.role,
      name: user.name
    },
    jwtConfig.secret,
    { expiresIn: jwtConfig.expiresIn }
  );

  return res.json({
    data: {
      type: 'auth',
      attributes: {
        token,
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role
        }
      }
    }
  });
});

router.post('/login/devops', (req, res) => {
  const user = fakeUsers.devops;

  const token = jwt.sign(
    {
      id: user.id,
      email: user.email,
      role: user.role,
      name: user.name
    },
    jwtConfig.secret,
    { expiresIn: jwtConfig.expiresIn }
  );

  return res.json({
    data: {
      type: 'auth',
      attributes: {
        token,
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role
        }
      }
    }
  });
});

module.exports = router;
