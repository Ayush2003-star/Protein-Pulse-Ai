from urllib import request

from django.shortcuts import render,redirect
import pandas as pd
from .models import ProteinData, ProteiDataHist
from django.db.models import IntegerField,Min,Max
from django.db.models.functions import Cast
import joblib

# Create your views here.

def home(request):
     #ProteinData.objects.create(age = 24)
#    data_frame = pd.read_csv('model\protein_dataset.csv')
#    for i,j in data_frame.iterrows():
#        ProteinData.objects.create(age=j['age'],gender=j['gender'],weight_kg=j['weight_kg'],activity_level=j['activity_level'],purpose=j['purpose'],lean_body_mass_kg=j['lean_body_mass_kg'],bmr=j['bmr'],protein_need_per_lean_kg_sedentary=j['protein_need_per_lean_kg_sedentary'],protein_need_per_lean_kg_active=j['protein_need_per_lean_kg_active'],protein_need_per_lean_kg_very_active=j['protein_need_per_lean_kg_very_active'],protein_per_kg_min=j['protein_per_kg_min'],protein_per_kg_moderate=j['protein_per_kg_moderate'],protein_per_kg_max=j['protein_per_kg_max'],activity_protein_multiplier=j['activity_protein_multiplier'],adjusted_protein_need=j['adjusted_protein_need'],age_protein_factor=j['age_protein_factor'],protein_for_age_group=j['protein_for_age_group'],gender_protein_base   =j['gender_protein_base'],protein_gender_adjusted=j['protein_gender_adjusted'],purpose_protein_multiplier=j['purpose_protein_multiplier'],protein_for_purpose=j['protein_for_purpose'],lean_to_total_ratio=j['lean_to_total_ratio'],muscle_mass_score=j['muscle_mass_score'],bmr_per_kg=j['bmr_per_kg'],protein_metabolic_need=j['protein_metabolic_need'],training_intensity=j['training_intensity'],recovery_protein_need=j['recovery_protein_need'],protein_g=j['protein_g'] )
    features_list=[{'icon': '🤖', 'Title': 'ModelAI', 'desc': 'trains Ml algorithms and automatically picks the best one.'},
                   {'icon':'🧪','Title':'Body Composition','desc':'Esyimates your body fat,leanmass and BMR from your measurements.'},
                   {'icon':'🎯','Title':'Goal specific','desc':'Different protein targets for weight loss,maintainence,and muscle gain.'},
                   {'icon':'🍽️','Title':'Meal Frequency','desc':'Account for how many meals you eat to optimise protein intake.'},
                   {'icon':'💪','Title':'Experience level','desc':'Advanced athletes need more protein '},
                   {'icon':'📊','Title':'Health','desc':'Get Bmr,TDEE,BMI,and a protein range-not just one number.'},]
    
    steps_list = [
    {
        'num': '1',
        'icon': '📝',
        'title': 'Enter Your Details',
        'desc': 'Fill in your age, weight, height, activity, goal, meals, and experience.'
    },
    {
        'num': '2',
        'icon': '🤖',
        'title': 'AI Analyses',
        'desc': 'Our ML model processes your data and makes a smart prediction.'
    },
    {
        'num': '3',
        'icon': '📈',
        'title': 'Get Your Plan',
        'desc': 'Receive a personalised daily protein target with a full report.'
    },
    ]
 
    return render(request, 'home.html',{'features_list':features_list,'steps_list':steps_list})

