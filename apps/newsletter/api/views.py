from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SubscriberSerializer

import json
from django.http import JsonResponse
from apps.newsletter.models import Subscriber
from .serializers import SubscriberSerializer 

def add_subscriber(request):
    # Convert the JSON data into a Python dictionary
    data = json.loads(request.body)
    email = data.get('email')  # Use get() to safely retrieve the 'email' field

    # Create a new Subscriber instance using the serializer
    serializer = SubscriberSerializer(data={'email': email})
    if serializer.is_valid():
        serializer.save()  # Save the instance to the database
        return JsonResponse({'success': True})
    else:
        # If the serializer is not valid, return an error response
        return JsonResponse({'error': serializer.errors}, status=400)




# @api_view(['GET'])
# def subscriber_list(request):
#     subscribers = Subscriber.objects.all()
#     serializer = SubscriberSerializer(subscribers, many=True)
#     return Response(serializer.data)

# import json

# from django.http import JsonResponse

# from apps.newsletter.models import Subscriber

# def api_add_subscriber(request):
#     data = json.loads(request.body)
#     email = data['email']

#     s = Subscriber.objects.create(email=email)

#     return JsonResponse({'success': True})