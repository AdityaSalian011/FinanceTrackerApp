import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from expense.models import Expense
from income.models import Income
from budget.models import Budget
from expense.forms import ExpenseForm
from income.forms import IncomeForm
from budget.forms import BudgetForm, RegistrationForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def index(request):
    return render(request, "websites/index.html")

def info(request):
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    budgets = Budget.objects.all()
    return render(request, "websites/info.html", {"expenses": expenses, "incomes": incomes, "budgets": budgets})

@login_required
def expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            xpense = form.save(commit=False)
            xpense.user = request.user
            xpense.save()    
            return redirect("info")
        else:
            err_message = "requires all values"
            return render(request, "expense/expense.html", {"err_message": 
            err_message})
    else:
        form = ExpenseForm()
    return render(request, "expense/expense.html", {"form": form})

@login_required           
def income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            ncome = form.save(commit=False)
            ncome.user = request.user
            ncome.save()
            return redirect("info")
        else:
            err_message = "requires all values"
            return render(request, "income/income.html", {"err_message": err_message})
    else:
        form = IncomeForm()
    return render(request, "income/income.html", {"form": form})

@login_required
def edit_expense(request, pk):
    instance = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=instance)
        if form.is_valid():
            xpense = form.save(commit=False)
            xpense.user = request.user
            xpense.save()
            return redirect("info")
    else:
        form = ExpenseForm(instance=instance)
    return render(request, "expense/edit_expense.html", {"form": form})

@login_required
def edit_income(request, pk):
    instance = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=instance)
        if form.is_valid():
            ncome = form.save(commit=False)
            ncome.user = request.user
            ncome.save()
            return redirect("info")
    else:
        form = IncomeForm(instance=instance)
    return render(request, "income/edit_income.html", {"form": form})

@login_required
def delete_expense(request, pk):
    delete = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        delete.delete()
        return redirect("info")
    return render(request, "expense/delete_expense.html", {"form": delete})

@login_required
def delete_income(request, pk):
    delete = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        delete.delete()
        return redirect("info")
    return render(request, "income/delete_income.html", {"form": delete})

def expense_chart(request):
    expenses = Expense.objects.all()

    data = [expense_.money for expense_ in expenses]
    keys = [expense_.get_category_display() for expense_ in expenses]

    palette_color = sns.color_palette("bright")

    combined_budgets = []
    combined_categories = []

    for i, key in enumerate(keys):
        if key not in combined_categories:
            combined_categories.append(key)
            total_for_category = data[i]
            indexes_to_remove = []
            for j in range(i + 1, len(keys)):
                if key == keys[j]:
                    total_for_category += data[j]
                    indexes_to_remove.append(j)  
            combined_budgets.append(total_for_category)
        
            for index in reversed(indexes_to_remove):
                del keys[index]
                del data[index]

    plt.pie(data, labels=keys, colors=palette_color, autopct="%.0f%%", startangle= 90)
    plt.legend()

    plot_dir = os.path.join(settings.BASE_DIR, "static")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plot_path = os.path.join(plot_dir, "plot.png")
    plt.savefig(plot_path)
    plt.close()

    return render(request, "expense/expense_chart.html", {"plot_path": "static/plot.png"})
    
def income_chart(request):
    incomes = Income.objects.all()

    data = [income_.money for income_ in incomes]
    keys = [income_.get_category_display() for income_ in incomes]

    palette_color = sns.color_palette("bright")

    combined_budgets = []
    combined_categories = []

    for i, key in enumerate(keys):
        if key not in combined_categories:
            combined_categories.append(key)
            total_for_category = data[i]
            indexes_to_remove = []
            for j in range(i + 1, len(keys)):
                if key == keys[j]:
                    total_for_category += data[j]
                    indexes_to_remove.append(j)  
            combined_budgets.append(total_for_category)
        
            for index in reversed(indexes_to_remove):
                del keys[index]
                del data[index]
                
    plt.pie(data, labels=keys, colors=palette_color, autopct="%.0f%%", startangle= 90)
    plt.legend()

    plot_dir = os.path.join(settings.BASE_DIR, "static")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plot_path = os.path.join(plot_dir, "plot1.png")
    plt.savefig(plot_path)
    plt.close()

    return render(request, "income/income_chart.html", {"plot_path": "static/plot1.png"})

@login_required
def budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            bud = form.save(commit=False)
            bud.user = request.user
            bud.save()
            return redirect("info")
        else:
            err_message = "requires all values"
            return render(request, "budget/budget.html", {"err_message": 
            err_message})
    else:
        form = BudgetForm()
    return render(request, "budget/budget.html", {"form": form})     

def budget_plot(request):
    budgets = Budget.objects.all()
    expenses = Expense.objects.all()

    total_budgets = [budget_.money for budget_ in budgets]
    current_budgets = [expense_.money for expense_ in expenses]

    bud_categories = [budget_.get_category_display() for budget_ in budgets]
    exp_categories = [expense_.get_category_display() for expense_ in expenses]

    combined_budgets = []
    combined_categories = []

    for i, b_cat in enumerate(bud_categories):
        if b_cat not in combined_categories:
            combined_categories.append(b_cat)
            total_for_category = total_budgets[i]
            indexes_to_remove = []
            for j in range(i + 1, len(bud_categories)):
                if b_cat == bud_categories[j]:
                    total_for_category += total_budgets[j]
                    indexes_to_remove.append(j)  
            combined_budgets.append(total_for_category)
        
            for index in reversed(indexes_to_remove):
                del bud_categories[index]
                del total_budgets[index]
            
    spent_budget_list = [0] * len(bud_categories)
    for i,bud_category in enumerate(bud_categories):
        for j,exp_category in enumerate(exp_categories):
            if exp_category == bud_category:
                current_budget = current_budgets[j]
                total_budget = total_budgets[i]
                spent_budget = (current_budget/ total_budget)*100
                spent_budget_list[i] += spent_budget

    for i, spent_budgets in enumerate(spent_budget_list):
        bud_category = bud_categories[i]

        plt.subplot(len(spent_budget_list), 1, i+1)
        plt.subplots_adjust(hspace=0.5)
        if spent_budgets > 80:
            plt.barh(["Budet"], [spent_budgets], color="red")
        else:
            plt.barh(["Budget"], [spent_budgets], color="blue") 

        plt.xlabel(bud_category)       
        plt.xlim([0,100])  

    plot_dir = os.path.join(settings.BASE_DIR, "static")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plot_path = os.path.join(plot_dir, "plot2.png")
    plt.savefig(plot_path)
    plt.close()
    return render(request, "budget/budget_plot.html", {"plot_path": "static/plot2.png"})

def edit_budget(request, pk):
    instance = get_object_or_404(Budget, pk=pk)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("info")
    else:
        form = BudgetForm(instance=instance)
    return render(request, "budget/edit_budget.html", {"form": form})

def delete_budget(request, pk):
    delete = get_object_or_404(Budget, pk=pk)
    if request.method == "POST":
        delete.delete()
        return redirect("info")
    return render(request, "budget/delete_budget.html", {"form": delete})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login
            return redirect("info")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})