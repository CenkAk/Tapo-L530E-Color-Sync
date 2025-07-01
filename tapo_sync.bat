@echo off
chcp 65001 >nul
echo Tapo L530E Renk Senkronizasyonu Baslatiliyor...
set /p monitor_index="Hangi monitoru secmek istersiniz? (1, 2, vb.): "
python ".\tapo_screen_sync.py" %monitor_index%
pause