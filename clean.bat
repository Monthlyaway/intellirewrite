@echo off
echo Cleaning rewriter data..., make sure the OUTPUT_DIR is `output`, or you need to manually modify this clearning script

REM Check if tasks.json exists and delete it
if exist tasks.json (
    echo Deleting tasks.json...
    del /f /q tasks.json
)

REM Check if output folder exists and delete it
if exist output (
    echo Deleting output folder...
    rmdir /s /q output
)

echo Cleanup complete!
echo.
echo All task files and chapter data have been removed.
echo You can now start fresh with new tasks.
echo.
pause 