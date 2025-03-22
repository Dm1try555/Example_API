import os
import time
import boto3
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.http import MediaFileUpload

# MinIO client setup
minio_client = boto3.client('s3',
                            endpoint_url="http://minio:9000",
                            aws_access_key_id="minioaccesskey",
                            aws_secret_access_key="miniosecretkey")


# Google Drive setup
def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive.file'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Google credentials not available")

    return build('drive', 'v3', credentials=creds)


def upload_to_google_drive(file_path, file_name):
    service = authenticate_google_drive()

    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='application/zip')

    request = service.files().create(media_body=media, body=file_metadata, fields='id')
    request.execute()


def backup_minio():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_filename = f"minio_backup_{timestamp}.tar.gz"

    # Create backup with MinIO client (without using `mc mirror` command)
    backup_data = minio_client.list_objects_v2(Bucket='my-backup-bucket').get('Contents', [])
    if backup_data:
        os.system(f"tar -czf /tmp/{backup_filename} /path/to/your/minio/data")  # Example of local backup creation

    upload_to_google_drive(f"/tmp/{backup_filename}", backup_filename)  # Upload to Google Drive

    # Clean up old backups in MinIO
    backups = minio_client.list_objects_v2(Bucket='my-backup-bucket').get('Contents', [])
    backups.sort(key=lambda x: x['LastModified'])
    if len(backups) > 10:
        for old_backup in backups[:len(backups) - 10]:
            minio_client.delete_object(Bucket='my-backup-bucket', Key=old_backup['Key'])


# Run backups every 30 sec instead of seconds
while True:
    try:
        backup_minio()
    except Exception as e:
        print(f"Error occurred during backup: {e}")
    time.sleep(30)
