from django.shortcuts import render,redirect,get_object_or_404
from .models import Note
from .forms import NoteModelForm
# Create your views here.\

#CRUD

#create view
def create_view(request):
    
    form = NoteModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('list')
    
    context = {
        'form':form
    }
    return render(request,"notepad/create.html",context)

#List View

def list_view(request):
    notes = Note.objects.all()
    context = {
        'objects_list':notes
    }
    return render(request,"notepad/list.html", context)

#Delete view
def delete_view(request,id):
    item_to_delete = Note.objects.filter(pk=id)
    if item_to_delete.exists():
        if request.user == item_to_delete[0].user:
            item_to_delete[0].delete()
    return redirect('list')


#Update View#
def update_view(request,id):
    unique_note = get_object_or_404(Note,id=id)
    form = NoteModelForm(request.POST or None, request.FILES or None, instance=unique_note)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('list')

    context = {
        'form':form
    }
    return render(request, "notepad/create.html", context)