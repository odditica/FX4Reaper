cd monoctrl

$found = "$(find . -type f)"

$found = $found.Split(" ")

Foreach ($f in $found) {
    echo "$f"
    
    $reaperPath = "$env:APPDATA\REAPER\Effects\blokatt\monoctrl"
    $reaperFilePath = "$reaperPath\\$f"
    Try
    {
        $repoDate = (Get-Item "$f").LastWriteTime
        $reaperDate = (Get-Item "$reaperFilePath").LastWriteTime
    }
    Catch
    {
        continue;
    }
    if ("$repoDate" -gt "$reaperDate") {
        echo "Newer in repo, copying."
        cp "$f" "$reaperPath"
    } elseif ("$repoDate" -lt "$reaperDate") {
        echo "Newer in Reaper, copying."
        cp "$reaperFilePath" .
    }

}
#cp -r monoctrl $env:APPDATA\REAPER\Effects\blokatt\

cd ..