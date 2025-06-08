import fs from 'fs';
import path from 'path';

const srcPath = path.resolve('../brigantes/static/index.html');
const destPath = path.resolve('../brigantes/templates/index.html');

// Read the file
let content = fs.readFileSync(srcPath, 'utf8');

// Replace paths
content = content
  .replace(/src="\.\//g, 'src="/static/')
  .replace(/href="\.\//g, 'href="/static/');

// Ensure destination folder exists
fs.mkdirSync(path.dirname(destPath), { recursive: true });

// Write modified file
fs.writeFileSync(destPath, content, 'utf8');

console.log(`✅ index.html patched and copied to ${destPath}`);
