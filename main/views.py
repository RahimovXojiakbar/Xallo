from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, WorkAssignment, Payment
from django.db.models import Sum
from django.utils import timezone

def staff_list(request):
    staff_list = Staff.objects.all().distinct()
    return render(request, 'staff_list.html', {'staff_list': staff_list})

def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    # Faqat is_active=True bo'lgan topshiriqlarni olish
    assignments = staff.assignments.filter(is_active=True)
    # Umumiy haqni hisoblash
    total_money = assignments.aggregate(Sum('money'))['money__sum'] or 0
    # Debugging uchun log qo'shamiz
    print(f"Staff ID: {pk}, Total Money: {total_money}")
    print(f"Active Assignments: {[(a.id, a.work_type, a.quantity, a.money, a.is_active) for a in assignments]}")
    return render(request, 'staff_detail.html', {
        'staff': staff,
        'assignments': assignments,
        'total_money': total_money
    })

def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        try:
            if not name or not position:
                raise ValueError("Barcha maydonlar to'ldirilishi shart")
            Staff.objects.create(name=name, position=position)
            return redirect('staff_list')
        except Exception as e:
            return render(request, 'staff_list.html', {'error': str(e), 'staff_list': Staff.objects.filter(assignments__is_active=True).distinct()})
    return render(request, 'staff_list.html', {'staff_list': Staff.objects.filter(assignments__is_active=True).distinct()})

def edit_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.name = request.POST.get('name')
        staff.position = request.POST.get('position')
        try:
            if not staff.name or not staff.position:
                raise ValueError("Barcha maydonlar to'ldirilishi shart")
            staff.save()
            return redirect('staff_list')
        except Exception as e:
            return render(request, 'staff_list.html', {'error': str(e), 'staff': staff, 'staff_list': Staff.objects.filter(assignments__is_active=True).distinct()})
    return render(request, 'staff_list.html', {'staff': staff, 'staff_list': Staff.objects.filter(assignments__is_active=True).distinct()})

def delete_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'staff_list.html', {'staff': staff, 'staff_list': Staff.objects.filter(assignments__is_active=True).distinct()})

def add_assignment(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        work_type = request.POST.get('work_type')
        quantity = request.POST.get('quantity')
        try:
            work_type = int(work_type)
            quantity = int(quantity)
            if work_type <= 0 or quantity <= 0:
                raise ValueError("Ish turi va soni musbat bo'lishi shart")
            assignment = WorkAssignment.objects.create(staff=staff, work_type=work_type, quantity=quantity)
            print(f"New Assignment: work_type={work_type}, quantity={quantity}, money={assignment.money}")
            return redirect('staff_detail', pk=staff_id)
        except ValueError as e:
            return render(request, 'staff_detail.html', {'error': str(e), 'staff': staff, 'assignments': staff.assignments.filter(is_active=True)})
        except Exception as e:
            return render(request, 'staff_detail.html', {'error': "Noma'lum xato yuz berdi", 'staff': staff, 'assignments': staff.assignments.filter(is_active=True)})
    return render(request, 'staff_detail.html', {'staff': staff, 'assignments': staff.assignments.filter(is_active=True)})

def edit_assignment(request, pk):
    assignment = get_object_or_404(WorkAssignment, pk=pk)
    if request.method == 'POST':
        assignment.work_type = request.POST.get('work_type')
        assignment.quantity = request.POST.get('quantity')
        try:
            if not assignment.work_type or not assignment.quantity:
                raise ValueError("Barcha maydonlar to'ldirilishi shart")
            assignment.save()
            return redirect('staff_detail', pk=assignment.staff.pk)
        except Exception as e:
            return render(request, 'staff_detail.html', {'error': str(e), 'assignment': assignment, 'staff': assignment.staff, 'assignments': assignment.staff.assignments.filter(is_active=True)})
    return render(request, 'staff_detail.html', {'assignment': assignment, 'staff': assignment.staff, 'assignments': assignment.staff.assignments.filter(is_active=True)})

def delete_assignment(request, pk):
    assignment = get_object_or_404(WorkAssignment, pk=pk)
    staff_id = assignment.staff.pk
    if request.method == 'POST':
        assignment.delete()
        return redirect('staff_detail', pk=staff_id)
    return render(request, 'staff_detail.html', {'assignment': assignment, 'staff': assignment.staff, 'assignments': assignment.staff.assignments.filter(is_active=True)})

def pay_money(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        total = WorkAssignment.objects.filter(staff=staff, is_active=True).aggregate(Sum('money'))['money__sum'] or 0
        if total > 0:
            WorkAssignment.objects.filter(staff=staff, is_active=True).update(is_active=False)
            Payment.objects.create(staff=staff, amount=total)
            return render(request, 'staff_detail.html', {'staff': staff, 'assignments': staff.assignments.filter(is_active=True), 'message': f"{total} so'm haq hodimga berildi"})
        return render(request, 'staff_detail.html', {'staff': staff, 'assignments': staff.assignments.filter(is_active=True), 'error': "To'lanadigan haq mavjud emas"})
    return render(request, 'staff_detail.html', {'staff': staff, 'assignments': staff.assignments.filter(is_active=True)})


