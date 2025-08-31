from datetime import datetime
import requests
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
from celery import shared_task

@shared_task
def generate_crm_report():
    """Weekly CRM report: total customers, orders, revenue."""

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = f"{now} - Report: "

    try:
        # GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql(
            """
            query {
              customers {
                totalCount
              }
              orders {
                totalCount
                totalRevenue
              }
            }
            """
        )

        result = client.execute(query)

        total_customers = result["customers"]["totalCount"]
        total_orders = result["orders"]["totalCount"]
        total_revenue = result["orders"]["totalRevenue"]

        status += f"{total_customers} customers, {total_orders} orders, {total_revenue} revenue"

    except Exception as e:
        status += f"Error fetching data: {e}"

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(status + "\n")

    return status

