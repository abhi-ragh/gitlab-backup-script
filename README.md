# GitLab Backup and Recovery Script

This script automates a comprehensive GitLab repository export and import process, ensuring data safety and reliable cloud synchronization.
It includes rigorous failure checks, structured storage, and full restoration validation.

## Features
- Automated GitLab Export: Creates export backups for 2-3 specified GitLab repositories using the GitLab API.
- Structured Backup Storage: Backups are stored in a dedicated folder structure within the VM environment, named according to the current date (e.g., backup_YYYY-MM-DD/).
- Reliable Error Handling: Implements logic to check the export status, manage failed exports, and perform necessary retries before proceeding.
- Secure Cloud Upload: Successfully exported backup files are immediately copied to S3 for reliable, offsite storage. Imports can function directly from the S3 location.
- Retention Policy: The VM enforces a local 7-day retention policy, automatically cleaning up older backups to manage storage.
- Import Validation: Ensures repositories are fully restored with proper naming conventions, performing a final validation check after import to confirm all files, branches, and commits are intact.
- Periodic Scheduling (Optional): Designed to be run periodically (e.g., via cron jobs), automatically creating a new, date-stamped backup folder each day.

This solution is designed to run within a dedicated Virtual Machine (VM) to manage execution, file retention, and environment dependencies efficiently.
