from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from ..serializers.todo_serializer import TaskSerializers
from ..models import Task


class TodoListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        tasks = user.task.all()
        return Response(data={
            "count" : len(tasks),
            "data" : TaskSerializers(tasks, many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = TaskSerializers(data=request.data)

        if serializer.is_valid():
            title = serializer.data.get("title", None)
            description = serializer.data.get("description", None)

            if not title:
                return Response(data={
                    "message": "Title is missing"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            task = Task.objects.create(title=title, description=description, user=user)
            task.save()
            return Response(data={
                "message": "Successfully created",
            })

        return Response(data={"message": "Invalid information"}, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        try:
            task = Task.objects.filter(pk=pk).first()
            return Response(data={
                "data" : TaskSerializers(task).data
            }, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(data={
                "data" : {}
            }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            task = Task.objects.filter(pk=pk).first()
            serializer = TaskSerializers(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(data={
                "message" : "Successfully modify",
                "data" : serializer.data
            }, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(data={
                "data" : {}
            }, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        task = Task.objects.filter(pk=pk).first()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        