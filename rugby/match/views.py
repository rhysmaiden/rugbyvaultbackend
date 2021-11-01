from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


from rugby.match.models import Match
from rugby.match.serializers import MatchSerializer



class ApiMatchListView(ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = PageNumberPagination