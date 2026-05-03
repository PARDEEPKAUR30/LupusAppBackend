from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from .models import LupusData
from .serializers import LupusDataSerializer

from django.http import FileResponse
import os
from django.conf import settings
import json


def home(request):
    return JsonResponse({"message": "API is working!"})


@api_view(['POST'])
def predict_lupus(request):
    try:
        data = request.data.copy()  # Create a mutable copy of request data
        # print("data>>>>>>>>>>>>>>",data)

        
        serializer = LupusDataSerializer(data=data)
        if serializer.is_valid():
            # Save data to database
            lupus_instance = serializer.save()
            # Perform ML prediction (Replace with actual ML model call)
            print("data>>>>>>>>>>>>>> after seralizer",data)
            prediction_result = calculate_weightage(data) 
            print("prediction_result>>>>>>>>>>>>>",prediction_result)
            
            if not prediction_result:
                return Response({
                    "prediction": "Something went wrong. Please try again!"
                }, status=400)


            result_data = json.loads(prediction_result.content)

            return Response({
                "prediction": result_data.get("prediction"),
                "weightage": result_data.get("weightage"),
                "clinical_criterion":result_data.get("clinical_criterion"),
                "data": serializer.data
            })
        
        return Response(serializer.errors, status=400)
    except Exception as e:
        print("Error in predict lupus>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:",e)
        return Response(serializer.errors, status=400)

def calculate_weightage(data):
    try:
        ana=data.get("ana","Positive")
        fever=data.get("fever","No")
        antiDsDNA=data.get("antiDsDNA","No")
        antiSmith=data.get("antiSmith","No")
        hemolysis=data.get("hemolysis","No")
        delirium=data.get("delirium","No")
        psychosis=data.get("psychosis","No")
        seizure=data.get("seizure","No")
        alopecia=data.get("alopecia","No")
        oralUlcers=data.get("oralUlcers","No")
        discoidRash=data.get("discoidRash","No")
        photosensitivity=data.get("photosensitivity","No")
        pleuralEffusion=data.get("pleuralEffusion","No")
        pericarditis=data.get("pericarditis","No")
        jointPain=data.get("jointPain","No")
        renalClass2=data.get("renalClass2","No")
        renalClass3=data.get("renalClass3","No")
        anticardiolipin=data.get("anticardiolipin","No")
        antiB2GPI=data.get("antiB2GPI","No")
        lupusAnticoagulant=data.get("lupusAnticoagulant","No")
        tlc=int(data.get("tlc", 4000) if data.get("tlc") is not None else 4000)
        plateletCount = float(data.get("plateletCount", 1.0) if data.get("plateletCount") is not None else 1.0)
        urineRoutine = float(data.get("urineRoutine", 0.1) if data.get("urineRoutine") is not None else 0.1)
        c3 = float(data.get("c3", 80) if data.get("c3") is not None else 80.0)
        c4 = float(data.get("c4", 10) if data.get("c4") is not None else 10.0)


        weightage=0
        clinical_criterion_fulfilled="No"

        if ana=="Positive":
            #SLE-specific antibodies
            if antiDsDNA=="Yes" or antiSmith=="Yes":
                weightage+=6

            #Constitutional
            if fever=="Yes":
                weightage+=2
                clinical_criterion_fulfilled="Yes"
                print("weightage after fever:", weightage)
            

            #Hematologic
            domain_score=0
            print("tlc>>>>>>>>>>>>>>>>>>>>>>>",tlc)
            if tlc<4000:
                print("tlc value:",tlc)
                domain_score=3

            if plateletCount<1.0:
                print("plt value:",plateletCount)
                domain_score=4

            if hemolysis=="Yes":
                domain_score=4

            weightage+=domain_score
            print("weightage after Hematologic:", weightage)

            
            #Neuropsychiatric
            domain_score=0
            if delirium=="Yes":
                domain_score=2
                clinical_criterion_fulfilled="Yes"

            if psychosis=="Yes":
                domain_score=3
                clinical_criterion_fulfilled="Yes"

            if seizure=="Yes":
                domain_score=5
                clinical_criterion_fulfilled="Yes"

            weightage+=domain_score
            print("weightage after Neuropsychiatric:", weightage)

            
            #Mucocutaneous
            domain_score=0
            if alopecia=="Yes":
                domain_score=2
                clinical_criterion_fulfilled="Yes"

            if oralUlcers=="Yes":
                domain_score=2
                clinical_criterion_fulfilled="Yes"

            if discoidRash=="Yes":
                domain_score=4
                clinical_criterion_fulfilled="Yes"

            if photosensitivity=="Yes":
                domain_score=6
                clinical_criterion_fulfilled="Yes"

            weightage+=domain_score
            print("weightage after Neuropsychiatric:", weightage)

            
            #Serosal
            domain_score=0
            if pleuralEffusion=="Yes":
                domain_score=5

            if pericarditis=="Yes":
                domain_score=6

            weightage+=domain_score
            print("weightage after Neuropsychiatric:", weightage)

            
            #Musculoskeletal
            if jointPain=="Yes":
                weightage+=6
                clinical_criterion_fulfilled="Yes"
                print("weightage after Neuropsychiatric:", weightage)

            #Renal
            domain_score=0
            if urineRoutine>0.5:
                print("urineRoutine value:",urineRoutine)
                domain_score=4
                
            if renalClass2=="Yes":
                domain_score=8
                
            if renalClass3=="Yes":
                domain_score=10

            weightage+=domain_score
            print("weightage after Neuropsychiatric:", weightage)

            #Antiphospholipid antibodies
            if anticardiolipin=="Yes" or antiB2GPI=="Yes" or lupusAnticoagulant=="Yes":
                weightage+=2
                print("weightage after ntiphospholipid antibodies:", weightage)

            #Complement proteins
            domain_score=0
            if c3<80 or c4<10:
                print("c3 value:",c3)
                print("c4 value:",c4)
                domain_score=3

            if c3<80 and c4<10:
                domain_score=4

            weightage+=domain_score
            print("weightage after Complement proteins:", weightage)


            # check conditions
            if weightage>=10 and clinical_criterion_fulfilled=="Yes":
                return JsonResponse({'prediction': 'Criteria Met', 'weightage': weightage, 'clinical_criterion':clinical_criterion_fulfilled })
            elif weightage>=10 and clinical_criterion_fulfilled!="Yes":
                return JsonResponse({'prediction': 'Criteria not Met (Clinical criterion is not fullfilled)', 'weightage': weightage, 'clinical_criterion':clinical_criterion_fulfilled })
            else:
                return JsonResponse({'prediction': 'Criteria Not Met', 'weightage': weightage, 'clinical_criterion':clinical_criterion_fulfilled})      
        else:
            return JsonResponse({'prediction': 'Not eligible for Criteria (Require positive ANA test ≥ 1:80)', 'weightage': weightage, 'clinical_criterion':clinical_criterion_fulfilled})

    except Exception as e:
        print("Error>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:",e)
        return False



