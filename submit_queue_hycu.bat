@echo OFF

rem Force l'utilisation West European Latin
chcp 1252 > nul

rem Inclut le repertoire binaire powershell dans le path
set PATH_PYTHON=C:\Users\Jdoe\AppData\Local\Programs\Python\Python311\
set PATH=%PATH_PYTHON%;%PATH%

call submit_aff.bat %*
echo _______________________________________________________________________
echo Debut de l'execution ...
date /T
echo %time:~+0,8%
echo _______________________________________________________________________

rem Mode TEST
if "%TOM_JOB_EXEC%" == "TEST" (
	echo Job execute en mode TEST
	%ABM_BIN%\tsend -sT -r0 -m"Traitement termine (mode TEST)"
	%ABM_BIN%\vtgestlog
	goto FIN
)

echo.

rem :LAUNCH
echo %PATH_PYTHON%\python %ABM_BIN%\vtom-hycu_backup-jobs.py --backup-name %1 --url %2 --auth-token %3 --auth-file %4 --check-interval %5 --timeout %6 --backup-config %7 --no-monitor %8 --verbose %9
%PATH_PYTHON%\python %ABM_BIN%\vtom-hycu_backup-jobs.py --backup-name %1 --url %2 --auth-token %3 --auth-file %4 --check-interval %5 --timeout %6 --backup-config %7 --no-monitor %8 --verbose %9
set RETCODE=%ERRORLEVEL%
if %RETCODE% equ 0 goto TERMINE
goto ERREUR

:ERREUR
%ABM_BIN%\tsend -sE -r%RETCODE% -m"Traitement en erreur (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo Fin d'execution
date /T
echo %time:~+0,8%
echo Exit [%RETCODE%] donc pas d'acquittement
echo _______________________________________________________________________
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:TERMINE
%ABM_BIN%\tsend -sT -r%RETCODE% -m"Traitement termine (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo Fin d'execution
date /T
echo %time:~+0,8%
echo Exit [%RETCODE%] donc acquittement
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:FIN
