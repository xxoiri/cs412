# voter_analytics/views.py
# Amy Ho, aho@bu.edu

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q, Count
import plotly.graph_objs as go
from plotly.offline import plot

class VotersListView(ListView):
    '''View to display voter information.'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100 # list 100 per page

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.apply_filters(qs)
        return qs.order_by('last_name', 'first_name')

    def apply_filters(self, qs):
        '''Apply filters to queryset - reusable for both list and graph views'''
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        min_score = self.request.GET.get('min_score')
        elections = self.request.GET.getlist('elections')
        
        if party:
            qs = qs.filter(party_affiliation=party)
        
        if min_year:
            qs = qs.filter(doB__year__gte=min_year)
        
        if max_year:
            qs = qs.filter(doB__year__lte=max_year)
        
        if min_score:
            qs = qs.filter(voter_score__gte=min_score)
        
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
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = range(1920, 2021)
        context['scores'] = range(0, 6)
        return context

class VoterDetailView(DetailView):
    '''View to display detailed information for a single voter.'''
    
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

def Search_View(request):
    '''View to display the search form.'''
    context = {
        'years': range(1920, 2021),
        'scores': range(0, 6)
    }
    return render(request, 'voter_analytics/search.html', context)

class GraphsView(ListView):
    '''View to display graphs of voter data.'''
    
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.apply_filters(qs)
        return qs

    def apply_filters(self, qs):
        '''Apply filters to queryset - reusable for both list and graph views'''
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        min_score = self.request.GET.get('min_score')
        elections = self.request.GET.getlist('elections')
        
        if party:
            qs = qs.filter(party_affiliation=party)
        
        if min_year:
            qs = qs.filter(doB__year__gte=min_year)
        
        if max_year:
            qs = qs.filter(doB__year__lte=max_year)
        
        if min_score:
            qs = qs.filter(voter_score__gte=min_score)
        
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
        
        return qs

    def get_context_data(self, **kwargs):
        '''
        Provide context variables for use in template
        '''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        
        # Get filtered queryset
        filtered_voters = self.get_queryset()
        
        # Generate graphs
        context['birth_year_histogram'] = self.create_birth_year_histogram(filtered_voters)
        context['party_pie_chart'] = self.create_party_pie_chart(filtered_voters)
        context['election_participation_histogram'] = self.create_election_participation_histogram(filtered_voters)
        
        # Add filter options to context
        context['years'] = range(1920, 2021)
        context['scores'] = range(0, 6)

        context['selected_elections'] = self.request.GET.getlist('elections')
        
        return context

    def create_birth_year_histogram(self, voters):
        '''Create histogram of voters by birth year'''
        # Extract birth years from the filtered voters
        birth_years = list(voters.values_list('doB__year', flat=True))
        
        # Create histogram
        fig = go.Histogram(x=birth_years, nbinsx=50)
        title_text = "Distribution of Voters by Birth Year"
        
        # Obtain the graph as an HTML div
        graph_div = plot(
            {"data": [fig], "layout_title_text": title_text},
            auto_open=False,
            output_type="div"
        )
        
        return graph_div

    def create_party_pie_chart(self, voters):
        '''Create pie chart of voters by party affiliation'''
        # Count voters by party affiliation
        party_counts = voters.values('party_affiliation').annotate(count=Count('id'))
        
        # Prepare data for pie chart
        parties = []
        counts = []
        for item in party_counts:
            parties.append(item['party_affiliation'])
            counts.append(item['count'])
        
        # Create pie chart
        fig = go.Pie(labels=parties, values=counts)
        title_text = "Distribution of Voters by Party Affiliation"
        
        # Obtain the graph as an HTML div
        graph_div = plot(
            {"data": [fig], "layout_title_text": title_text},
            auto_open=False,
            output_type="div"
        )
        
        return graph_div

    def create_election_participation_histogram(self, voters):
        '''Create histogram of election participation'''
        print(f"Total voters in query: {voters.count()}")
        
        # Debug: Check individual election counts
        v20state_count = voters.filter(v20state=True).count()
        v21town_count = voters.filter(v21town=True).count()
        v21primary_count = voters.filter(v21primary=True).count()
        v22general_count = voters.filter(v22general=True).count()
        v23town_count = voters.filter(v23town=True).count()
        
        print(f"Election counts - v20state: {v20state_count}, v21town: {v21town_count}, v21primary: {v21primary_count}, v22general: {v22general_count}, v23town: {v23town_count}")
        
        # Prepare data for bar chart
        election_names = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        participation_counts = [
            v20state_count,
            v21town_count,
            v21primary_count,
            v22general_count,
            v23town_count
        ]
        
        print(f"Participation counts: {participation_counts}")
        
        # Create bar chart
        fig = go.Bar(
            x=election_names, 
            y=participation_counts,
            marker_color='lightblue'
        )
        
        layout = go.Layout(
            title="Election Participation Distribution",
            xaxis_title="Election",
            yaxis_title="Number of Participants",
            showlegend=False
        )
        
        # Obtain the graph as an HTML div
        graph_div = plot(
            {"data": [fig], "layout": layout},
            auto_open=False,
            output_type="div"
        )
        
        return graph_div