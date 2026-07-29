$root = (Get-Location).Path
$publishedRoot = Join-Path $root 'publicados'
$toPublishRoot = Join-Path $root 'publicar'

$canonicalPublished = @(
    '90_LEGACY/06_TOE_ARCHITECTURE_OF_REALITY/01_Treatises/paper.html',
    'RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_01_P_VS_NP/05_PROOFS/paper.html',
    'RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_02_RIEMANN/04_PAPERS/paper.html',
    'RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_03_NAVIER_STOKES/04_PAPERS/paper.html',
    'RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_04_YANG_MILLS/04_PAPERS/paper.html',
    'RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_05_HODGE_CONJECTURE/05_PROOFS/paper.html',
    'RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_06_BIRCH_SWINNERTON_DYER/04_PAPERS/paper.html'
)

$publishedSet = @{}
foreach ($relative in $canonicalPublished) {
    $full = [IO.Path]::GetFullPath((Join-Path $root ($relative -replace '/', '\')))
    if (-not (Test-Path -LiteralPath $full)) {
        throw "Published canonical file not found: $relative"
    }
    $publishedSet[$full.ToLowerInvariant()] = $true
}

$htmlFiles = Get-ChildItem -Recurse -File -Filter *.html |
    Where-Object {
        $_.FullName -notmatch '\\.git\\' -and
        $_.FullName -notmatch '\\.lake\\' -and
        $_.FullName -notmatch '\\publicar\\|\\publicados\\'
    }

$articleFiles = @()
foreach ($file in $htmlFiles) {
    $content = [IO.File]::ReadAllText($file.FullName)
    $isArticle =
        ($file.Name -match '(?i)(paper|article|treatise|thesis|preprint|manuscript|essay|proof|theorem)') -or
        ($file.DirectoryName -match '(?i)(PAPERS|TREATISES|PROOFS|ARTICLES|PREPRINTS)') -or
        $content.Contains('class="content-wrapper"') -or
        $content.Contains('<article>')
    if ($isArticle) { $articleFiles += $file }
}

foreach ($folder in @($publishedRoot, $toPublishRoot)) {
    [IO.Directory]::CreateDirectory($folder) | Out-Null
    [IO.File]::Copy((Join-Path $root 'paper-layout.css'), (Join-Path $folder 'paper-layout.css'), $true)
}

function Copy-StagedFile($source, $destinationRoot) {
    $relative = $source.FullName.Substring($root.Length).TrimStart('\')
    $destination = Join-Path $destinationRoot $relative
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($destination)) | Out-Null
    [IO.File]::Copy($source.FullName, $destination, $true)
}

$publishedFiles = @()
$toPublishFiles = @()
foreach ($file in $articleFiles) {
    if ($publishedSet.ContainsKey($file.FullName.ToLowerInvariant())) {
        Copy-StagedFile $file $publishedRoot
        $publishedFiles += $file
    } else {
        Copy-StagedFile $file $toPublishRoot
        $toPublishFiles += $file
    }
}

"ARTICLE_HTML=$($articleFiles.Count) PUBLISHED=$($publishedFiles.Count) TO_PUBLISH=$($toPublishFiles.Count)"
