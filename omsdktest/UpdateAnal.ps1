$output = @{}
$fields = @()
Get-ChildItem -Path C:\Users\vaideeswaran_ganesan\Work\omdata\SDKRepo\1* | ForEach-Object -Process {
    $a = $_.FullName
    $k = [xml](Get-Content ${a}\_master\Catalog.xml | out-string)
    foreach ($i in $k.Manifest.SoftwareComponent) {
        if ($output.ContainsKey($i.path) -eq $False)
        {
            $output[$i.path] = @{
                'Revision' = $i.RevisionHistory.InnerText
                'Attributes' = ""
                'Others' = ""
            }
            if ($i.RevisionHistory -eq $null -or $i.RevisionHistory.InnerText -eq $null) {
                continue
            }
            $fields += $i.RevisionHistory.InnerText.Split()
            $attrs = @()
            $others = @()
            if ($i.RevisionHistory.InnerText -match 'CVE-([^-]+)-([^\s]+)') {
                $output[$i.path]['Vulnerability'] = $Matches[0]
                $attrs += "[1]Vulnerability"
            }
            if ($i.RevisionHistory.InnerText -match 'loss|crash|unavailable|inoperable|failure|[Aa]ssert|hang|recovery') {
                $attrs += "[2]Availability"
            }
            if ($i.RevisionHistory.InnerText -match 'Improved[-\s]security|Security') {
                $attrs += "[2]Security"
            }
            if ($i.RevisionHistory.InnerText -match 'wrong|[rR]eliability|accuracy|[Cc]orrupt') {
                $attrs += "[3]Reliability"
            }
            if ($i.RevisionHistory.InnerText -match '[Pp]erformance|latency|degradation|excessive') {
                $attrs += "[3]Performance"
            }
            if ($i.RevisionHistory.InnerText -match '[Cc]ompliance') {
                $others += "[4]Compliance"
            }
            if ($i.RevisionHistory.InnerText -match '(Added|Add|adds|Improved) support') {
                $others += "[4]Support"
            }
            if ($i.RevisionHistory.InnerText -match '[Ee]nhance|[Oo]ptimize' -and $attrs.Length -eq 0) {
                $others += "[9]Enhancements"
            }
            if ($i.RevisionHistory.InnerText -match '[Dd]iagnostics') {
                $others += "[9]Diagnostics"
            }
            if ($i.RevisionHistory.InnerText -match '[Cc]orrect') {
                $others += "[9]Accuracy"
            }
            $output[$i.path]['Attributes'] = $attrs -join ','
            $output[$i.path]['Others'] = $others -join ','
        }
    }
}

$json = $output | ConvertTo-Json
Out-File -FilePath C:\Users\vaideeswaran_ganesan\Work\omdata\SDKRepo\T.Json -InputObject $json -Encoding ascii 
Out-File -FilePath C:\Users\vaideeswaran_ganesan\Work\omdata\F.txt -InputObject $fields
