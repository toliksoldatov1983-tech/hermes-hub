param(
    [string]$Root = "E:\Hermes-Hub"
)

$ErrorActionPreference = "Stop"

$bundlePath = Join-Path $Root "handoff\CHATGPT_CONTEXT_BUNDLE.md"

$sourceFiles = @(
    "HERMES_HUB_STATE.md",
    "progress\PROGRESS_CARD.md",
    "tasks\NEXT_TASKS.md",
    "decisions\DECISIONS.md",
    "PROJECT_HINTS.md",
    "SAFETY_RULES.md",
    "docs\CHATGPT_CHAT_ROLES.md",
    "docs\BATCH_WORKFLOW.md",
    "docs\MALYARKA_CLEAN_CORE_CONTRACTS.md",
    "docs\MALYARKA_CLEAN_PARSER_RULES.md",
    "docs\MALYARKA_CLEAN_AREA_RULES.md",
    "docs\MALYARKA_CLEAN_ORDER_RESULT_RULES.md",
    "docs\MALYARKA_CLEAN_COREL_MODEL_RULES.md",
    "docs\MALYARKA_CLEAN_COREL_IMPLEMENTATION_PLAN.md",
    "docs\MALYARKA_CLEAN_PIPELINE_SMOKE_TEST_PLAN.md",
    "docs\MALYARKA_CLEAN_USAGE_GUIDE_PLAN.md",
    "docs\MALYARKA_CLEAN_MANUAL_CORE_CHECK_PLAN.md",
    "docs\MALYARKA_CLEAN_EMPTY_INVALID_STATUS_FIX_PLAN.md",
    "docs\MALYARKA_CLEAN_USER_ENTRY_PLAN.md",
    "docs\MALYARKA_CLEAN_SIMPLE_RUN_PLAN.md",
    "docs\MALYARKA_CLEAN_SIMPLE_USER_ORDER_INPUT_PLAN.md",
    "handoff\BATCH_PACKET_TEMPLATE.md"
)

function Add-SourceFile {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$RelativePath
    )

    $path = Join-Path $Root $RelativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing source file: $path"
    }

    $content = Get-Content -LiteralPath $path -Encoding UTF8

    $Lines.Add("")
    $Lines.Add("---")
    $Lines.Add("")
    $Lines.Add("## Source: $RelativePath")
    $Lines.Add("")
    $Lines.Add("~~~markdown")
    foreach ($line in $content) {
        $Lines.Add($line)
    }
    $Lines.Add("~~~")
}

$generatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$lines = [System.Collections.Generic.List[string]]::new()

$lines.Add("# ChatGPT Context Bundle")
$lines.Add("")
$lines.Add("Generated: $generatedAt")
$lines.Add("")
$lines.Add("Generator:")
$lines.Add("")
$lines.Add("~~~text")
$lines.Add("E:\Hermes-Hub\tools\Update-ChatGPTContextBundle.ps1")
$lines.Add("~~~")
$lines.Add("")
$lines.Add("Use this file when ChatGPT cannot see local disk files.")
$lines.Add("")
$lines.Add("This is a generated portable snapshot, not the main source of truth.")
$lines.Add("")
$lines.Add("Main source of truth:")
$lines.Add("")
$lines.Add("~~~text")
$lines.Add("E:\Hermes-Hub\HERMES_HUB_STATE.md")
$lines.Add("~~~")
$lines.Add("")
$lines.Add("How ChatGPT should use this:")
$lines.Add("")
$lines.Add("1. Read this bundle as the current project context.")
$lines.Add("2. Answer in Russian and simple words.")
$lines.Add("3. Show a short progress card regularly.")
$lines.Add("4. Prepare BATCH_PACKET for Codex instead of many small tasks.")
$lines.Add("5. Do not ask the user to remember hidden context.")
$lines.Add("6. If disk state is uncertain, ask Codex to verify files.")
$lines.Add("")
$lines.Add("Important:")
$lines.Add("")
$lines.Add("~~~text")
$lines.Add("Old Malyarka is archive-only.")
$lines.Add("Do not touch .env, orders.db, .git, tokens, keys, Telegram, Vision or APIs without separate permission.")
$lines.Add("~~~")

foreach ($file in $sourceFiles) {
    Add-SourceFile -Lines $lines -RelativePath $file
}

$russianNavigationFiles = Get-ChildItem -LiteralPath $Root -File -Filter "*.md" |
    Where-Object { $_.Name -match "[^\x00-\x7F]" } |
    Sort-Object Name

foreach ($file in $russianNavigationFiles) {
    Add-SourceFile -Lines $lines -RelativePath $file.Name
}

$bundle = $lines -join "`r`n"

$secretPatterns = @(
    "sk-[A-Za-z0-9_-]{20,}",
    "xoxb-[A-Za-z0-9_-]{20,}",
    "bot[0-9]{6,}:[A-Za-z0-9_-]{20,}",
    "(?i)api_key\s*=",
    "(?i)token\s*=",
    "(?i)password\s*=",
    "BEGIN .*PRIVATE KEY"
)

foreach ($pattern in $secretPatterns) {
    if ($bundle -match $pattern) {
        throw "Secret-like content detected. Bundle was not written. Pattern: $pattern"
    }
}

Set-Content -LiteralPath $bundlePath -Value $bundle -Encoding UTF8

Write-Output "Updated: $bundlePath"
