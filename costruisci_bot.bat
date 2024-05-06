@echo off
set /p botName=Nome del bot: 

echo caricamento... 10%%
docker stop %botName% > nul 2>&1
docker rm %botName% > nul 2>&1
docker rmi %botName%-img > nul 2>&1
echo caricamento... 30%%
docker build -t %botName%-img . > nul 2>&1
echo caricamento... 80%%
docker run --name %botName% -e TZ=Europe/Rome --restart always -v .:/app -d %botName%-img > nul 2>&1
echo caricamento... 100%%
echo bot %botName% costruito con successo!