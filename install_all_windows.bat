@echo off
for /r %%A in (*.bat) do if /i "%%~nA"=="install_windows" (	
	call "%%A"		
	echo =====================	
)
echo All done.
:End
pause