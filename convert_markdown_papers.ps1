$root = (Get-Location).Path

$markdownFiles = Get-ChildItem -Recurse -File -Filter *.md |
    Where-Object {
        $_.FullName -notmatch '\\.git\\' -and
        $_.FullName -notmatch '\\.lake\\' -and
        $_.FullName -notmatch '\\04_FORMAL_RESEARCH_LAB\\' -and
        $_.FullName -notmatch '\\publicar\\|\\publicados\\'
    }

$includePattern = '(?i)(^|[_\-\s])(paper|article|treatise|thesis|preprint|manuscript|essay)([_\-\s\.]|$)'
$excludePattern = '(?i)(readme|roadmap|status|report|index|guide|master|result|summary|checklist|audit|log|session|task|structure|documentation|metadata|catalog|chronogram|protocol|verification|analysis|analise|attack|gun-|legacy|state|license|changelog|epistemic|references|source)'

$candidates = @($markdownFiles | Where-Object {
    ($_.Name -match $includePattern -or $_.DirectoryName -match '(?i)(PAPERS|TREATISES|ARTICLES|PREPRINTS)') -and
    $_.Name -notmatch $excludePattern
})

$errors = @()
$converted = @()

foreach ($source in $candidates) {
    $target = [IO.Path]::ChangeExtension($source.FullName, '.html')
    if (Test-Path -LiteralPath $target) {
        $stem = [IO.Path]::GetFileNameWithoutExtension($source.Name)
        $target = Join-Path $source.DirectoryName ($stem + '_from_md.html')
    }

    $temporary = [IO.Path]::GetTempFileName()
    try {
        & npx --yes marked -i $source.FullName -o $temporary --gfm --breaks 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "marked exited with code $LASTEXITCODE"
        }

        $markdown = [IO.File]::ReadAllText($source.FullName)
        $heading = [regex]::Match($markdown, '(?m)^\s*#\s+(.+?)\s*$')
        if ($heading.Success) {
            $title = $heading.Groups[1].Value.Trim()
        } else {
            $title = [IO.Path]::GetFileNameWithoutExtension($source.Name) -replace '[_\-]+', ' '
        }
        $title = ($title -replace '[*_`~]', '') -replace '\s+', ' '
        $titleTag = if ($title.Length -gt 50) { $title.Substring(0, 50) + '...' } else { $title }

        $body = [IO.File]::ReadAllText($temporary)
        $body = [regex]::Replace($body, '^\s*<h1>.*?</h1>\s*', '', [Text.RegularExpressions.RegexOptions]::Singleline)
        $body = [regex]::Replace($body, '\s+align="[^"]*"', '')
        $body = [regex]::Replace($body, '&(?!#\d+;|#x[0-9A-Fa-f]+;|[A-Za-z][A-Za-z0-9]+;)', '&amp;')

        $relativeDirectory = $target.Substring($root.Length)
        $relativeDirectory = [IO.Path]::GetDirectoryName($relativeDirectory).Trim('\')
        if ([string]::IsNullOrEmpty($relativeDirectory)) {
            $depth = 0
        } else {
            $depth = ($relativeDirectory -split '\\').Count
        }
        $stylesheet = ('../' * $depth) + 'paper-layout.css'

        $titleEscaped = [Net.WebUtility]::HtmlEncode($title)
        $sourceEscaped = [Net.WebUtility]::HtmlEncode($source.Name)
        $document = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>$([Net.WebUtility]::HtmlEncode($titleTag))</title>
  <meta name="description" content="Artigo convertido do arquivo Markdown Tamesis: $sourceEscaped">
  <link rel="stylesheet" href="$stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {delimiters: [{left: '`$`$', right: '`$`$', display: true}, {left: '`$', right: '`$', display: false}]});"></script>
</head>
<body>
  <header>
    <h1>$titleEscaped</h1>
    <div class="authors">Tamesis Research Archive</div>
    <div class="date">Automatic Markdown conversion - source file: $sourceEscaped</div>
  </header>
  <main><article>
$body
  </article></main>
</body>
</html>
"@
        [IO.File]::WriteAllText($target, $document, (New-Object Text.UTF8Encoding($false)))
        $converted += [pscustomobject]@{ Source = $source.FullName; Target = $target }
    } catch {
        $errors += ($source.FullName + ' :: ' + $_.Exception.Message)
    } finally {
        Remove-Item -LiteralPath $temporary -Force -ErrorAction SilentlyContinue
    }
}

"CANDIDATES=$($candidates.Count) CONVERTED=$($converted.Count) ERRORS=$($errors.Count)"
$errors
