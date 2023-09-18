# Import necessary modules
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer


# Define a viewset for handling server list requests
class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()  # Initialize the queryset with all Server objects

    # Define the list method to handle GET requests
    def list(self, request):
        # Extract query parameters from the request
        server_id = request.query_params.get("server_id")
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == 'true'
        members_count = request.query_params.get("members_count") == 'true'

        # Check if the request is for a server owned by the authenticated user
        # If 'by_user' is set to True and the user is not authenticated, raise AuthenticationFailed exception
        if by_user or (server_id and not request.user.is_authenticated):
            raise AuthenticationFailed()

        # Check if a specific server ID is provided in the query parameters
        if server_id:
            try:
                # Filter the queryset to retrieve the server with the specified ID
                self.queryset = self.queryset.filter(id=server_id)
                # If the server with the specified ID doesn't exist, raise a ValidationError
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {server_id} not found")
            except ValueError:
                raise ValidationError(detail="Something went wrong")
        else:
            # If no specific server ID is provided, apply additional filters based on other query parameters

            # Filter servers by category if 'category' parameter is provided
            if category:
                self.queryset = self.queryset.filter(category__name=category)

            # Filter servers by the authenticated user's ID if 'by_user' parameter is True
            if by_user:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)

            # Limit the queryset to a specified quantity of servers if 'qty' parameter is provided
            if qty:
                self.queryset = self.queryset[:int(qty)]

        # Annotate the queryset with the count of members if 'members_count' parameter is True
        if members_count:
            self.queryset = self.queryset.annotate(
                members_count=Count("members"))

        # Serialize the queryset into ServerSerializer format and return the response
        serializer = ServerSerializer(self.queryset, many=True, context={
                                      "members_count": members_count})

        return Response(serializer.data)
