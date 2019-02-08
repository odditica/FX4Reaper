@echo off
SET name=MonoCtrl
xcopy "%~dp0%name%" "%appdata%\REAPER\Effects\blokatt\%name%\" /s /i /Y && (
  echo Successfully installed %name% to:
  echo %appdata%\REAPER\Effects\blokatt\%name%\
) || (
  echo Could not install %name% to:
  echo %appdata%\REAPER\Effects\blokatt\%name%\
)