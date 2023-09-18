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
        by_user = request.query_params.get("by_user") == 'true'
        members_count = request.query_params.get("members_count") == 'true'

        if by_user or server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if server_id:
            try:
                self.queryset = self.queryset.filter(id=server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {server_id} not found")
            except ValueError:
                raise ValidationError(detail="Something went wrong")
        else:
            if category:
                self.queryset = self.queryset.filter(category__name=category)

            if by_user:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)

            if members_count:
                self.queryset = self.queryset.annotate(
                    members_count=Count("members"))

            if qty:
                self.queryset = self.queryset[:int(qty)]

        serializer = ServerSerializer(self.queryset, many=True, context={
                                      "members_count": members_count})
        return Response(serializer.data)
