from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import list, detail, edit
from django.utils import timezone
from django.urls import reverse_lazy

from .models import Person
from .forms import PersonForm


@login_required
def persons_list(request):
    persons = Person.objects.all()
    return render(request, 'person.html', {'persons': persons})


@login_required
def persons_new(request):
    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})



class PersonList(list.ListView):
    model = Person

class PersonDetail(detail.DetailView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data();
        context["now"] = timezone.now()
        return context

class PersonCreate(edit.CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', "salary", "bio", "photo"]
    success_url = "/clientes/person_list"

class PersonUpdate(edit.UpdateView):
        model = Person
        fields = ['first_name', 'last_name', 'age', "salary", "bio", "photo"]
        #success_url = reverse_lazy("person_list_cbv")

        def get_success_url(self):
            return reverse_lazy("person_list_cbv")

class PersonDelete(edit.DeleteView):
    model = Person
    success_url = "/clientes/person_list"

