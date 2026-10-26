@rem setlocal

:: 1. Generate a locale-independent timestamp (YYYYMMDD_HHMMSS)
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set timestamp=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%_%datetime:~8,2%%datetime:~10,2%%datetime:~12,2%

:: 2. Set Paths
set PATH="C:\Program Files\Rhino 8\System";%PATH%
cd "C:\dev\structural-analysis\Parcial3\T6 T7 T8 Ejercicios ok\"

:: 3. Run Rhino with the timestamped output file
start "" "C:\Program Files\Rhino 8\System\Rhino.exe"  -_Open "C:\dev\structural-analysis\Parcial3\T6 T7 T8 Ejercicios ok\T_Section_Diagram.3dm"  _ReadOnly=_Yes -_SetDisplayMode _Viewport=_Active _Mode=_Rendered -_-ViewCaptureToFile "C:\dev\structural-analysis\Parcial3\T6 T7 T8 Ejercicios ok\T_Section_Diagram_%timestamp%.png" _Width=1920 _Height=1080 _Enter -_Exit

echo PATH=%PATH%
@rem endlocal