def predict(request):
        if request.method=='POST':
         print(request.POST,'nvfdgshd')
         data_frame = pd.DataFrame([request.POST.dict()])
         data_frame= data_frame.drop(['meals_per_day','fitness_experience','csrfmiddlewaretoken', 'height_cm'],axis=1)
         Age = int(request.POST.get('age'))
         Gender = request.POST.get('gender')
         Height_cm = float(request.POST.get('height_cm'))
         weight_kg = float(request.POST.get('weight_kg'))
         Activity_level = request.POST.get('activity_level')
         purpose = request.POST.get('purpose')
         Meals_dat = request.POST.get('meals_per_day')
         fitness_experience = request.POST.get('fitness_experience')
        
        #lean_body_mass_kg
         if Gender == 'Male':
            lean_body_mass_kg = (0.407 * weight_kg) + (0.267 * Height_cm) - 19.2
         else:
            lean_body_mass_kg = (0.252 * weight_kg) + (0.473 * Height_cm) - 48.3
         data_frame['lean_body_mass_kg'] = lean_body_mass_kg
        
        #bmr
         if Gender == "Male":
            bmr = (10 * weight_kg) + (6.25 * Height_cm) - (5 * Age) + 5
         else:
            bmr = (10 * weight_kg) + (6.25 * Height_cm) - (5 * Age) - 161

         data_frame["bmr"] = bmr
        
        
    
        
        
       # protein_need_per_lean_kg

         protein_need_per_lean_kg_sedentary = lean_body_mass_kg * 1.0
         protein_need_per_lean_kg_active = lean_body_mass_kg * 1.2
         protein_need_per_lean_kg_very_active = lean_body_mass_kg * 1.4

         data_frame["protein_need_per_lean_kg_sedentary"] = protein_need_per_lean_kg_sedentary
         data_frame["protein_need_per_lean_kg_active"] = protein_need_per_lean_kg_active
         data_frame["protein_need_per_lean_kg_very_active"] = protein_need_per_lean_kg_very_active
        #protein_per_kg_moderate
         protein_per_kg_moderate=  weight_kg * 1.2
         protein_per_kg_max= weight_kg * 2.0
         protein_per_kg_min= weight_kg * 0.8
         data_frame["protein_per_kg_min"] = protein_per_kg_min
         data_frame["protein_per_kg_max"] = protein_per_kg_max
         data_frame["protein_per_kg_moderate"] = protein_per_kg_moderate
        
        #activity_protein_multiplier# activity_protein_multiplier

         if Activity_level == "sedentary":
          activity_protein_multiplier = 1.0
         elif Activity_level == "lightly_active":
          activity_protein_multiplier = 1.2
         elif Activity_level == "moderately_active":
          activity_protein_multiplier = 1.4
         elif Activity_level == "very_active":
          activity_protein_multiplier = 1.6
         elif Activity_level == "extra_active":
          activity_protein_multiplier = 1.8

         data_frame["activity_protein_multiplier"] = activity_protein_multiplier
        
         #adjusted_protein_need
        
         adjusted_protein_need = protein_per_kg_moderate * activity_protein_multiplier

         data_frame["adjusted_protein_need"] = adjusted_protein_need
        
        #protein_for_age_group
         if Age <= 18:
          protein_for_age_group = weight_kg * 1.2
         elif Age <= 50:
          protein_for_age_group = weight_kg * 1.0
         else:
          protein_for_age_group = weight_kg * 1.2

         data_frame["protein_for_age_group"] = protein_for_age_group
       
        #gender_protein_base
         if Gender == "Male":
          gender_protein_base = weight_kg * 1.0
         else:
          gender_protein_base = weight_kg * 0.9

         data_frame["gender_protein_base"] = gender_protein_base
        
        #protein_gender_adjusted
         if Gender == "Male":
          protein_gender_adjusted = adjusted_protein_need * 1.0
         else:
          protein_gender_adjusted = adjusted_protein_need * 0.9

         data_frame["protein_gender_adjusted"] = protein_gender_adjusted
        
        #purpose_protein_multiplier
        
         if purpose == "weight_loss":
          purpose_protein_multiplier = 1.1
         elif purpose == "maintain":
          purpose_protein_multiplier = 1.0
         elif purpose == "weight_gain":
          purpose_protein_multiplier = 1.2
         elif purpose == "muscle_gain":
          purpose_protein_multiplier = 1.3

         data_frame["purpose_protein_multiplier"] = purpose_protein_multiplier
        
        
        #protein_for_purpose
         protein_for_purpose = adjusted_protein_need * purpose_protein_multiplier

         data_frame["protein_for_purpose"] = protein_for_purpose
        
        #muscle_mass_score
         muscle_mass_score = (lean_body_mass_kg / weight_kg) * 100

         data_frame["muscle_mass_score"] = muscle_mass_score
        
        #bmr_per_kg
         bmr_per_kg = bmr / weight_kg

         data_frame["bmr_per_kg"] = bmr_per_kg
        
        #protein_metabolic_need
         protein_metabolic_need = bmr_per_kg * 0.02

         data_frame["protein_metabolic_need"] = protein_metabolic_need
        
        #training_intensity
    

         if Activity_level == "sedentary":
          training_intensity = 1
         elif Activity_level == "lightly_active":
          training_intensity = 2
         elif Activity_level == "moderately_active":
          training_intensity = 3
         elif Activity_level == "very_active":
          training_intensity = 4
         elif Activity_level == "extra_active":
          training_intensity = 5

         data_frame["training_intensity"] = training_intensity
        
        #recovery_protein_need
         recovery_protein_need = adjusted_protein_need * (1 + (training_intensity * 0.1))

         data_frame["recovery_protein_need"] = recovery_protein_need
        
        
       
         
         le_1 = joblib.load('model/activity_level.joblib')
         le_2= joblib.load('model/gender_encoder.joblib')
         le_3= joblib.load('model/purpose_encoding.joblib')
         data_frame['activity_level']=le_1.transform(data_frame['activity_level'])
         data_frame['gender']=le_2.transform(data_frame['gender'])
         data_frame['purpose']=le_3.transform(data_frame['purpose'])
         print('extra cdsjkngjsdgn',data_frame.columns)
         pipeline = joblib.load('model/protein_pipeline.joblib')
         protein_g = pipeline.predict(data_frame)
         print('protein_g',protein_g[0])
         
            
         ProteiDataHist.objects.create(Age=Age,Gender=Gender,Height_cm=Height_cm ,Weight_kg=weight_kg,Activity_Level=Activity_level,Fitness_Goal=purpose,Meals_Per_Day=Meals_dat,FitnessExperience=fitness_experience,protein_g=protein_g[0])
        
         print(ProteiDataHist.objects.count())
        
        
    
         return redirect('history')
        return render(request, 'predict.html') 
  
