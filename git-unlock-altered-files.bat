@echo off
echo "Unlocking constants.py"
git update-index --no-skip-worktree .\constants.py
echo "Unlocking gallery-dl.conf"
git update-index --no-skip-worktree .\gallery-dl.conf
echo "Unlocking last-run.txt"
git update-index --no-skip-worktree .\last-run.txt
echo "Unlocking logs.txt"
git update-index --no-skip-worktree .\logs.txt
echo "Unlocking text_handlers.py"
git update-index --no-skip-worktree .\text_handlers.py
echo "Done. Files cleared to commit"