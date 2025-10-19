require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');
const authRoutes = require('./routes/auth.routes');
const authMiddleware = require('./middleware/auth.middleware');

const app = express();
const PORT = process.env.PORT || 3000;
const APPLICATION_SERVICE_URL = process.env.APPLICATION_SERVICE_URL || 'http://localhost:5000';

app.use(cors());

app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

const apiRouter = express.Router();

apiRouter.use('/auth', express.json(), authRoutes);

apiRouter.use('/', authMiddleware, createProxyMiddleware({
  target: `${APPLICATION_SERVICE_URL}`,
  changeOrigin: true,
  onProxyReq: (proxyReq, req, res) => {
    console.log(`Proxying ${req.method} ${req.url} to ${APPLICATION_SERVICE_URL}${req.url}`);

    if (req.headers['x-user-role']) {
      proxyReq.setHeader('X-User-Role', req.headers['x-user-role']);
    }
    if (req.headers['x-user-email']) {
      proxyReq.setHeader('X-User-Email', req.headers['x-user-email']);
    }
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`Received response from backend: ${proxyRes.statusCode}`);
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.status(500).json({
      errors: [{
        title: 'Proxy Error',
        detail: err.message
      }]
    });
  },
  logLevel: 'debug'
}));

app.use('/api/v1', apiRouter);

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'audit-manager-api-gateway',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
  console.log(`Proxying requests to: ${APPLICATION_SERVICE_URL}`);
});

module.exports = app;
