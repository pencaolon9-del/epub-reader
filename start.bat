@echo off
cd /d "g:\学习文件\小说"
start /b C:\tool\python.exe -m http.server 8080
timeout 2 >nul
start http://localhost:8080/reader-with-book.html
pause
