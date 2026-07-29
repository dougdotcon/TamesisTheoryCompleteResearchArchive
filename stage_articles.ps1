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
$manifest = @()
foreach ($file in $articleFiles) {
    $relative = $file.FullName.Substring($root.Length).TrimStart('\')
    $titleMatch = [regex]::Match([IO.File]::ReadAllText($file.FullName), '<title[^>]*>(.*?)</title>', [Text.RegularExpressions.RegexOptions]::Singleline)
    $title = if ($titleMatch.Success) { [regex]::Replace($titleMatch.Groups[1].Value, '\s+', ' ').Trim() } else { $file.BaseName }
    $isPublished = $publishedSet.ContainsKey($file.FullName.ToLowerInvariant())
    $isConverted = Select-String -LiteralPath $file.FullName -Pattern 'Artigo convertido do arquivo Markdown Tamesis' -SimpleMatch -Quiet
    $markdownSource = ''
    if ($isConverted) {
        $stem = [IO.Path]::GetFileNameWithoutExtension($file.Name) -replace '_from_md$', ''
        $candidateSource = Join-Path $file.DirectoryName ($stem + '.md')
        if (Test-Path -LiteralPath $candidateSource) {
            $markdownSource = $candidateSource.Substring($root.Length).TrimStart('\')
        }
    }
    if ($publishedSet.ContainsKey($file.FullName.ToLowerInvariant())) {
        Copy-StagedFile $file $publishedRoot
        $publishedFiles += $file
    } else {
        Copy-StagedFile $file $toPublishRoot
        $toPublishFiles += $file
    }
    $manifest += [pscustomobject]@{
        status = if ($isPublished) { 'published' } else { 'to_publish' }
        kind = if ($isConverted) { 'markdown_converted' } else { 'html_existing' }
        title = $title
        source_path = $relative
        markdown_source = $markdownSource
        staged_path = if ($isPublished) { 'publicados/' + ($relative -replace '\\', '/') } else { 'publicar/' + ($relative -replace '\\', '/') }
    }
}

$manifestText = (($manifest | Sort-Object status, source_path | ConvertTo-Csv -NoTypeInformation) -join [Environment]::NewLine)
[IO.File]::WriteAllText((Join-Path $root 'ARTICLE_MANIFEST.csv'), $manifestText, (New-Object Text.UTF8Encoding($false)))

"ARTICLE_HTML=$($articleFiles.Count) PUBLISHED=$($publishedFiles.Count) TO_PUBLISH=$($toPublishFiles.Count)"
