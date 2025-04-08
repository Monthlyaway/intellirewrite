@echo off
echo Cleaning chapter rewriter data...

REM Check if tasks.json exists and delete it
if exist tasks.json (
    echo Deleting tasks.json...
    del /f /q tasks.json
)

REM Check if chapter_data folder exists and delete it
if exist chapter_data (
    echo Deleting chapter_data folder...
    rmdir /s /q chapter_data
)

echo Cleanup complete!
echo.
echo All task files and chapter data have been removed.
echo You can now start fresh with new tasks.
echo.
pause 