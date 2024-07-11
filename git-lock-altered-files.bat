@echo off
echo "Locking constants.py"
git update-index --skip-worktree .\constants.py
echo "Locking gallery-dl.conf"
git update-index --skip-worktree .\gallery-dl.conf
echo "Locking last-run.txt"
git update-index --skip-worktree .\last-run.txt
echo "Locking logs.txt"
git update-index --skip-worktree .\logs.txt
echo "Locking text_handlers.py"
git update-index --skip-worktree .\text_handlers.py
echo "Done. Further edits will be ignored"