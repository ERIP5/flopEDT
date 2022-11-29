from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from quote.models import Quote, QuoteType
from lib import *



@pytest.fixture
def quote_type1(db) -> QuoteType:
    return QuoteType.objects.create(name="drole", abbrev="DR")

@pytest.fixture
def quote_type2(db) -> QuoteType:
    return QuoteType.objects.create(name="serieux", abbrev="SE")


@pytest.fixture
def quote1(db, quote_type1:QuoteType) -> Quote:
    return Quote.objects.create(quote="Si la connerie se mesurait, tu servirais de metre-etalon. Tu serais a Sevres.", date="20 juillet 2020", quote_type = quote_type1)

@pytest.fixture
def quote2(db, quote_type2:QuoteType) -> Quote:
    return Quote.objects.create(quote="Trop gesticuler mene au ridicule.", date="16 fevrier 1968", quote_type = quote_type2)

def test_quote(client_query,
                quote1 : Quote,
                quote2 : Quote):
    query='''
        query {
            quotes {
                edges {
                    node {
                        id
                        quote
                        date
                        quoteType{
                            name
                            abbrev
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "quotes")
    data = get_data(res)
    assert quote1.quote in data["quote"]
    assert quote1.date in data["date"]
    assert quote1.quote_type.name in data["name"]
    assert quote1.quote_type.abbrev in data["abbrev"]
    assert quote2.quote in data["quote"]
    assert quote2.date in data["date"]
    assert quote2.quote_type.name in data["name"]
    assert quote2.quote_type.abbrev in data["abbrev"]

def test_quote_filter(client_query,
                quote2 : Quote):
    query='''
        query {
            quotes (date_Istartswith : \"16\") {
                edges {
                    node {
                        id
                        quote
                        date
                        quoteType {
                            name
                            abbrev
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "quotes")
    data = get_data(res)
    assert quote2.quote in data["quote"]
    assert quote2.date in data["date"]
    assert quote2.quote_type.name in data["name"]
    assert quote2.quote_type.abbrev in data["abbrev"]
