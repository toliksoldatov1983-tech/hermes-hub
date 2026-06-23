param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$OutDir = (Join-Path $ProjectRoot "dist")
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$package = Join-Path $OutDir "malyarka-runtime-clean_$stamp.zip"

$excludeDirs = @(
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dist"
)
$excludeFiles = @(
    ".env",
    "orders.db",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.lock"
)

$files = Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File -Force | Where-Object {
    $relative = $_.FullName.Substring($ProjectRoot.Length).TrimStart("\")
    $parts = $relative -split "[\\/]"
    foreach ($dir in $excludeDirs) {
        if ($parts -contains $dir) { return $false }
    }
    foreach ($pattern in $excludeFiles) {
        if ($_.Name -like $pattern) { return $false }
    }
    return $true
}

if ($files.Count -eq 0) {
    throw "No files selected for package."
}

$temp = Join-Path ([System.IO.Path]::GetTempPath()) "malyarka_runtime_package_$stamp"
$manifest = Join-Path $temp "manifest.txt"
if (Test-Path -LiteralPath $temp) {
    Remove-Item -LiteralPath $temp -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $temp | Out-Null

try {
    $files | ForEach-Object { $_.FullName } | Set-Content -LiteralPath $manifest -Encoding UTF8

    if (Test-Path -LiteralPath $package) {
        Remove-Item -LiteralPath $package -Force
    }

    $pythonCode = @'
import pathlib
import sys
import zipfile

project_root = pathlib.Path(sys.argv[1]).resolve()
manifest = pathlib.Path(sys.argv[2]).resolve()
package = pathlib.Path(sys.argv[3]).resolve()

with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for raw in manifest.read_text(encoding="utf-8-sig").splitlines():
        path = pathlib.Path(raw).resolve()
        rel = path.relative_to(project_root).as_posix()
        zf.write(path, rel)
'@
    $pythonCode | python - $ProjectRoot $manifest $package
}
finally {
    if (Test-Path -LiteralPath $temp) {
        Remove-Item -LiteralPath $temp -Recurse -Force
    }
}

[pscustomobject]@{
    Package = $package
    Files = $files.Count
    SizeKB = [math]::Round((Get-Item -LiteralPath $package).Length / 1KB, 1)
}
