from django.shortcuts import render, get_object_or_404
from .models import Book
from django.db.models import Q
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def search(request):
    query = request.GET.get("q", "")

    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query)
    )

    return render(request, "books.html", {
        "books": books,
        "query": query,
    })


def home(request):
    query = request.GET.get("q", "")

    books = Book.objects.all()[5:]

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    return render(request, "home.html", {
        "books": books,
    })



def read_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Read HTML file as bytes
    with book.html.open("rb") as file:
        raw_content = file.read()

    # Try UTF-8 first, then Windows encoding
    try:
        html = raw_content.decode("utf-8")
    except UnicodeDecodeError:
        html = raw_content.decode("cp1252", errors="replace")

    soup = BeautifulSoup(html, "html.parser")

    # Get only the body
    body = soup.body

    if body:
        content = body.decode_contents()
    else:
        content = str(soup)

    # Remove things that should not run inside EasyBooks
    content_soup = BeautifulSoup(content, "html.parser")

    for tag in content_soup.find_all([
        "script",
        "iframe",
        "object",
        "embed",
        "form"
    ]):
        tag.decompose()

    # Give images a path relative to the uploaded HTML file
    for img in content_soup.find_all("img"):

        src = img.get("src")

        if src:
            img["src"] = urljoin(
                request.build_absolute_uri(
                    book.html.url
                ),
                src
            )

    content = content_soup.decode_contents()

    return render(
        request,
        "reader.html",
        {
            "book": book,
            "content": content,
        }
    )