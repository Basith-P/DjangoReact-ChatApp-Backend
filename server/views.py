from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):

        server_id = request.query_params.get("server_id")
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get(
            "by_user", "false").lower() == 'true'
        members_count = request.query_params.get(
            "members_count", "false").lower() == 'true'

        # Check if the request is for a server owned by the authenticated user
        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed(
                "Authentication required to access user-specific data.")

        # Apply filters based on query parameters
        if server_id:
            try:
                self.queryset = self.queryset.filter(id=server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        f"Server with id {server_id} not found")
            except ValueError:
                raise ValidationError("Invalid server ID provided.")

        else:
            if category:
                self.queryset = self.queryset.filter(category__name=category)

            if by_user:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)

            if qty:
                try:
                    qty = int(qty)
                    self.queryset = self.queryset[:qty]
                except ValueError:
                    raise ValidationError(
                        "Invalid 'qty' parameter. It must be an integer.")

        # Annotate the queryset with the count of members if 'members_count' parameter is True
        if members_count:
            self.queryset = self.queryset.annotate(
                members_count=Count("members"))

        serializer = ServerSerializer(self.queryset, many=True, context={
                                      "members_count": members_count})
        return Response(serializer.data)
