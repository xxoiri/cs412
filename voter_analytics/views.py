# voter_analytics/views.py
# Amy Ho, aho@bu.edu

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q

class VotersListView(ListView):
    '''View to display voter information.'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100  # Show 100 records per page

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        min_score = self.request.GET.get('min_score')
        elections = self.request.GET.getlist('elections')  # For checkboxes
        
        # Apply filters
        if party:
            qs = qs.filter(party_affiliation=party)
        
        if min_year:
            qs = qs.filter(doB__year__gte=min_year)
        
        if max_year:
            qs = qs.filter(doB__year__lte=max_year)
        
        if min_score:
            qs = qs.filter(voter_score__gte=min_score)
        
        # Election filters
        election_filters = Q()
        if 'v20state' in elections:
            election_filters |= Q(v20state=True)
        if 'v21town' in elections:
            election_filters |= Q(v21town=True)
        if 'v21primary' in elections:
            election_filters |= Q(v21primary=True)
        if 'v22general' in elections:
            election_filters |= Q(v22general=True)
        if 'v23town' in elections:
            election_filters |= Q(v23town=True)
        
        if elections:
            qs = qs.filter(election_filters)
        
        return qs.order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate year range for dropdowns (e.g., 1920-2020)
        context['years'] = range(1920, 2021)
        context['scores'] = range(0, 6)  # Voter scores from 0 to 5
        return context

class VoterDetailView(DetailView):
    '''View to display detailed information for a single voter.'''
    
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

def search_view(request):
    '''View to display the search form.'''
    context = {
        'years': range(1920, 2021),
        'scores': range(0, 6)
    }
    return render(request, 'voter_analytics/search.html', context)