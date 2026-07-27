param(
    [string]$TargetPath = 'C:\Users\user\Desktop\malyarka_codex_work'
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $TargetPath)) {
    [pscustomobject]@{
        TargetPath = $TargetPath
        Exists = $false
        Method = 'RestartManager'
        Processes = @()
        Error = 'Target path does not exist'
    } | ConvertTo-Json -Depth 5
    exit 0
}

$source = @"
using System;
using System.Runtime.InteropServices;

public static class RestartManagerNative
{
    public const int RmRebootReasonNone = 0;

    [StructLayout(LayoutKind.Sequential)]
    public struct RM_UNIQUE_PROCESS
    {
        public int dwProcessId;
        public System.Runtime.InteropServices.ComTypes.FILETIME ProcessStartTime;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct RM_PROCESS_INFO
    {
        public RM_UNIQUE_PROCESS Process;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)]
        public string strAppName;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 64)]
        public string strServiceShortName;
        public int ApplicationType;
        public uint AppStatus;
        public uint TSSessionId;
        [MarshalAs(UnmanagedType.Bool)]
        public bool bRestartable;
    }

    [DllImport("rstrtmgr.dll", CharSet = CharSet.Unicode)]
    public static extern int RmStartSession(out uint pSessionHandle, int dwSessionFlags, string strSessionKey);

    [DllImport("rstrtmgr.dll", CharSet = CharSet.Unicode)]
    public static extern int RmRegisterResources(uint pSessionHandle, uint nFiles, string[] rgsFilenames, uint nApplications, IntPtr rgApplications, uint nServices, string[] rgsServiceNames);

    [DllImport("rstrtmgr.dll")]
    public static extern int RmGetList(uint dwSessionHandle, out uint pnProcInfoNeeded, ref uint pnProcInfo, [In, Out] RM_PROCESS_INFO[] rgAffectedApps, ref uint lpdwRebootReasons);

    [DllImport("rstrtmgr.dll")]
    public static extern int RmEndSession(uint pSessionHandle);
}
"@

if (-not ('RestartManagerNative' -as [type])) {
    Add-Type -TypeDefinition $source
}

$session = 0
$sessionKey = [guid]::NewGuid().ToString()
$processes = @()
$errorText = $null

try {
    $startResult = [RestartManagerNative]::RmStartSession([ref]$session, 0, $sessionKey)
    if ($startResult -ne 0) {
        throw "RmStartSession failed with code $startResult"
    }

    $resources = @($TargetPath)
    $registerResult = [RestartManagerNative]::RmRegisterResources($session, [uint32]$resources.Count, $resources, 0, [IntPtr]::Zero, 0, $null)
    if ($registerResult -ne 0) {
        throw "RmRegisterResources failed with code $registerResult"
    }

    $needed = 0
    $count = 0
    $rebootReasons = 0
    $firstResult = [RestartManagerNative]::RmGetList($session, [ref]$needed, [ref]$count, $null, [ref]$rebootReasons)

    if ($firstResult -eq 234 -and $needed -gt 0) {
        $count = $needed
        $info = New-Object RestartManagerNative+RM_PROCESS_INFO[] $count
        $secondResult = [RestartManagerNative]::RmGetList($session, [ref]$needed, [ref]$count, $info, [ref]$rebootReasons)
        if ($secondResult -ne 0) {
            throw "RmGetList failed with code $secondResult"
        }

        for ($i = 0; $i -lt $count; $i++) {
            $pid = $info[$i].Process.dwProcessId
            $cim = Get-CimInstance Win32_Process -Filter "ProcessId = $pid" -ErrorAction SilentlyContinue
            $processes += [pscustomobject]@{
                Name = $info[$i].strAppName
                PID = $pid
                ExecutablePath = if ($cim) { $cim.ExecutablePath } else { $null }
                CommandLine = if ($cim) { $cim.CommandLine } else { $null }
                ApplicationType = $info[$i].ApplicationType
                AppStatus = $info[$i].AppStatus
                Restartable = $info[$i].bRestartable
            }
        }
    } elseif ($firstResult -eq 0) {
        $processes = @()
    } else {
        throw "RmGetList failed with code $firstResult"
    }
} catch {
    $errorText = $_.Exception.Message
} finally {
    if ($session -ne 0) {
        [void][RestartManagerNative]::RmEndSession($session)
    }
}

[pscustomobject]@{
    TargetPath = $TargetPath
    Exists = $true
    Method = 'RestartManager'
    Processes = $processes
    Error = $errorText
} | ConvertTo-Json -Depth 6
