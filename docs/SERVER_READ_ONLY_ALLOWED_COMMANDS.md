# Server Read-Only Allowed Commands

Date: 2026-06-17 | NOT executed — description only

| Command | Purpose | Restrictions |
|---------|---------|-------------|
| `pwd` | Current directory | Safe |
| `ls -la` | File listing | Only in known paths |
| `find . -maxdepth 2 -type f` | Limited file search | No secrets paths |
| `tree -L 2` | Directory tree | If installed, no content |
| `head -5 file.py` | File header | Only whitelist files |
| `grep -l pattern *.py` | Filename search | By filename, not content |
| `cat file.py` | Read file | Only whitelist, no secrets |

## Forbidden Even as Read-Only

| Command | Reason |
|---------|--------|
| `cat .env` | Secrets |
| `grep token *` | Token search |
| `python -m compileall` | Execution, not read-only |
| `pytest` | Execution |
| `systemctl` | Service control |
| `git add/commit/push` | Write operations |
| `patch` | Write operations |
| `sed -i` | In-place edit |
