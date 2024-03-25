@echo off
rem You should already be here in ai-chat-survey
setlocal
git pull origin main

set "envFile=.env"
if not exist "%envFile%" (
    echo Setting up variables.
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

    echo OPENAI_API_KEY=%openaiapi% >> .env
)

:docker
docker-compose up --build
echo Press any key to continue.
pause