def privacy_policy(request):
    return render(request, 'privacy_policy.html')
    
def downloads(request):
    return HttpResponse(
        '<h2>Welcome to LupusApp</h2>'
        '<a href="/api/download-apk/">Download Lupus Check App</a>'
    )

def download_apk(request):
    file_path = os.path.join(settings.BASE_DIR, 'LupusAppBackend', 'downloads', 'app-release.apk')

    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename='app-release.apk'
    )
def lupuscheck_app(request):
    fields = [
        ("antiDsDNA", "Anti-dsDNA"),
        ("antiSmith", "Anti-Smith"),
        ("fever", "Fever"),
        ("hemolysis", "Autoimmune Hemolysis"),
        ("delirium", "Delirium"),
        ("psychosis", "Psychosis"),
        ("seizure", "Seizure"),
        ("alopecia", "Non-Scarring Alopecia"),
        ("oralUlcers", "Oral Ulcers"),
        ("discoidRash", "Subacute Cutaneous or Discoid Lupus"),
        ("photosensitivity", "Acute Cutaneous Lupus"),
        ("jointPain", "Joint Involvement"),
        ("pleuralEffusion", "Pleural/Pericardial Effusion"),
        ("pericarditis", "Acute Pericarditis"),
        ("anticardiolipin", "Anticardiolipin Antibodies"),
        ("antiB2GPI", "Anti-beta2 glycoprotein 1 antibodies"),
        ("lupusAnticoagulant", "Lupus Anticoagulant"),
        ("renalClass2", "Renal biopsy class II/V lupus"),
        ("renalClass3", "Renal biopsy class III/IV lupus"),
    ]
    return render(request, 'lupuscheck_app.html', {"fields":fields})

def lupuscheck_link(request):
    return render(request, 'app_icon.html')