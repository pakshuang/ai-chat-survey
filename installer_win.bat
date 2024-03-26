@echo off
setlocal
rem You should already be here in ai-chat-survey
rem updates files
echo Getting updates...
git pull origin main

rem sample.env has to be updated. This will override openai api keys stored previously.
echo Setting up variables...
cp sample.env .env
:ask
set /p "response=Do you wish to set an OpenAI API key (Strongly recommended)? (Y/N): "
if /i "%response%" == "N" goto docker
if /i "%response%" == "Y" goto loop
echo Invalid response.
goto ask

:loop
set /p "openaiapi=What is your OpenAI API key? "
:asktwo
set /p "response=Do you wish to confirm? (Y/N): "
if /i "%response%" == "N" goto loop
if /i "%response%" == "Y" goto save
echo Invalid response
goto asktwo
:save
rem Add a new line to .env
echo OPENAI_API_KEY=%openaiapi% >> .env
echo API key set!

rem Build docker image.
echo Running docker compose...
:docker
docker-compose build

:run
set /p "response=Docker built! Run the container? (Y/N): " 
if /i "%response%" == "N" goto end
if /i "%response%" == "Y" (
    docker-compose up 
    goto exit
)
echo Invalid Response.
goto run
:end
echo Installation complete!
endlocal
pause