import collections
import urllib

from django.http import HttpResponse
from django.shortcuts import render


from pymysql import connect

from App.models import Focus


def index(request):

    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='dsci551', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select bookID,title,authors,average_rating,publication_date,publisher from books order by rand() limit 20;")
    books=cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'index.html', {'books': books})


def list(request):

    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='dsci551', charset='utf8')
    cursor = conn.cursor()
    cursor.execute(
        "select bookID,title,authors,average_rating,publication_date,publisher,comment from books join focus on focus.book_id=books.bookID order by bookID;")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'list.html',locals())

def add(request,num):

    book_code = num

    focus = Focus(book_id = book_code)
    focus.save()
    print(focus)
    return HttpResponse("add %s successfully!" % book_code)
def del_focus(request,num):

    book_code = num

    focus = Focus.objects.get(book_id=book_code)
    focus.delete()
    return HttpResponse("delete %s successfully!" % book_code)


def search(request):
    te = request.GET.get('content')
    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='dsci551', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select bookID,title,authors,average_rating,publication_date,publisher from books where title like '% {} %' order by title;".format(te))
    books = cursor.fetchall()
    years = []
    nums = []
    cursor.execute("select Year(str_to_date(publication_date, '%m/%d/%Y')) as y,count(*) from books where title like '% {} %' group by y order by y;".format(te))
    data = cursor.fetchall()
    for item in data:
        years.append(item[0])
        nums.append(item[1])
    cursor.close()
    conn.close()
    return render(request, 'search.html', locals())


def findauthor(request,author):
    d=collections.defaultdict(int)
    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='dsci551', charset='utf8')
    cursor = conn.cursor()
    parse_author = urllib.parse.unquote(author)
    parse_author_set = set(parse_author.split('/'))
    cursor.execute(
        "select bookID,title,authors,average_rating,publication_date,publisher from books where authors='{}';".format(
            parse_author))
    book = cursor.fetchall()
    books = []
    for b in book:
        books.append(b)
    cursor.execute(
        "select Year(str_to_date(publication_date, '%m/%d/%Y')) as y,count(*) from books where authors='{}' group by y order by y;".format(
            parse_author))
    data = cursor.fetchall()
    for item in data:
        year=item[0]
        num=item[1]
        d[year]+=num
    if len(parse_author_set)!=1:
        for pa in parse_author_set:
            cursor.execute(
                "select bookID,title,authors,average_rating,publication_date,publisher from books where authors=%s;",(pa,))
            book_sub = cursor.fetchall()
            for b in book_sub:
                books.append(b)
            cursor.execute(
                "select Year(str_to_date(publication_date, '%m/%d/%Y')) as y,count(*) from books where authors='{}' group by y order by y;".format(
                    pa))
            data = cursor.fetchall()
            for item in data:
                year = item[0]
                num = item[1]
                d[year] += num
    years=[k for k in d.keys()]
    years.sort()
    nums=[d[y] for y in years]
    cursor.close()
    conn.close()
    return render(request, 'search.html', locals())


def findpublisher(request,publisher):
    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='dsci551', charset='utf8')
    cursor = conn.cursor()
    parse_publisher = urllib.parse.unquote(publisher)
    cursor.execute(
        "select bookID,title,authors,average_rating,publication_date,publisher from books where publisher=%s;",
        (parse_publisher,))
    books = cursor.fetchall()
    years = []
    nums = []
    cursor.execute(
        "select Year(str_to_date(publication_date, '%m/%d/%Y')) as y,count(*) from books where publisher='{}' group by y order by y;".format(parse_publisher))
    data = cursor.fetchall()
    for item in data:
        years.append(item[0])
        nums.append(item[1])
    cursor.close()
    conn.close()
    return render(request, 'search.html', locals())