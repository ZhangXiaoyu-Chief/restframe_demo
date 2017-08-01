from django.shortcuts import render,HttpResponse
from demo.serializers import BookSerializer
from demo.models import Book
from rest_framework.renderers import JSONRenderer

# Create your views here.


def publisher_detail(requst):
    return HttpResponse("")


def book_detail(request, pk):

    book_obj = Book.objects.filter(id=pk).first()
    serializer = BookSerializer(book_obj, context={"request": request})
    json_data = JSONRenderer().render(serializer.data)

    return HttpResponse(json_data.decode())