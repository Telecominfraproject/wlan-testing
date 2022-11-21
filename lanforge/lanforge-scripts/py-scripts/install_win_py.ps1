# Before you can run this script, start with:
#
# 	Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy UnRestricted
#
#
# You want to install Chocolatey as Administrator, so 
# Right-click on your Posh icon, Run as Administrator
# then .\setup_lanforge_python.ps1
#

# set this if you need set -e behavior
# $ErrorActionPreference = "Stop"

# $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
# $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

#Requires -RunAsAdministrator
Set-ExecutionPolicy -Scope CurrentUser UnRestricted

$testchoco = powershell choco -v
# & $testchoco
if ($lastexitcode -ne 0){
    Write-Output "Seems Chocolatey is not installed, installing now"
    Set-ExecutionPolicy Bypass -Scope Process -Force
	[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
	Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
	choco upgrade chocolatey
	Write-Output "Re-run this script now that Chocolatey is installed."
	exit
}
else{
    Write-Output "Chocolatey Version $testchoco is already installed"
}

# choco install microsoft-windows-terminal
# refreshenv
choco install git.install
RefreshEnv.cmd
$env:PATH += ";C:\Program Files\Git\bin"
$testgit = powershell git --version
if ($lastexitcode -ne 0){
	Write-Output "git was not installed or is not in your path, bye."
	exit 1
}

choco install -y python3
RefreshEnv.cmd
$env:PATH += ";C:\Python311\"
$testpy = powershell C:\Python311\python -V
if ($lastexitcode -ne 0){
	Write-Output "git was not installed or is not in your path, bye."
	exit 1
}
Write-Output "Upgrading pip..."
C:\Python311\python -m pip install --upgrade pip

Invoke-WebRequest -URI 'https://www.candelatech.com/download/setup_win_py.ps1' -OutFile 'setup_lanforge_python2.ps1'

# At this point we do not want to be Administrator anymore.
# we should exit with a message to start the next user-level stage
Write-Output "This ends the Administrator level requirements."
Write-Output "Next: close all your powershell windows"
Write-Output "Open a new powershell window and run setup_win_py.ps1 script as a user."
exit 0

