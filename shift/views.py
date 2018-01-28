from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView


from shift.models import Shift, Locker, Manager, Marketer, Expenses
from datetime import datetime
from datetime import timedelta
from shift.forms import LeadMarketer_SignUpForm, Marketer_SignUpForm, Expense_report


# Create your views here.
def shift_listView(request):
    template_name = 'shifts/shifts_list.html'
    queryset = Shift.objects.all()

    # Query all available shifts by week day, 2 = Mon, 3 = Tue etc...
    queryset_monday = Shift.objects.filter(time__week_day=2)
    queryset_tuesday = Shift.objects.filter(time__week_day=3)
    queryset_wednesday = Shift.objects.filter(time__week_day=4)
    queryset_thursday = Shift.objects.filter(time__week_day=5)
    queryset_friday = Shift.objects.filter(time__week_day=6)

    context = {
        "object_list": queryset,
        'monday_shifts': queryset_monday,
        'tuesday_shifts': queryset_tuesday,
        'wednesday_shifts': queryset_wednesday,
        'thursday_shifts': queryset_thursday,
        'friday_shifts': queryset_friday,
    }
    return render(request, template_name, context)

def user_listView(request):
    template_name = 'shifts/users.html'
    queryset_marketers = Marketer.objects.all()
    queryset_managers = Manager.objects.all()
    print(queryset_managers)

    context = {
        "marketers": queryset_marketers,
        'managers': queryset_managers,
    }
    return render(request, template_name, context)

def expenses(request):
    template_name = 'shifts/expenses.html'
    errors = None
    instance = get_object_or_404(Expenses)
    form = Expense_report(request.POST or None, instance=instance)
    context = {

    }

    if form.is_valid():
        form.save(commit=True)
        return HttpResponseRedirect('/expenses/')

    if form.errors:
        errors = form.errors
        print(errors)

    return render(request, template_name, context)

def leadMarketer_SignUp(request, pk):
    template_name = 'shifts/shift_signup.html'
    errors = None

    instance = get_object_or_404(Shift, id=pk)
    form = LeadMarketer_SignUpForm(request.POST or None, instance=instance)

    # Match the authenticated user with the Marketer
    marketer = Marketer.objects.filter(user = request.user).first()

    if form.is_valid():
        instance.lead_marketer = marketer
        form.save(commit=True)
        return HttpResponseRedirect('/shifts/'+pk)

    if form.errors:
        errors = form.errors
        print(errors)

    context = {
        'form': form,
        'errors': errors
    }

    return render(request, template_name, context)

def marketer_SignUp(request, pk):
    template_name = 'shifts/shift_signup.html'
    errors = None

    instance = get_object_or_404(Shift, id=pk)
    form = Marketer_SignUpForm(request.POST or None, instance=instance)

    # Match the authenticated user with the Marketer
    get_marketer = Marketer.objects.filter(user=request.user).first()
        #Marketer.objects.filter(user = request.user)

    if form.is_valid():
        #marketer = instance.objects.create(marketer=get_marketer)
        instance.marketers.add(get_marketer)
        form.save()
        return HttpResponseRedirect('/shifts/'+pk)

    if form.errors:
        errors = form.errors
        print(errors)

    context = {
        'form': form,
        'errors': errors
    }

    return render(request, template_name, context)

class ShiftDetailView(DetailView):
    template_name = 'shifts/shift_details.html'
    endTime = 0

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Shift.objects.all())
        self.endTime = self.object.time + timedelta(minutes=35)
        return super(ShiftDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ShiftDetailView, self).get_context_data(**kwargs)
        print(context)
        context['end_time'] = self.endTime
        return context

    def get_queryset(self):
        queryset = Shift.objects.all()
        return queryset

class MyShiftsView(ListView):
    template_name = 'shifts/my_shifts.html'

    current_user = None
    queryset = None

    def get(self, request, *args, **kwargs):
        self.current_user = request.user
        return super(MyShiftsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        print(self.kwargs)
        get_marketer = Marketer.objects.filter(user=self.current_user).first()
        self.queryset = Shift.objects.filter(
            Q(lead_marketer=get_marketer)
        )

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(MyShiftsView, self).get_context_data(**kwargs)
        print(context)
        context['user_data'] = self.queryset
        return context
