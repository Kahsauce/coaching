const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const PORT = process.env.PORT || 3000;

function serveFile(filePath, res) {
  fs.readFile(path.join(__dirname, filePath), (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    const ext = path.extname(filePath);
    const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' }[ext] || 'text/plain';
    res.writeHead(200, { 'Content-Type': mime });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url.startsWith('/api/metrics')) {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    const date = url.searchParams.get('date') || new Date().toISOString().slice(0,10);
    const child = spawn('python', ['src/sport_plan.py', 'metrics', date]);
    let output = '';
    child.stdout.on('data', d => output += d);
    child.stderr.on('data', d => output += d);
    child.on('close', () => {
      const lines = output.trim().split('\n');
      const metrics = {};
      lines.forEach(l => {
        const parts = l.split(':');
        if (parts.length === 2) {
          metrics[parts[0].trim()] = parseFloat(parts[1]) || parts[1].trim();
        }
      });
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(metrics));
    });
  } else {
    const filePath = req.url === '/' ? '/index.html' : req.url;
    serveFile(filePath, res);
  }
});

server.listen(PORT, () => {
  console.log(`Serveur lancé sur http://localhost:${PORT}`);
});
