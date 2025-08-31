#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Define query for orders in the last 7 days
query = gql(
    """
    query GetRecentOrders($cutoff: DateTime!) {
      orders(filter: { orderDate_Gte: $cutoff }) {
        id
        customer {
          email
        }
      }
    }
    """
)

# Compute cutoff datetime
cutoff = (datetime.now() - timedelta(days=7)).isoformat()

try:
    result = client.execute(query, variable_values={"cutoff": cutoff})
    orders = result.get("orders", [])
except Exception as e:
    orders = []
    with open("/tmp/order_reminders_log.txt", "a") as log:
        log.write(f"{datetime.now()} - Error fetching orders: {e}\n")

# Log results
with open("/tmp/order_reminders_log.txt", "a") as log:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if orders:
        for order in orders:
            log.write(f"{timestamp} - Order {order['id']} for {order['customer']['email']}\n")
    else:
        log.write(f"{timestamp} - No recent orders found\n")

print("Order reminders processed!")

