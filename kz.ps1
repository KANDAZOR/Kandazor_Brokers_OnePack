param([string]$Cmd="help",[string]$Cfg="configs\cluster.yaml")
$ErrorActionPreference = "Stop"
function Run-Sim { 
  .\.venv\Scripts\Activate.ps1
  $env:PYTHONPATH = "$PWD\src"
  python src\engine\pipeline.py --config $Cfg
}
function Report-Latest {
  .\.venv\Scripts\Activate.ps1
  $env:PYTHONPATH = "$PWD\src"
  python src\tools\report_latest.py
}
function CSV-Validate([string[]]$Paths){
  .\.venv\Scripts\Activate.ps1
  $env:PYTHONPATH = "$PWD\src"
  foreach($p in $Paths){ python src\tools\csv_validate.py $p }
}
switch ($Cmd.ToLower()) {
  "run" { Run-Sim }
  "report" { Report-Latest }
  "csv-validate" { CSV-Validate @($Args) }
  default { Write-Host "Comandos: run | report | csv-validate <arquivos>" }
}
