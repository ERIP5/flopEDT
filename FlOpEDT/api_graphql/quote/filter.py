from django_filters import FilterSet
from quote.models import Quote

class QuoteFilter(FilterSet):
    class Meta:
        model = Quote
        fields = {
            'quote' : ['icontains', 'istartswith'],
            'last_name' : ['icontains', 'istartswith'],
            'for_name' : ['icontains', 'istartswith'],
            'nick_name' : ['icontains', 'istartswith'],
            'desc_author' : ['icontains', 'istartswith'],
            'date' : ['icontains', 'istartswith'],
            'header' : ['icontains', 'istartswith'],
            'quote_type__name' :['icontains', 'istartswith'],
            'quote_type__abbrev' :['icontains', 'istartswith'],
            'positive_votes' : ['exact'],
            'negative_votes' : ['exact'],
            'id_acc' : ['exact'],
            'status' : ['icontains', 'istartswith']
        }