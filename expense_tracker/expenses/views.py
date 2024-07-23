from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import Expense
from django.db.models import Sum
from datetime import datetime
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('expense_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('expense_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate monthly expenses
    current_month = datetime.now().month
    monthly_expenses = expenses.filter(date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0
    
    # Example budget for demonstration purposes
    budget = 1000
    remaining_budget = budget - total_expenses
    
    # Calculate expenses by category
    expenses_by_category = expenses.values('category').annotate(total_amount=Sum('amount'))
    
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses,
        'remaining_budget': remaining_budget,
        'expenses_by_category': expenses_by_category
    })
@login_required
def add_expense(request):
    if request.method == 'POST':
        title = request.POST['title']
        amount = request.POST['amount']
        date = request.POST['date']
        description = request.POST.get('description', '')
        category = request.POST.get('category', 'Other')
        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            date=date,
            description=description,
            category= category
        )
        return redirect('expense_list')
    return render(request, 'expenses/expense_form.html')
@login_required
def edit_expense(request, pk):
    expense = Expense.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.date = request.POST['date']
        expense.description = request.POST.get('description', '')
        expense.category = request.POST.get('category', expense.category)
        expense.save()
        return redirect('expense_list')
    return render(request, 'expenses/expense_form.html', {'expense': expense})

@login_required
def delete_expense(request, pk):
    expense = Expense.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})