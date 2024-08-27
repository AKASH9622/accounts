from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import countries, states, cities
from ..serializers import CountrySerializer, StateSerializer, CountryWithStatesSerializer, CitiesSerializer

@api_view(['GET'])
def get_countries(request):
    country_list = countries.objects.all()
    serializer = CountrySerializer(country_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_states(request):
    state_list = states.objects.all()
    serializer = StateSerializer(state_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_cities(request):
    cities_list = cities.objects.all()
    serializer = CitiesSerializer(cities_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def common_template(request):
    country_list = countries.objects.prefetch_related('states_set').all()
    serializer = CountryWithStatesSerializer(country_list, many=True)
    return Response(serializer.data)