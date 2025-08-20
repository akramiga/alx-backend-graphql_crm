import graphene

# Define a Query class that inherits from graphene.ObjectType
class Query(graphene.ObjectType):
    # Declare a field called 'hello' of type String
    hello = graphene.String()

    # Resolver method for the 'hello' field
    def resolve_hello(root, info):
        return "Hello, GraphQL!"

# Create a schema with the Query
schema = graphene.Schema(query=Query)