def history(request):
    records = ProteiDataHist.objects.all().order_by('-id')

    return render(request, 'history.html',{'records':records})  
def report(request):
        # a=  ProteinData.objects.all().values_list('gender',flat=True)
        # b=[]
        # c=[]
        
        # for i in a:
        #     if i=='Male':
        #         b.append(i)
        #     else:
        #         c.append(i)
        # print(len(b))
        # print(len(c))
        # male_data=len(b)
        # female_data=len(c)
        # dict_level={}
        # datra_activity_level=ProteinData.objects.all().values_list('activity_level',flat=True).distinct()
        # for i in datra_activity_level:
        #     data = ProteinData.objects.filter(activity_level=i).values()
        #     data=len(data)
        #     dict_level[i]=data
        # print(data)    
        # print(dict_level)
        # # print(datra_activity_level)
        # #orderby in python
        # # or_by= ProteinData.objects.all().order_by('-protein_g')
        # # print(or_by)
        
        # #changeing dtatatype in database
        # or_by=  ProteinData.objects.annotate(protein_int=Cast('protein_g',IntegerField())).all().order_by('-protein_int').values_list('protein_int')
        # print(or_by)
        # print(type(or_by))
        # dict_protein={}
        # data_protein = ProteinData.objects.all().values_list('protein_g',flat=True).distinct()
        # for i in data_protein:
        #     data = ProteinData.objects.filter(protein_g=i).values()
        #     data=len(data)
        #     dict_protein[i]=data
        # print(dict_protein)
        # print(min(dict))
        
        # conversion = ProteinData.objects.annotate(protein_int=Cast('protein_g',IntegerField())).aggregate(min=Min('protein_int'),max=Max('protein_int'))
             
        low=[]
        mid=[]
        high=[] 
        a= ProteinData.objects.annotate(protein_int=Cast('protein_g',IntegerField()))
       
        for i in a:
            if i.protein_int<=75:
                low.append(i)
            elif i.protein_int>75 and i.protein_int<=175:
                mid.append(i)
            else:
                high.append(i)
        counta = len(low)
        countb = len(mid)
        countc  = len(high)
        
        pur_dict ={}
        
        b = ProteinData.objects.all().values_list('purpose',flat=True).distinct()
        for i in b:
            data = ProteinData.objects.filter(purpose=i).values()
            data=len(data)
            pur_dict[i]=data
        values = list(pur_dict.values())
        labels = list(pur_dict.keys())
        
        print(values)
        print(labels)
        
        return render(request, 'report.html',{'counta':counta,'countb':countb,'countc':countc,'values':values,'labels':labels,'values':values,'labels':labels  }) 
    
    
