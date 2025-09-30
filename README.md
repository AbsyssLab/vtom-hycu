# Integration HYCU with Visual TOM
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![en](https://img.shields.io/badge/lang-fr-green.svg)](README-fr.md)  
This project enables the integration of HYCU Backup with the Visual TOM scheduler.

The solution provides a Python script that can trigger and monitor HYCU backups through the HYCU API, with comprehensive monitoring and reporting capabilities.

The Python script `vtom-hycu_backup-jobs.py` is used together with its associated queue batch for Windows and Linux environments.

# Disclaimer
No Support and No Warranty are provided by Absyss SAS for this project and related material. The use of this project's files is at your own risk.
Absyss SAS assumes no liability for damage caused by the usage of any of the files offered here via this Github repository.
Consultings days can be requested to help for the implementation.

# Prerequisites

  * Visual TOM 7.1.2 or higher
  * Windows with PowerShell installed
  * Python 3.x or higher
  * HYCU API access with valid authentication token
  * Network connectivity to HYCU server

# Instructions

## HYCU Backup Integration

The script provides comprehensive HYCU backup management through the HYCU API. It supports the following actions:
  * Trigger backup jobs with custom configurations
  * Monitor backup execution status in real-time
  * Generate detailed execution reports
  * Multiple authentication methods (token, file, environment variables)
  * Configurable monitoring intervals and timeouts
  * Comprehensive error handling with specific exit codes

## Features

- **Backup Triggering**: Start HYCU backups with custom configurations
- **Real-time Monitoring**: Monitor backup execution status with configurable intervals
- **Detailed Reporting**: Generate comprehensive execution reports
- **Flexible Authentication**: Support for token, file, and environment variable authentication
- **Error Handling**: Comprehensive error handling with specific exit codes
- **Timeout Management**: Configurable monitoring timeouts for long-running backups

# Usage Guidelines

The application model should be imported into Visual TOM.
The Visual TOM job must be executed from a system with network access to the HYCU server.

Notes:
The Python script `vtom-hycu_backup-jobs.py` uses generic variables and supports multiple authentication methods.

## Tests with HYCU Integration

### Visual TOM queue Execution
```batch
submit_queue_hycu.bat "Daily Backup" "https://hycu.example.com" "YOUR_TOKEN" "" "30" "3600" "" "" ""
submit_queue_hycu.bat "Production Backup" "https://hycu.example.com" "" "auth.json" "60" "7200" "backup_config.json" "" "verbose"
submit_queue_hycu.bat "Quick Backup" "https://hycu.example.com" "YOUR_TOKEN" "" "30" "3600" "" "no-monitor" ""
```

### Direct execution (Python only)
  ``` Python
python vtom-hycu_backup-jobs.py --backup-name "Daily Backup" --url https://hycu.example.com --auth-token YOUR_TOKEN
python vtom-hycu_backup-jobs.py --backup-name "Production Backup" --url https://hycu.example.com --auth-file auth.json
python vtom-hycu_backup-jobs.py --backup-name "Quick Backup" --url https://hycu.example.com --auth-token YOUR_TOKEN --no-monitor
  ```
 
## Authentication Methods

### 1. Token Authentication
```bash
python vtom-hycu_backup-jobs.py --backup-name "Daily Backup" --url https://hycu.example.com --auth-token YOUR_TOKEN
```

### 2. Authentication File
Create a JSON file with authentication credentials:
```json
{
  "token": "your_hycu_auth_token_here",
  "username": "admin",
  "api_version": "v1"
}
```

Then use it with:
```bash
python vtom-hycu_backup-jobs.py --backup-name "Daily Backup" --url https://hycu.example.com --auth-file auth.json
```

### 3. Environment Variables
```bash
export HYCU_URL=https://hycu.example.com
export HYCU_AUTH_TOKEN=YOUR_TOKEN
python vtom-hycu_backup-jobs.py --backup-name "Daily Backup"
```

## Configuration Files

### Backup Configuration
Create a backup configuration file `backup_config.json`:
```json
{
  "name": "Example Production Backup",
  "type": "full",
  "retention": "30 days",
  "compression": true,
  "encryption": true,
  "schedule": "daily",
  "target": "production-database",
  "priority": "high",
  "notifications": {
    "email": "admin@example.com",
    "webhook": "https://webhook.example.com/backup-status"
  }
}
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success - Backup completed successfully |
| 1 | Configuration error - Missing URL or authentication |
| 2 | Monitoring error - Error during backup monitoring |
| 3 | Timeout error - Backup monitoring timed out |
| 4 | Backup failed - Backup execution failed |
| 5 | Backup cancelled - Backup was cancelled |
| 6 | Unknown status - Backup ended with unknown status |
| 7 | User interruption - Operation cancelled by user |
| 8 | Unexpected error - Unexpected error occurred |

## Report Output

The script generates a detailed report after backup completion:

```
==================================================
HYCU BACKUP EXECUTION REPORT
==================================================
Timestamp: 2024-01-15T10:30:45.123456
Job ID: backup_12345
Status: completed
Start Time: 2024-01-15T10:30:45
End Time: 2024-01-15T10:35:22
Progress: 100%
==================================================
```

## Error Handling

The script includes comprehensive error handling:
- **Network errors**: Connection issues with HYCU API
- **Authentication errors**: Invalid or expired tokens
- **Configuration errors**: Missing required parameters
- **Timeout errors**: Backup monitoring timeouts
- **API errors**: HYCU API response errors

All errors are logged with appropriate messages and exit codes.

## Security Considerations

- Store authentication tokens securely
- Use environment variables for sensitive data
- Ensure authentication files have appropriate permissions
- Consider using encrypted authentication files for production use

## Troubleshooting

### Common Issues

1. **Authentication failed**: Verify your token is valid and not expired
2. **Connection refused**: Check the HYCU URL and network connectivity
3. **Timeout errors**: Increase the timeout value for long-running backups
4. **Permission denied**: Ensure proper file permissions for authentication files

### Debug Mode

Use the `--verbose` flag for detailed logging:
```bash
python vtom-hycu_backup-jobs.py --verbose --backup-name "Debug Backup"
```

## API Compatibility

This script is designed to work with HYCU API v1. The following endpoints are used:
- `POST /api/v1/backups` - Trigger backup
- `GET /api/v1/backups/{job_id}/status` - Get backup status

# License
This project is licensed under the Apache 2.0 License - see the [LICENSE](license) file for details

# Code of Conduct
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS has adopted the [Contributor Covenant](CODE_OF_CONDUCT.md) as its Code of Conduct, and we expect project participants to adhere to it. Please read the [full text](CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.
