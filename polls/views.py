from polls.forms import BookingsForm
from django.shortcuts import render
from django.views import generic
from .models import Bookings
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
import datetime
from datetime import timedelta
from django.db.models.functions import Cast
from django.db.models.fields import DateField
import plotly.graph_objects as go
from django.utils import timezone

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('polls:index')

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_message = "Your profile was created successfully"
    success_url = reverse_lazy('polls:index')

class IndexView(generic.ListView):    
    template_name = 'polls/index.html'
    
    def get_queryset(self):
        return 


def bookings(request):
    if request.method == "POST":
        form = BookingsForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            print("Error ", form.errors)
    form = BookingsForm(initial={"name":request.user.username, "stats": request.user.profile.status})
    al= list(Bookings.objects.values_list("date_time", flat=True))
    al = list(dict.fromkeys(al))
    now = timezone.now()
    al = [als for als in al if als + timedelta(days = 1) > now]
    al.sort()
    fl = []
    for bl in al:
        fl.append([list(Bookings.objects.filter(date_time=bl).filter(stats='Premium').values_list('name', flat=True)) + list(Bookings.objects.filter(date_time=bl).filter(stats='Normal').values_list('name', flat=True))] + [str(bl.strftime("%d/%m/%Y, %H:%M:%S"))])
    nfl = []
    for x in fl:
        nfl.append([x[1]] + x[0][0:4])
    
    return render(request, 'polls/bookings.html', {'form':form, 'nfl':nfl})

def Profile(request):
    user = request.user
    try:
        if request.method == "POST":
            data= request.POST
            user.username = data.get("username")
            user.first_name = data.get("firstname")
            user.last_name = data.get("lastname")
            user.profile.gender = data.get("gender")
            user.profile.age = data.get("age")
            user.profile.save()
            user.save()
    except:
        pass
    al= list(Bookings.objects.values_list("date_time", flat=True))
    al = list(dict.fromkeys(al))
    now = timezone.now()
    al = [als for als in al if als + timedelta(days=1) > now]
    al.sort()
    fl = []
    for bl in al:
        fl.append([list(Bookings.objects.filter(date_time=bl).filter(stats='Premium').values_list('name', flat=True)) + list(Bookings.objects.filter(date_time=bl).filter(stats='Normal').values_list('name', flat=True))] + [str(bl.strftime("%d/%m/%Y, %H:%M:%S"))])
    nfl = []
    for x in fl:
        nfl.append([x[1]] + x[0][0:4])
    usern = request.user.username
    ul = []
    for jk in nfl:
        if usern in jk:
            ul.append(jk[0])
    return render(request, 'polls/profile.html', {'user': user, "ds": ul})

def check_admin(user):
   return user.is_superuser

@user_passes_test(check_admin)
def seebs(request):
    df = list(Bookings.objects.annotate(date_only=Cast('date_time', DateField())).values_list('date_time', flat=True))
    df = [i.date() for i in df]
    year = datetime.datetime.now().year
    df.append(datetime.date(year, 12, 31))
    df.insert(0, datetime.date(year, 1, 1))
    
    ls = []
    for i in df:
        if i not in ls:
            ls.append(i)
    counterl = []
    for x in ls:
        counter = df.count(x)
        if counter > 4:
            counter = 4
        counterl.append(counter)
        counter = 0
    counterl[0] = counterl[0] - 1
    counterl[-1] = counterl[-1] - 1

    for g in ls:
        g = g.strftime('%d/%m/%Y')
    ls = sorted(ls)

    ls = [str(x) for x in ls]
    diff = []
    for h in ls:
        if h == ls[-1]:
            next = h
        else:
            next = ls[ls.index(h)+1]
        differ = datetime.datetime.strptime(str(next), "%Y-%m-%d").date() - datetime.datetime.strptime(str(h), "%Y-%m-%d").date()
        diff.append(differ.days)

    del diff[-1]
    diff = [int(u) for u in diff]
    diff = [p-1 for p in diff]

    temp = counterl
    y = 1

    for x in range(len(diff)):
        for x in range(diff[x]):
            temp.insert(y,0)
            y += 1
        y += 1

    year = datetime.datetime.now().year

    d1 = datetime.date(year, 1, 1)
    d2 = datetime.date(year, 12, 31)

    delta = d2 - d1

    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days+1)]
    weekdays_in_year = [i.weekday() for i in dates_in_year] 
    weeknumber_of_dates = [i.strftime("%Gww%V")[2:] for i in dates_in_year] 
    text = [str(i) for i in dates_in_year] 

    colorscale= [[0, '#808080'], [0.25, '#00FF00'], [0.50, '#FFFF00'], [0.75, '#FFA500'], [1, '#ff0000']]
    
    data = [
        go.Heatmap(
        x = weeknumber_of_dates,
        y = weekdays_in_year,
        z = temp,
        text=text,
        hoverinfo='text',
        xgap=3, # this
        ygap=3, # and this is used to make the grid-like apperance
        showscale=False,
        colorscale=colorscale
    )
    ]
    layout = go.Layout(
        title= 'Gym Bookings Heatmap',
        height=280,
        yaxis=dict(
        showline = False, showgrid = False, zeroline = False,
        tickmode='array',
        ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        tickvals=[0,1,2,3,4,5,6],
        ),
        xaxis=dict(
        showline = False, showgrid = False, zeroline = False,
        ),
        font={'size':10, 'color':'#9e9e9e'},
        plot_bgcolor=('#fff'),
        margin = dict(t=40),
    )

    fig = go.Figure(data=data, layout=layout)
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, 'polls/seebs.html', context)


