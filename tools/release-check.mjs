import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {combineMiddleware} from '../server/middleware.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const git = args => execFileSync('git', args, {cwd: root, windowsHide: true, maxBuffer: 32 * 1024 * 1024});
const files = git(['ls-files', '-z']).toString().split('\0').filter(Boolean);
const issues = [];
const sha = data => createHash('sha256').update(data).digest('hex');
for (const entry of git(['ls-files', '--stage', '-z']).toString().split('\0')) {
  if (entry.startsWith('120000 ')) issues.push(entry.split('\t')[1] + ': symlink refused');
}
for (const file of files) {
  const absolute = path.join(root, file);
  if (fs.lstatSync(absolute).isSymbolicLink()) issues.push(file + ': symlink refused');
  if (/(^|\/)(\.runtime|node_modules|dist|__pycache__)(\/|$)|(^|\/)(plugins\.json|auth\.json|config\.toml|\.env(?:\..*)?)$|\.(?:db|bak|log|previous|tgz)$/i.test(file)) {
    issues.push(file + ': private/generated path');
    continue;
  }
  if (!/\.(?:cjs|mjs|js|json|md|html|svg|css|ps1|bat|py|ya?ml)$/.test(file)) continue;
  const text = fs.readFileSync(absolute, 'utf8');
  if (/[A-Z]:[\\/](?:Users[\\/](?:Administrator|ADMINI~1)|AI[\\/]ChatGPT)/i.test(text)) issues.push(file + ': personal path');
  if (/(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)/.test(text)) issues.push(file + ': possible credential (value suppressed)');
}
const provenance = JSON.parse(fs.readFileSync(path.join(root, 'vendor/modeltrace/PROVENANCE.json')));
for (const [name, info] of Object.entries(provenance.files)) {
  const file = 'vendor/modeltrace/' + name;
  if (sha(fs.readFileSync(path.join(root, file))) !== info.sha256 || sha(git(['show', ':' + file])) !== info.sha256) issues.push(file + ': provenance mismatch');
}
const history = JSON.parse(fs.readFileSync(path.join(root, 'history/PROVENANCE.json')));
for (const file of ['codex-history.middleware.js', 'history/codex-history.middleware.js']) {
  if (sha(fs.readFileSync(path.join(root, file))) !== history.sha256 || sha(git(['show', ':' + file])) !== history.sha256) issues.push(file + ': history changed');
}
const generated = fs.readFileSync(path.join(root, 'workbench.middleware.js'), 'utf8');
if (generated !== combineMiddleware()) issues.push('workbench.middleware.js: must rebuild the public entry without private holds');
for (const required of ['README.md', 'MAINTAINING.md', 'LICENSE', 'plugin/index.mjs', 'server/http.mjs', 'web/index.html', 'history/page/index.html', 'docs/images/native-filter.png', 'docs/images/monitor-light.png', 'docs/images/monitor-dark.png', 'docs/images/monitor-settings.png', 'docs/images/history.png']) {
  if (!files.includes(required)) issues.push(required + ': not staged/tracked');
}
if (issues.length) { console.error(issues.join('\n')); process.exitCode = 1; }
else console.log(JSON.stringify({passed: true, publicFiles: files.length, history: 'unchanged', modelTrace: 'verified', middleware: 'no private holds', note: 'Heuristic scan supplements manual review.'}));
