# PowerShell Safe Patterns for Chinese Paths

Use these patterns directly.

## Enumerate files

```powershell
Get-ChildItem -LiteralPath 'D:\数据\项目A' -Recurse -File
```

## Read text

```powershell
Get-Content -LiteralPath 'D:\数据\项目A\说明.txt' -Encoding utf8
```

## Write text

```powershell
Set-Content -LiteralPath 'D:\数据\项目A\结果\summary.txt' -Value $text -Encoding utf8
```

## Search text

```powershell
Get-ChildItem -LiteralPath 'D:\数据\项目A' -Recurse -File |
  Select-String -Pattern '发病率'
```

## Never do this for Chinese-heavy workloads

- Do not use wildcard-based destructive path composition.
- Do not rely on implicit default encoding.
- Do not ignore decode exceptions.

