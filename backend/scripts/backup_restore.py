#!/usr/bin/env python
import os
import sys
import subprocess
from datetime import datetime


def backup_database():
    db_name = os.getenv("POSTGRES_DB", "blueteamers_db")
    db_user = os.getenv("POSTGRES_USER", "blueteamers_user")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{db_name}_{timestamp}.sql"

    print(f"[*] Starting PostgreSQL backup for '{db_name}'...")
    cmd = f"pg_dump -U {db_user} -d {db_name} -F c -f {backup_filename}"
    res = os.system(cmd)

    if res == 0:
        print(f"[+] Backup completed successfully: {backup_filename}")
    else:
        print(f"[-] Backup failed with exit code: {res}")


def restore_database(backup_file):
    db_name = os.getenv("POSTGRES_DB", "blueteamers_db")
    db_user = os.getenv("POSTGRES_USER", "blueteamers_user")

    if not os.path.exists(backup_file):
        print(f"[-] Error: Backup file '{backup_file}' does not exist.")
        sys.exit(1)

    print(f"[*] Restoring PostgreSQL database from '{backup_file}'...")
    cmd = f"pg_restore -U {db_user} -d {db_name} --clean --no-owner {backup_file}"
    res = os.system(cmd)

    if res == 0:
        print(f"[+] Restore completed successfully.")
    else:
        print(f"[-] Restore finished with return code: {res}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        if len(sys.argv) < 3:
            print("Usage: python backup_restore.py restore <path_to_backup_file>")
            sys.exit(1)
        restore_database(sys.argv[2])
    else:
        backup_database()
