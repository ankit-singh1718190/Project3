from rest_framework import serializers
from .models import student
#validetors
def StartWithR(value):
    if value[0].lower() !='r':
        raise serializers.ValidationError('name should be start withe R')

class StudentSerializer(serializers.Serializer):
     name=serializers.CharField(max_length=50,validators=[StartWithR])
     city=serializers.CharField(max_length=50)
     roll=serializers.IntegerField()

     def create(self, validated_data):
          return student.objects.create(**validated_data)

     def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.city = validated_data.get('city', instance.city)
        instance.roll = validated_data.get('roll', instance.roll)
        instance.save()
        return instance
      #fields level validation 
     def validate_roll(self, value):
         if value >=200:
             raise serializers.ValidationError('set is full')
         return value
     #object leavel validaction
     def validate(self, data):
         nam=data.get('name')
         ciy=data.get('city')
         if nam.lower()=='ankit' and ciy.lower()!='lucknow':
             raise serializers.ValidationError('city must be Lucknow')
         return data