"""Package npm's explicit public allowlist, never the installed plugin directory."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import subprocess
import tarfile
import zipfile

root = Path(__file__).resolve().parent.parent
subprocess.run(['node', 'tools/release-check.mjs'], cwd=root, check=True)
output = root / 'dist'
output.mkdir(exist_ok=True)
npm = 'npm.cmd' if os.name == 'nt' else 'npm'
result = subprocess.check_output([npm, 'pack', '--json', '--pack-destination', str(output)], cwd=root)
# npm lifecycle output may precede the final JSON. The archive name is fixed by metadata.
pkg = json.loads((root / 'package.json').read_text(encoding='utf-8'))
archive = output / (pkg['name'] + '-' + pkg['version'] + '.tgz')
name = 'magpie-codex-workbench-v' + pkg['version']
zipped = output / (name + '.zip')
with tarfile.open(archive, 'r:gz') as source, zipfile.ZipFile(zipped, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as target:
    for item in source.getmembers():
        parts = PurePosixPath(item.name).parts
        if not item.isfile() or parts[0] != 'package' or '..' in parts or any(p in ('.runtime', 'node_modules', 'dist') for p in parts):
            raise RuntimeError('Unexpected archive member: ' + item.name)
        target.writestr(name + '/' + '/'.join(parts[1:]), source.extractfile(item).read())
subprocess.run(['node', 'tools/release-check.mjs'], cwd=root, check=True)
sums = ''.join(hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + f.name + '\n' for f in (archive, zipped))
(output / 'SHA256SUMS.txt').write_text(sums, encoding='utf-8')
print(sums)
