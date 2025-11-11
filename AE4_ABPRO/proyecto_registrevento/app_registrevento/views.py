from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .forms import EventForm, ParticipantForm
from .models import Participant
from .models import Event # Asegúrate de importar Event al inicio

# You can keep a simple index view (project-level urls also define one).
def index(request):
	return render(request, 'index.html')


def create_event(request):
	ParticipantFormSet = formset_factory(ParticipantForm, extra=1)

	if request.method == 'POST':
		event_form = EventForm(request.POST)
		participant_formset = ParticipantFormSet(request.POST, prefix='participants')

		if event_form.is_valid() and participant_formset.is_valid():
			# Server-side: check for duplicate emails among participant forms
			emails = []
			for form in participant_formset.forms:
				cd = form.cleaned_data
				if cd and cd.get('correo'):
					emails.append(cd.get('correo').strip().lower())

			dupes = set([e for e in emails if emails.count(e) > 1])
			if dupes:
				# Attach an error to each form that has a duplicated email
				for form in participant_formset.forms:
					cd = getattr(form, 'cleaned_data', None)
					if cd and cd.get('correo') and cd.get('correo').strip().lower() in dupes:
						form.add_error('correo', 'Correo duplicado entre participantes.')
				# Add user-visible message; will re-render form with errors below
				messages.error(request, 'Hay correos duplicados entre participantes. Corrige los campos marcados.')
			else:
				# No duplicates — save event and participants
				event = event_form.save()
				messages.success(request, 'Evento creado correctamente.')

				# Save participant objects for each filled form
				for pform in participant_formset.cleaned_data:
					if not pform:
						continue
					nombre = pform.get('nombre')
					correo = pform.get('correo')
					if nombre and correo:
						Participant.objects.create(event=event, nombre=nombre, correo=correo)

				return redirect('inicio')
		else:
			# Some validation errors in forms — add a general error message
			messages.error(request, 'Corrige los errores en el formulario.')
	else:
		event_form = EventForm()
		participant_formset = ParticipantFormSet(prefix='participants')

	return render(request, 'event_form.html', {
		'form': event_form,
		'participant_formset': participant_formset,
	})

def event_list(request):
    # 1. Obtener todos los objetos Event de la BD
    # El .order_by('-fecha') es opcional, para mostrar los más nuevos primero
    eventos = Event.objects.all().order_by('-fecha') 

    # 2. Enviar la lista de eventos a la plantilla
    context = {
        'eventos': eventos
    }
    return render(request, 'event_list.html', context)