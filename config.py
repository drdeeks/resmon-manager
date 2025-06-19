# Configuration for Resource Monitor Scanner

# Critical system processes that should NEVER be terminated
CRITICAL_PROCESSES = {
    'system', 'smss.exe', 'csrss.exe', 'wininit.exe', 'winlogon.exe',
    'services.exe', 'lsass.exe', 'svchost.exe', 'spoolsv.exe', 'explorer.exe',
    'dwm.exe', 'audiodg.exe', 'conhost.exe', 'dllhost.exe', 'msdtc.exe',
    'taskhost.exe', 'taskhostw.exe', 'registry', 'secure system', 'memory compression',
    'memcompression'
}

# Protected processes that are often important but may appear unnecessary
# These require administrator privileges or are protected by Windows
PROTECTED_PROCESSES = {
    # HP-related services
    'diagscap.exe', 'touchpointanalyticsclientservice.exe', 'sysinfocap.exe',
    'networkcap.exe', 'hpcommrecovery.exe', 'hpprintscandoctorservice.exe',
    'hpcc.bg.backgroundapp.exe',
    # Windows authentication and security
    'ngciso.exe', 'oneapp.igcc.winservice.exe',
    # Windows Update and telemetry
    'usoclient.exe', 'wuauclt.exe', 'waasmedicagent.exe',
    # Security and Antivirus processes
    'msmpseng.exe', 'mpdefendercoreservice.exe', 'antimalware service executable',
    'mbamservice.exe', 'malwarebytes.exe', 'mc-fw-host.exe',
    # Other protected services
    'backgroundtaskhost.exe', 'runtimebroker.exe'
}

# Critical Windows services that should not be stopped
CRITICAL_SERVICES = {
    'eventlog', 'rpcss', 'dcomlaunch', 'cryptsvc', 'bits', 'wuauserv',
    'themes', 'audiosrv', 'browser', 'dhcp', 'dnscache', 'eventlog',
    'lanmanserver', 'lanmanworkstation', 'netlogon', 'netman', 'nla',
    'policyagent', 'protectedstorage', 'rasauto', 'rasman', 'remoteregistry',
    'schedule', 'seclogon', 'sens', 'sharedaccess', 'shellhwdetection',
    'spooler', 'srservice', 'tapisrv', 'termservice', 'w32time',
    'winmgmt', 'wmi', 'wscsvc', 'wuauserv', 'xmlprov'
}

# Processes that are commonly unnecessary or resource-heavy
COMMON_UNNECESSARY_PROCESSES = {
    'iexplore.exe', 'chrome.exe', 'firefox.exe', 'opera.exe', 'msedge.exe',
    'notepad.exe', 'calc.exe', 'mspaint.exe', 'wordpad.exe'
}

# Services that are often unnecessary and can be safely stopped
UNNECESSARY_SERVICES = {
    'fax', 'messenger', 'netdde', 'netddedsdm', 'telnet', 'remoteaccess',
    'clipbook', 'alerter', 'browser'
}

# Memory threshold (MB) - processes using more than this are flagged as resource-heavy
MEMORY_THRESHOLD_MB = 500

# CPU threshold (%) - processes using more than this consistently are flagged
CPU_THRESHOLD_PERCENT = 80

# Time threshold (seconds) - how long a process should be inactive to be considered for termination
INACTIVE_TIME_THRESHOLD = 3600  # 1 hour

# Maximum number of duplicate processes allowed for the same executable
MAX_DUPLICATE_INSTANCES = 3

# Logging configuration
LOG_FILE = 'resource_monitor.log'
LOG_LEVEL = 'INFO'

# GUI Configuration
WINDOW_TITLE = "Resource Monitor Scanner"
WINDOW_SIZE = "800x600"
REFRESH_INTERVAL = 5000  # milliseconds 