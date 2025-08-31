#!/bin/bash

# Navigate to project root (update with absolute path if on actual machine virtual/otherwise)
cd /absolute/path/to/alx-backend-graphql_crm || exit

# Run Django cleanup command
deleted=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

# Log with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$deleted inactive customers\" >> /tmp/customer_cleanup_log.txt
