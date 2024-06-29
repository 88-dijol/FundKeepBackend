from django.shortcuts import render

from datetime import datetime

from rest_framework import viewsets

from rest_framework.response import Response

from rest_framework import status

from rest_framework.views import APIView

from rest_framework import authentication,permissions

from django.contrib.auth.models import User

from django.utils import timezone

from django.db.models import Sum

from api.serializers import UserSerializer,ExpenseSerializer,Incomeserializer

from api.models import Expense,Income

from api.permissions import OwnerOnly

# Create your views here.



class SignUpView(viewsets.ViewSet):

    def create(self,request,*args,**kwargs):

        serializer=UserSerializer(data=request.data)    #deserialization

        if serializer.is_valid():

            serializer.save()  #save aakumbo eth serializerill poyi def create method vilikyum athilthe

            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        
        else:

            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class ExpenseViewSet(viewsets.ModelViewSet):

    queryset=Expense.objects.all()

    serializer_class=ExpenseSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]


    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)      

    def list(self,request,*args,**kwargs):
      

        qs=Expense.objects.filter(owner=request.user)

        # request.query_params==is a dict{}  {"month":4}
        # http://127.0.0.1:8000/api/expenses/?year=2023&month=4

        if 'month' in request.query_params:    
          
            month= request.query_params.get('month')

            qs=qs.filter(created_date__month=month)

        if "year" in request.query_params:

            year=request.query_params.get('year')

            qs=qs.filter(created_date__year=year)

         # suppose oru category =food koduthu appo ethil olla ella expenseum kanikyanam

        if 'category' in request.query_params:

            category=request.query_params.get('category')

            qs=qs.filter(category=category)

        if 'priority' in request.query_params:

            priority=request.query_params.get('priority')

            qs=qs.filter(priority=priority)



       #query parameterill onnum pass cheythillegil ,aa monthille motham expense list cheyanam
        if len(request.query_params.keys())==0:

            current_month=timezone.now().month

            current_year=timezone.now().year

            qs=qs.filter(created_date__month=current_month,created_date__year=current_year)


        serializer=ExpenseSerializer(qs,many=True)

        return Response(data=serializer.data)



#here we are using api view because here we are not performing any srud operation here we are only doing processing the data from the model and the only neede data is got filtered 
class ExpenseSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        print(request.query_params)

        #considering the date from to other date

        if "start_date" in request.query_params and "end_date" in request.query_params:

            # startdate end date extract cheyth eduth ath string aayittan kitta aa stringinne pythonte datellot aaki
            # stringinne datellot mattan strptime enna method call aaki..parameters of strptime is string and format

            start_date=datetime.strptime(request.query_params.get("start_date"),"%Y-%m-%d").date()

            end_date=datetime.strptime(request.query_params.get("end_date"),"%Y-%m-%d").date()

            all_expenses=Expense.objects.filter(owner=request.user,created_date__range=(start_date,end_date))

        # else casell namma month year onnum koduthillegil current monthile kanikyanam

        else:

            current_month=timezone.now().month

            current_year=timezone.now().year

            all_expenses=Expense.objects.filter(

                                owner=request.user,
                                created_date__month=current_month,
                                created_date__year=current_year
 
            )

        #aggregate(total=Sum("amount"))=={} nte ullil value return cheyum,['total']  --egane kodutha eth just aa total mathram return cheyollu

        total_expense=all_expenses.values("amount").aggregate(total=Sum("amount"))['total']   #{}

        category_summary=all_expenses.values("category").annotate(total=Sum("amount")).order_by("-total")    #.order_by("-total") sorting the amount in descending order high to l

        # print(category_summary)

        priority_summary=all_expenses.values("priority").annotate(total=Sum("amount")).order_by("-total")


        data={

            "expense_total":total_expense,

            "category_summary":category_summary,

            "priority_summary":priority_summary
        }

        return Response(data=data)


# =========================================================================
# income

class IncomeViewSet(viewsets.ModelViewSet):

    queryset=Income.objects.all()

    serializer_class=Incomeserializer

    # eth work cheyanegil user userinte credentials pass cheyanam so namma authentication permissionum set cheyanam

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]


    #  while we are saving all details their is a field owner which is not null in model but here it becomes null when we are not giving the values to owner`..so what we need to do is to give value while saving`
    # in createmodemixin-->create method-->perform_create where serializer is saving

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)    #owner who is sending the token   


    # if we are listing all incomes...yeth usernte token aan koduthe aa aalude mathram incomes list cheyan 
    # padollu allathe veroralude tokenill bakhi ellardeyum paadilla for that

    def list(self,request,*args,**kwargs):

        qs=Income.objects.filter(owner= request.user)

        if 'month' in request.query_params:    
          
            month= request.query_params.get('month')

            qs=qs.filter(created_date__month=month)

        if "year" in request.query_params:

            year=request.query_params.get('year')

            qs=qs.filter(created_date__year=year)

         # suppose oru category =food koduthu appo ethil olla ella expenseum kanikyanam

        if 'category' in request.query_params:

            category=request.query_params.get('category')

            qs=qs.filter(category=category)



       #query parameterill onnum pass cheythillegil ,aa monthille motham expense list cheyanam
        if len(request.query_params.keys())==0:

            current_month=timezone.now().month

            current_year=timezone.now().year

            qs=qs.filter(created_date__month=current_month,created_date__year=current_year)


        serializer=Incomeserializer(qs,many=True)

        return Response(data=serializer.data)
