// PM2 configuration for managing both Python apps
// File: ecosystem.config.js

module.exports = {
  apps: [
    {
      name: 'face-recognition-api',
      script: 'python',
      args: 'main.py',
      cwd: '/path/to/face-recognition-app',
      interpreter: 'none',
      env: {
        PORT: 5000,
        NODE_ENV: 'production'
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    },
    {
      name: 'nfc-contact-app',
      script: 'python',
      args: 'main.py',
      cwd: '/path/to/nfc-contact-app',
      interpreter: 'none',
      env: {
        PORT: 5002,
        NODE_ENV: 'production'
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    }
  ]
};