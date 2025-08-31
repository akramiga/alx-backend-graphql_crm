import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

def log_crm_heartbeat():
    """Logs a heartbeat message with timestamp and optionally checks GraphQL hello."""
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Default status
    status = "CRM is alive"

    try:
        # Setup GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Define a simple hello query
        query = gql(
            """
            query {
              hello
            }
            """
        )

        result = client.execute(query)
        hello_value = result.get("hello", "No response")

        status += f" | GraphQL hello: {hello_value}"

    except Exception as e:
        status += f" | GraphQL check failed: {e}"

    # Append log
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{now} {status}\n")

def update_low_stock():
    """Executes GraphQL mutation to restock low products and logs results."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Setup GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Define mutation
        mutation = gql(
            """
            mutation {
              updateLowStockProducts {
                success
                updatedProducts
              }
            }
            """
        )

        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{now} - Updated: {', '.join(updated_products)}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{now} - Error: {e}\n")
