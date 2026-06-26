Some files (like esbuild.exe and rollup.win32-x64-msvc.node) are locked, likely by a running process (e.g., a dev server, terminal, or editor).

To fix:

Close all terminals, editors, and processes using the project.
Open Task Manager (Ctrl+Shift+Esc) and end any Node.js or related processes.
Try again:
If it still fails:

Restart your computer to release all file locks, then run the commands above again.
After cleanup, reinstall dependencies:

This should resolve the permission issues and allow you to proceed.