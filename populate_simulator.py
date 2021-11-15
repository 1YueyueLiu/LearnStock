import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'LearnStock.settings')
                    
import django 
django.setup()
from stock.models import Category,Page

def populate():

    Stock_definition=[
        {'title':'Stock',
        'url':'https://www.investopedia.com/terms/s/stock.asp',
        'views':112,},
        {'title':'Stock Keeping Unit',
        'url':'https://www.investopedia.com/terms/s/stock-keeping-unit-sku.asp',
        'views':12},
        {'title':'Stock Market',
        'url':'https://www.investopedia.com/terms/s/stockmarket.asp',
        'views':20},
        {'title':'Strength, Weakness, Opportunity, and Threat（SWOT）Analysis',
        'url':'https://www.investopedia.com/terms/s/swot.asp',
        'views':16}

    ]
    Growth_stock=[
        {'title':'Top Growth Stocks for November 2021',
        'url':'https://www.investopedia.com/investing/best-growth-stocks/',
        'views':30}
    ]
    Top_stock=[
        {'title':'Top 5 Highest Priced Stocks In America',
        'url':'https://www.investopedia.com/financial-edge/0711/the-highest-priced-stocks-in-america.aspx',
        'views':40},
        {'title':'How Facebook(Meta) makes money',
        'url':'https://www.investopedia.com/ask/answers/120114/how-does-facebook-fb-make-money.asp',
        'views':60}
       
    ]

    Tech_stock=[
        {'title':'The World Wide Web Inventor Thinks Tech Giants Need to Be Broken Up',
        'url':'https://www.investopedia.com/news/world-wide-web-inventor-thinks-tech-giants-need-be-broken/',
        'views':38}
    ]

    Difference_stock=[
        {'title':'Preferred vs. Common Stock: What is the Difference?',
        'url':'https://www.investopedia.com/ask/answers/difference-between-preferred-stock-and-common-stock/',
        'views':29}
    ]
 
    cats = {'Stock Knowledge':{'pages': Stock_definition,'views':150,'likes':115},
            'Growth stock':{'pages': Growth_stock,'views':77,'likes':34},
            'Top stock':{'pages': Top_stock,'views':87,'likes':67},
            'Tech stock':{'pages': Tech_stock,'views':98,'likes':46},
            'Other investment':{'pages': Difference_stock,'views':32,'likes':10}
    }

    for cat,cat_data in cats.items():
        c = add_cat(cat,views=cat_data['views'],likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c,p['title'],p['url'],views=p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f' - {c}:{p}')



def add_page(cat,title,url,views=0):
    p = Page.objects.get_or_create(category=cat,title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name,views=0,likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c



if __name__ == '__main__':
     print('Starting Simulator population script...')
     populate()
