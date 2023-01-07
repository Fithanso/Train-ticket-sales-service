from rest_framework import serializers

from train_main_app.models import *
from train_main_app.functions import get_tz_by_name
from tickets.models import PurchasedTicket

import pycountry


class VoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voyage
        fields = "__all__"


class StationInVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationInVoyage
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"


class PurchasedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedTicket
        fields = "__all__"


class VoyagesSearchResultSerializer(serializers.Serializer):
    voyage = VoyageSerializer()
    departure_station = StationSerializer()
    arrival_station = StationSerializer()
    stations_en_route = StationInVoyageSerializer(many=True),
    departure_en_route = StationInVoyageSerializer()
    arrival_en_route = StationInVoyageSerializer()
    arrival_datetime = serializers.DateTimeField()
    seat_prices = serializers.DictField(),
    link_to_purchase = serializers.CharField()
    expired = serializers.BooleanField()


class PurchaseOperationSerializer(serializers.Serializer):
    seat_numbers = serializers.RegexField('^\d{1,}(,\d{1,})*$')
    voyage_pk = serializers.PrimaryKeyRelatedField(queryset=Voyage.objects.all())
    departure_en_route_id = serializers.IntegerField()
    arrival_en_route_id = serializers.IntegerField()
    customers_timezone = serializers.CharField()
    customers_region_code = serializers.CharField()
    customers_phone_number = serializers.RegexField('^[1-9][0-9]{4,14}$')
    customers_email = serializers.EmailField()

    def validate(self, data):
        for seat_number in tuple(data['seat_numbers'].split(',')):
            if PurchasedTicket.objects.filter(voyage_id=data['voyage_pk'], seat_number=seat_number).exists():
                raise serializers.ValidationError("This ticket has already been purchased: " + seat_number)

        return data

    def validate_departure_en_route_id(self, value):
        if not StationInVoyage.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Departure station does not exist")
        return value

    def validate_arrival_en_route_id(self, value):
        if not StationInVoyage.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Arrival station does not exist")
        return value

    def validate_customers_timezone(self, value):
        if not get_tz_by_name(value):
            raise serializers.ValidationError("Timezone does not exist")
        return value

    def validate_customers_region_code(self, value):

        if pycountry.countries.get(alpha_2=value) or pycountry.countries.get(alpha_3=value):
            return value

        raise serializers.ValidationError("Country code does not exist")



