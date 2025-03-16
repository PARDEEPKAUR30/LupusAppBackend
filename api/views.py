from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import LupusData
from .serializers import LupusDataSerializer


def home(request):
    return JsonResponse({"message": "API is working!"})


@api_view(['POST'])
def predict_lupus(request):
    try:
        data = request.data.copy()  # Create a mutable copy of request data
        
        # Convert "Yes"/"No" values to boolean True/False
        boolean_fields = [
            "fever", "alopecia", "oralUlcers", "discoidRash", "photosensitivity", "jointPain",
            "pleuralEffusion", "pericarditis", "delirium", "psychosis", "seizure",
            "renalClass2", "renalClass3","anticardiolipin", "antiB2GPI", "lupusAnticoagulant",
        ]
        for field in boolean_fields:
            if field in data:
                data[field] = data[field] == "Yes"  # Convert "Yes" to True, "No" to False

        # Convert numeric fields to float (if empty, set to None)
        numeric_fields = [
            "urineRoutine", "haemoglobin", "tlc", "plateletCount",
            "c3", "c4", "antiDsDNA", "antiSmith"
        ]
        for field in numeric_fields:
            value = data.get(field)
            
            if value is None or value == "":  
                data[field] = 0.0  # Set a default value like 0.0
            else:
                try:
                    data[field] = float(value)  # Convert to float
                except ValueError:
                    data[field] = 0.0  # Handle invalid values safely


        serializer = LupusDataSerializer(data=data)

        if serializer.is_valid():
            # Save data to database
            lupus_instance = serializer.save()

            # Perform ML prediction (Replace with actual ML model call)
            prediction_result = calculate_weightage(data) if calculate_weightage(data) else 'Something went wrong. Please try again!'

            print("prediction_result>>>>>>>>>>>>>",prediction_result)
            return Response({
                "prediction": prediction_result,
                "data": serializer.data
            })
        
        return Response(serializer.errors, status=400)
    except Exception as e:
        print("Error in predict lupus>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:",e)
        return Response(serializer.errors, status=400)

def calculate_weightage(data):
    try:
        fever=data.get("fever","No")
        alopecia=data.get("alopecia","No")
        oralUlcers=data.get("oralUlcers","No")
        discoidRash=data.get("discoidRash","No")
        photosensitivity=data.get("photosensitivity","No")
        jointPain=data.get("jointPain","No")
        pleuralEffusion=data.get("pleuralEffusion","No")
        pericarditis=data.get("pericarditis","No")
        delirium=data.get("delirium","No")
        psychosis=data.get("psychosis","No")
        seizure=data.get("seizure","No")
        anticardiolipin=data.get("anticardiolipin","No")
        antiB2GPI=data.get("antiB2GPI","No")
        lupusAnticoagulant=data.get("lupusAnticoagulant","No")
        renalClass2=data.get("renalClass2","No")
        renalClass3=data.get("renalClass3","No")
        urineRoutine=float(data.get("urineRoutine", 0))
        haemoglobin=float(data.get("haemoglobin", 0))
        tlc=float(data.get("tlc", 0))
        plateletCount=float(data.get("plateletCount", 0))
        c3=float(data.get("c3", 0))
        c4=float(data.get("c4", 0))
        antiDsDNA=float(data.get("antiDsDNA", 0))
        antiSmith=float(data.get("antiSmith", 0))

        weightage=0
        if antiDsDNA>370.5 or antiSmith>=1.0:
            weightage+=6
            if fever:
                weightage+=2
            
            if haemoglobin<12:
                weightage+=3
            if tlc<4000:
                weightage+=4
            if plateletCount<1.0:
                weightage+=4


            if delirium:
                weightage+=2
            if psychosis:
                weightage+=3
            if seizure:
                weightage+=5


            if alopecia:
                weightage+=2
            if oralUlcers:
                weightage+=2
            if discoidRash:
                weightage+=4
            if photosensitivity:
                weightage+=6


            if pleuralEffusion:
                weightage+=5
            if pericarditis:
                weightage+=6


            if jointPain:
                weightage+=6


            if urineRoutine>0.5:
                weightage+=4
            if renalClass2:
                weightage+=8
            if renalClass3:
                weightage+=10

            if anticardiolipin or antiB2GPI or lupusAnticoagulant:
                weightage+=2

            if c3<80 or c4<10:
                weightage+=3
            elif c3<80 and c4<10:
                 weightage+=4


            if weightage>10:
                return 'Criteria Met' 
            else:
                return 'Criteria Not Met'      
        else:
            return 'Criteria Not Met'

    except Exception as e:
        print("Error>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:",e)
        return False
