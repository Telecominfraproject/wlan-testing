# setup_win_py.ps1
# Use this script after the install_win_py.ps1 script has been done twice
Set-ExecutionPolicy -Scope CurrentUser Unrestricted
$ErrorActionPreference = "Stop"
Set-Location "$Home\Documents"
if (-not(test-path "$Home\Documents\lanforge-scripts")) {
	Write-Output "LF  Cloning github.com/greearb/lanforge-scripts ...."
	git clone 'https://github.com/greearb/lanforge-scripts'
}

if (-not(test-path "$Home\Documents\venv_lanforge\Scripts\Activate.ps1")) {
	# mkdir venv_lanforge
   Write-Output "LF  Creating virtual environment..."
	pip install virtualenv
	Write-Output "LF  Cloning github.com/greearb/lanforge-scripts ...."
	python -m venv venv_lanforge

	if ($lastexitcode -ne 0) {
		Write-Output "Problems creating python virtual environment, bye."
		exit 1
	}
}
if (-not(test-path "$Home\Documents\venv_lanforge\Scripts\Activate.ps1")) {
	Write-Output "No virtual python environment to activate, bye."
	exit 1
}
.\venv_lanforge\Scripts\Activate.ps1
Write-Output "LF  Upgrading pip and setup tools...."
python -m pip install --upgrade pip
Write-Output "LF  Upgrading wheel...."
pip install --upgrade wheel
Write-Output "LF  Upgrading setup tools...."
pip install --upgrade setuptools

Write-Output "LF  Deactivating virtual environment..."
deactivate
RefreshEnv
Write-Output "LF  Activating virtual environment..."
.\venv_lanforge\Scripts\Activate.ps1
Write-Output "LF  Updating py-scripts dependencies..."
Set-Location "$Home\Documents\lanforge-scripts\py-scripts"
python .\update_dependencies.py

#