$fname = 'C:\Users\vaideeswaran_ganesan\Work\omdata\MsgReg\iDRAC_MsgReg_14G_RTSPlus_2019Q1.xml'
$registry_db = 'C:\Users\vaideeswaran_ganesan\Work\omdata\MsgRegistry.csv'


function Analyze
{
    param($message)

    if ($message -match '(lower|upper)\s+(warning|critical)\s+threshold')
    {
        return ($Matches[1], $Matches[2], "Threshold")
    }
    if ($message -match '(below|above)\s+the\s+normal+threshold')
    {
        return ($Matches[1], $Matches[2], "Threshold")
    }
    if ($message -match 'inside range')
    {
        return ($Matches[1], 'Normal', "Threshold")
    }
    if ($message -match 'outside of range')
    {
        return ($Matches[1], 'critical', "Threshold")
    }
    return "None"
}
$reg = [xml](Get-Content $fname | Out-String)
$regjs = New-Object -TypeName System.Collections.ArrayList
foreach ($entry in $reg.REGISTRY.REGISTRY_ENTRIES.MESSAGE)
{
    $js = New-Object psobject
    $js | Add-Member -Type NoteProperty -Name "Name" -Value  $entry.NAME
    $js | Add-Member -Type NoteProperty -Name "Prefix" -Value  $entry.MESSAGE_ID.PREFIX
    $js | Add-Member -Type NoteProperty -Name "Sequence" -Value  $entry.MESSAGE_ID.SEQUENCE_NUMBER
    $js | Add-Member -Type NoteProperty -Name "Description" -Value  $entry.MESSAGE_DESCRIPTION
    $js | Add-Member -Type NoteProperty -Name "Severity" -Value  $entry.FIXED_MESSAGE_INSTANCE_VALUES.PERCEIVED_SEVERITY.DESCRIPTION
    $js | Add-Member -Type NoteProperty -Name "Action" -Value  $entry.FIXED_MESSAGE_INSTANCE_VALUES.RECOMMENDED_ACTION.DESCRIPTION
    $message = @()
    foreach ($k in $entry.MESSAGE_COMPONENTS.ChildNodes) 
    {
        if ($k.LocalName -eq 'STATIC_ELEMENT')
        {
            $message += $k.InnerText
        }
        elseif ($k.LocalName -eq 'DYNAMIC_ELEMENT')
        {
            $message += ('${' + ($k.SOURCE_PROPERTY -replace '\s+','-') + '}')
        }
    }
    $js | Add-Member -Type NoteProperty -Name "Message" -Value ($message -join '')
    $c = $regjs.Add($js)
}
$regjs | ConvertTo-Csv -NoTypeInformation | Out-File -FilePath $registry_db -Encoding ascii

