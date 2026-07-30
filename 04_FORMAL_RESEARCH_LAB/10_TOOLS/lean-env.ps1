param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string] $Program,
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $Arguments
)

$ErrorActionPreference = 'Stop'

$gitMingw = if ($env:TAMESIS_GIT_MINGW_BIN) { $env:TAMESIS_GIT_MINGW_BIN } else { 'C:\Program Files\Git\mingw64\bin' }
$gitUsr = if ($env:TAMESIS_GIT_USR_BIN) { $env:TAMESIS_GIT_USR_BIN } else { 'C:\Program Files\Git\usr\bin' }
$toolchainBin = if ($env:TAMESIS_LEAN_TOOLCHAIN_BIN) { $env:TAMESIS_LEAN_TOOLCHAIN_BIN } else { Join-Path $env:USERPROFILE '.elan\toolchains\leanprover--lean4---v4.32.2\bin' }
$elanShim = if ($env:TAMESIS_ELAN_SHIM_BIN) { $env:TAMESIS_ELAN_SHIM_BIN } else { Join-Path $env:USERPROFILE 'scoop\apps\elan\current\.elan\bin' }
$cacheDir = if ($env:MATHLIB_CACHE_DIR) { $env:MATHLIB_CACHE_DIR } else { Join-Path $env:USERPROFILE '.cache\mathlib' }

$required = @(
  (Join-Path $gitMingw 'curl.exe'),
  (Join-Path $gitUsr 'uname.exe'),
  (Join-Path $gitUsr 'chmod.exe'),
  (Join-Path $toolchainBin 'lean.exe'),
  (Join-Path $toolchainBin 'lake.exe'),
  (Join-Path $toolchainBin 'leantar.exe'),
  (Join-Path $elanShim 'elan.exe')
)
foreach ($path in $required) {
  if (-not (Test-Path -LiteralPath $path)) { throw "Required executable not found: $path" }
}

$selectedCurl = Join-Path $gitMingw 'curl.exe'
$curlVersion = (& $selectedCurl --version | Select-Object -First 1)
if ($curlVersion -match 'curl 7\.55\.1') { throw "Unsupported curl selected: $curlVersion" }

New-Item -ItemType Directory -Force -Path $cacheDir | Out-Null
$cacheCurl = Join-Path $cacheDir 'curl-7.88.1'
if (-not (Test-Path -LiteralPath $cacheCurl) -or
    (Get-FileHash $cacheCurl -Algorithm SHA256).Hash -ne (Get-FileHash $selectedCurl -Algorithm SHA256).Hash) {
  Copy-Item -LiteralPath $selectedCurl -Destination $cacheCurl -Force
}

$env:PATH = "$gitMingw;$gitUsr;$toolchainBin;$elanShim;$env:PATH"
Write-Host "curl: $curlVersion"
Write-Host "lean: $(& (Join-Path $toolchainBin 'lean.exe') --version)"
Write-Host "lake: $(& (Join-Path $toolchainBin 'lake.exe') --version)"
Write-Host "cache curl: $cacheCurl"

$executable = switch ($Program.ToLowerInvariant()) {
  'lean' { Join-Path $toolchainBin 'lean.exe' }
  'lake' { Join-Path $toolchainBin 'lake.exe' }
  'elan' { Join-Path $elanShim 'elan.exe' }
  default { $program }
}

& $executable @Arguments
exit $LASTEXITCODE
