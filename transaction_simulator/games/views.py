from django.shortcuts import render, get_object_or_404
from .models import Crisis, Donor, Scheme, Person, Game, Transaction, Turn


# Create your views here.

### CRISIS VIEWS ###

def index(request):
    return HttpResponse("Hello, Dheeraj. You're at the games index.")

def crisis_index(request):

    latest_crisis_list = Crisis.objects.order_by('-pk')
    context = {
        'latest_crisis_list': latest_crisis_list
    }

    return render(
        request,
        'games/crisis/index.html',
        context
    )

def crisis_detail(request, crisis_id):

    crisis = get_object_or_404(Crisis, pk=crisis_id)
    return render(
        request,
        'games/crisis/detail.html/',
        {'crisis': crisis}
    )

### DONOR VIEWS ###

def donor_index(request):

    latest_donor_list = Donor.objects.order_by('-pk')
    context = {'latest_donor_list': latest_donor_list}

    return render(
        request,
        'games/donors/index.html',
        context
    )

def donor_detail(request, donor_id):

    donor = get_object_or_404(Donor, pk=donor_id)
    return render(
        request,
        'games/donors/detail.html/',
        {'donor': donor}
    )

### SCHEME VIEWS ###

def scheme_index(request):

    latest_scheme_list = Scheme.objects.order_by('-pk')
    context = {'latest_scheme_list': latest_scheme_list}

    return render(
        request,
        'games/schemes/index.html',
        context
    )

def scheme_detail(request, scheme_id):

    scheme = get_object_or_404(Scheme, pk=scheme_id)
    return render(
        request,
        'games/schemes/detail.html/',
        {'scheme': scheme}
    )

### PERSON VIEWS ###

def person_index(request):

    latest_person_list = Person.objects.order_by('-pk')
    context = {'latest_person_list' : latest_person_list}

    return render(
        request,
        'games/persons/index.html',
        context
    )

def person_detail(request, person_id):

    person = get_object_or_404(Person, pk=person_id)
    return render(
        request,
        'games/persons/detail.html/',
        {'person': person}
    )

### GAME VIEWS ###

def game_index(request):

    latest_game_list = Game.objects.order_by('-pk')
    context = {'latest_game_list': latest_game_list}

    return render(
        request,
        'games/games/index.html',
        context
    )

def game_detail(request, game_id):

    game = get_object_or_404(Person, pk=game_id)
    return render(
        request,
        'games/games/detail.html/',
        {'game': game}
    )

### TRANSACTION VIEWS ###

def transaction_index(request):

    latest_transaction_index = Transaction.objects.order_by('-pk')
    context = {'latest_transaction_list': latest_transaction_index}

    return render(
        request,
        'games/transactions/index.html'
    )


def tra_detail(request, transaction_id):

    transaction = get_object_or_404(Transaction, pk=transaction_id)
    return render(
        request,
        'games/games/detail.html/',
        {'transaction': transaction}
    )