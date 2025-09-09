#!/usr/bin/env python3
"""
HYCU Backup Manager
===================

A Python script for triggering and monitoring HYCU backups via command line interface.

This script provides functionality to:
- Trigger HYCU backups
- Monitor backup execution status
- Generate execution reports
- Handle authentication via multiple methods
- Return appropriate exit codes for different scenarios

Author: HYCU Integration Team
Version: 1.0.0
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HYCUBackupManager:
    """Main class for managing HYCU backup operations."""
    
    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        """
        Initialize HYCU Backup Manager.
        
        Args:
            base_url: HYCU API base URL
            auth_token: Authentication token for API access
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.session = requests.Session()
        
        if auth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {auth_token}',
                'Content-Type': 'application/json'
            })
    
    def trigger_backup(self, backup_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger a backup operation.
        
        Args:
            backup_config: Backup configuration parameters
            
        Returns:
            Dictionary containing backup job information
        """
        try:
            url = f"{self.base_url}/api/v1/backups"
            response = self.session.post(url, json=backup_config)
            response.raise_for_status()
            
            logger.info("Backup triggered successfully")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to trigger backup: {e}")
            raise
    
    def get_backup_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a backup job.
        
        Args:
            job_id: Backup job ID
            
        Returns:
            Dictionary containing backup status information
        """
        try:
            url = f"{self.base_url}/api/v1/backups/{job_id}/status"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get backup status: {e}")
            raise
    
    def monitor_backup(self, job_id: str, check_interval: int = 30, timeout: int = 3600) -> Dict[str, Any]:
        """
        Monitor backup execution until completion.
        
        Args:
            job_id: Backup job ID
            check_interval: Interval between status checks (seconds)
            timeout: Maximum monitoring time (seconds)
            
        Returns:
            Final backup status
        """
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Backup monitoring timed out after {timeout} seconds")
            
            status = self.get_backup_status(job_id)
            current_status = status.get('status', 'unknown')
            
            logger.info(f"Backup {job_id} status: {current_status}")
            
            if current_status in ['completed', 'failed', 'cancelled']:
                return status
            
            time.sleep(check_interval)
    
    def generate_report(self, backup_result: Dict[str, Any]) -> str:
        """
        Generate a human-readable report from backup results.
        
        Args:
            backup_result: Backup execution results
            
        Returns:
            Formatted report string
        """
        report_lines = [
            "=" * 50,
            "HYCU BACKUP EXECUTION REPORT",
            "=" * 50,
            f"Timestamp: {datetime.now().isoformat()}",
            f"Job ID: {backup_result.get('job_id', 'N/A')}",
            f"Status: {backup_result.get('status', 'N/A')}",
            f"Start Time: {backup_result.get('start_time', 'N/A')}",
            f"End Time: {backup_result.get('end_time', 'N/A')}",
        ]
        
        if 'progress' in backup_result:
            report_lines.append(f"Progress: {backup_result['progress']}%")
        
        if 'error_message' in backup_result:
            report_lines.append(f"Error: {backup_result['error_message']}")
        
        if 'details' in backup_result:
            report_lines.append("\nDetails:")
            for key, value in backup_result['details'].items():
                report_lines.append(f"  {key}: {value}")
        
        report_lines.append("=" * 50)
        
        return "\n".join(report_lines)

def load_auth_from_file(auth_file: str) -> Dict[str, str]:
    """
    Load authentication credentials from file.
    
    Args:
        auth_file: Path to authentication file
        
    Returns:
        Dictionary containing authentication credentials
    """
    try:
        with open(auth_file, 'r') as f:
            auth_data = json.load(f)
        return auth_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load auth file: {e}")
        raise

def main():
    """Main function for command line execution."""
    parser = argparse.ArgumentParser(
        description="HYCU Backup Manager - Trigger and monitor HYCU backups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Trigger a backup with basic authentication
  python hycu_backup_manager.py --url https://hycu.example.com --auth-token YOUR_TOKEN --backup-name "Daily Backup"
  
  # Use environment variables for authentication
  export HYCU_URL=https://hycu.example.com
  export HYCU_AUTH_TOKEN=YOUR_TOKEN
  python hycu_backup_manager.py --backup-name "Daily Backup"
  
  # Use authentication file
  python hycu_backup_manager.py --url https://hycu.example.com --auth-file auth.json --backup-name "Daily Backup"
  
  # Monitor with custom intervals
  python hycu_backup_manager.py --url https://hycu.example.com --auth-token YOUR_TOKEN --backup-name "Daily Backup" --check-interval 60 --timeout 7200

Environment Variables:
  HYCU_URL: HYCU API base URL
  HYCU_AUTH_TOKEN: Authentication token for API access
  HYCU_AUTH_FILE: Path to authentication file
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--backup-name',
        required=True,
        help='Name of the backup to trigger'
    )
    
    # Optional arguments
    parser.add_argument(
        '--url',
        help='HYCU API base URL (can also be set via HYCU_URL environment variable)'
    )
    
    parser.add_argument(
        '--auth-token',
        help='Authentication token (can also be set via HYCU_AUTH_TOKEN environment variable)'
    )
    
    parser.add_argument(
        '--auth-file',
        help='Path to authentication file containing credentials (can also be set via HYCU_AUTH_FILE environment variable)'
    )
    
    parser.add_argument(
        '--check-interval',
        type=int,
        default=30,
        help='Interval between status checks in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=3600,
        help='Maximum monitoring time in seconds (default: 3600)'
    )
    
    parser.add_argument(
        '--backup-config',
        help='Path to JSON file containing backup configuration'
    )
    
    parser.add_argument(
        '--no-monitor',
        action='store_true',
        help='Trigger backup without monitoring execution'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Get configuration from arguments or environment variables
        base_url = args.url or os.getenv('HYCU_URL')
        if not base_url:
            logger.error("HYCU URL not provided. Use --url argument or HYCU_URL environment variable.")
            sys.exit(1)
        
        # Get authentication
        auth_token = args.auth_token or os.getenv('HYCU_AUTH_TOKEN')
        auth_file = args.auth_file or os.getenv('HYCU_AUTH_FILE')
        
        if auth_file:
            auth_data = load_auth_from_file(auth_file)
            auth_token = auth_data.get('token', auth_token)
        
        if not auth_token:
            logger.error("Authentication token not provided. Use --auth-token, --auth-file, or environment variables.")
            sys.exit(1)
        
        # Initialize backup manager
        manager = HYCUBackupManager(base_url, auth_token)
        
        # Prepare backup configuration
        backup_config = {
            'name': args.backup_name,
            'timestamp': datetime.now().isoformat()
        }
        
        # Load additional configuration if provided
        if args.backup_config:
            try:
                with open(args.backup_config, 'r') as f:
                    additional_config = json.load(f)
                backup_config.update(additional_config)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.error(f"Failed to load backup config file: {e}")
                sys.exit(1)
        
        # Trigger backup
        logger.info(f"Triggering backup: {args.backup_name}")
        backup_result = manager.trigger_backup(backup_config)
        
        job_id = backup_result.get('job_id')
        if not job_id:
            logger.error("No job ID received from backup trigger")
            sys.exit(1)
        
        logger.info(f"Backup job created with ID: {job_id}")
        
        # Monitor backup if requested
        if not args.no_monitor:
            logger.info("Starting backup monitoring...")
            try:
                final_status = manager.monitor_backup(
                    job_id, 
                    args.check_interval, 
                    args.timeout
                )
                backup_result.update(final_status)
            except TimeoutError as e:
                logger.error(f"Backup monitoring timed out: {e}")
                sys.exit(3)
            except Exception as e:
                logger.error(f"Error during backup monitoring: {e}")
                sys.exit(2)
        
        # Generate and print report
        report = manager.generate_report(backup_result)
        print(report)
        
        # Return appropriate exit code
        status = backup_result.get('status', 'unknown')
        if status == 'completed':
            logger.info("Backup completed successfully")
            sys.exit(0)
        elif status == 'failed':
            logger.error("Backup failed")
            sys.exit(4)
        elif status == 'cancelled':
            logger.warning("Backup was cancelled")
            sys.exit(5)
        else:
            logger.warning(f"Backup ended with unknown status: {status}")
            sys.exit(6)
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(7)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(8)

if __name__ == "__main__":
    main() 