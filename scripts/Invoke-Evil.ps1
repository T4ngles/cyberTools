function Invoke-Evil
{
	Write-Host 'foobared'
    $rawcode = "Write-Host 'foobared2'"
    $code = "V3JpdGUtSG9zdCAnZm9vYmFyZWQyJwo="
    $newcode = [System.Text.Encoding]::ASCII.GetString(
        [Convert]::FromBase64String($code))

    Invoke-Expression $newcode

    $rawcode2 = "Write-Host 'foobared2'"
    $rawcode2Bytes = [System.Text.Encoding]::ASCII.GetBytes($rawcode2)
    Write-Host "rawbytes: " $rawcode2Bytes
    $xorKey = 123
    $obfuscatedrawcode2Bytes = foreach($byte in $rawcode2Bytes) { $byte -bxor $xorKey }

    $obfuscatedrawcode2String = [System.Convert]::ToBase64String($obfuscatedrawcode2Bytes)
    Write-Host "string of xor'd bytes: " $obfuscatedrawcode2String
    $code2 = $obfuscatedrawcode2String
    $bytes = [Convert]::FromBase64String($code2)
    $newbytes = foreach($byte in $bytes) { $byte -bxor $xorKey }

    $newcode2 = [System.Text.Encoding]::ASCII.GetString($newBytes)

    Invoke-Expression $newcode2

    Start-Sleep -s 5
}
Invoke-Evil