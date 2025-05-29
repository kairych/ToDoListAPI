import requests
from bs4 import BeautifulSoup
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from to_do_app.models import Task, AstanaHub
from .filters import TaskFilter
from .serializers import TaskSerializer, AstanaHubSerializer


class TaskListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated]


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class ParseAstanaHubView(APIView):
    """Parse AstanaHub website and save the first 10 companies to the database"""
    def post(self, request):
        url = 'https://astanahub.com/ru/service/techpark/'
        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table')

        if not table:
            return Response({"error": "No table found"}, status=status.HTTP_400_BAD_REQUEST)

        rows = table.find_all('tr')[1:11]
        parsed_data = []

        for row in rows:
            cols = row.find_all('td')

            obj = AstanaHub.objects.create(
                cert_number=cols[0].get_text(strip=True),
                cert_issue_date=cols[1].get_text(strip=True),
                cert_expire_date=cols[2].get_text(strip=True),
                bin=cols[3].get_text(strip=True),
                is_active=True if cols[4].get_text(strip=True) == 'Активно' else False,
                company_name=cols[5].get_text(strip=True),
            )
            parsed_data.append(obj)

        serializer = AstanaHubSerializer(parsed_data, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
