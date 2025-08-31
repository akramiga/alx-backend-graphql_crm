# CRM Celery Setup

## Requirements
- Redis running locally on port 6379

## Steps
1. Install dependencies:

pip install -r requirements.txt

2. Run database migrations:

python manage.py migrate

3. Start Celery worker:

celery -A crm worker -l info

4. Start Celery Beat:

celery -A crm beat -l info

5. Logs:
- Weekly CRM reports are written to `/tmp/crm_report_log.txt`
