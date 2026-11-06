import math

from django.db.models import Count, Q
from django.shortcuts import render

from .models import DictionaryEntry


CATEGORY_DISPLAY = {
    'green': 'Aynan berilganlar',
    'yellow': 'Variantdoshlari',
    'red': 'Lug‘atda uchramaydi',
    'purple': 'Okkazional iboralar',
}


def _page_window(current, total, span=2):
    """Build a compact page list like [1, '...', 4, 5, 6, '...', 147]."""
    pages = []
    start = max(1, current - span)
    end = min(total, current + span)

    if start > 1:
        pages.append(1)
        if start > 2:
            pages.append('...')

    pages.extend(range(start, end + 1))

    if end < total:
        if end < total - 1:
            pages.append('...')
        pages.append(total)

    return pages


def _entry_to_dict(entry):
    return {
        'title': entry.title,
        'category': entry.category,
        'category_label': CATEGORY_DISPLAY.get(entry.category, entry.category),
        'meaning': entry.meaning or 'Ma’no kiritilmagan.',
        'layer': 'Axloqiy-maʼnaviy',
        'pages': entry.pages,
        'notes': entry.notes,
        'example': entry.example,
    }


def index(request):
    counts = DictionaryEntry.objects.values('category').annotate(total=Count('id'))
    category_totals = {item['category']: item['total'] for item in counts}

    uzual_total = category_totals.get('green', 0) + category_totals.get('yellow', 0) + category_totals.get('red', 0)

    stats = [
        {'icon': 'layers', 'value': f"{DictionaryEntry.objects.count():,}".replace(',', ' '), 'label': 'Jami frazeologik birlik'},
        {'icon': 'book', 'value': f"{uzual_total:,}".replace(',', ' '), 'label': 'Uzual iboralar', 'note': 'uzual'},
        {'icon': 'book', 'value': f"{category_totals.get('green', 0):,}".replace(',', ' '), 'label': 'Lug‘atda aynan berilgan', 'note': 'green'},
        {'icon': 'feather', 'value': f"{category_totals.get('yellow', 0):,}".replace(',', ' '), 'label': 'Lug‘atda variantdoshi berilgan', 'note': 'yellow'},
        {'icon': 'book-open', 'value': f"{category_totals.get('red', 0):,}".replace(',', ' '), 'label': 'Lug‘atda uchramaydigan', 'note': 'red'},
        {'icon': 'refresh', 'value': f"{category_totals.get('purple', 0):,}".replace(',', ' '), 'label': 'Okkazional iboralar', 'note': 'purple'},
    ]
    return render(request, 'index.html', {'stats': stats})


def dictionary(request):
    search_query = (request.GET.get('q') or '').strip()
    category = request.GET.get('category', 'all')
    if category not in ('all', 'green', 'yellow', 'red', 'purple'):
        category = 'all'

    page_size_value = request.GET.get('page_size', '25')

    if page_size_value == 'all':
        page_size = 'all'
    else:
        try:
            page_size = int(page_size_value)
        except (TypeError, ValueError):
            page_size = 25

        if page_size not in (25, 50, 100, 500):
            page_size = 25

    entries = DictionaryEntry.objects.order_by('title')
    if category != 'all':
        entries = entries.filter(category=category)
    if search_query:
        entries = entries.filter(Q(title__icontains=search_query) | Q(meaning__icontains=search_query))

    total_matching = entries.count()

    if page_size == 'all':
        total_pages = 1
        current_page = 1
        entries = entries
    else:
        total_pages = max(1, math.ceil(total_matching / page_size))
        try:
            current_page = int(request.GET.get('page', '1'))
        except (TypeError, ValueError):
            current_page = 1
        current_page = max(1, min(current_page, total_pages))
        start = (current_page - 1) * page_size
        entries = entries[start:start + page_size]

    phrases = [_entry_to_dict(entry) for entry in entries]

    counts = DictionaryEntry.objects.values('category').annotate(total=Count('id'))
    category_totals = {item['category']: item['total'] for item in counts}
    category_totals['all'] = DictionaryEntry.objects.count()
    category_totals_display = {key: f"{value:,}".replace(',', ' ') for key, value in category_totals.items()}

    return render(request, 'dictionary.html', {
        'phrases': phrases,
        'current_page_size': str(page_size),
        'search_query': search_query,
        'current_category': category,
        'category_totals': category_totals_display,
        'total_matching': f"{total_matching:,}".replace(',', ' '),
        'current_page': current_page,
        'total_pages': total_pages,
        'page_numbers': _page_window(current_page, total_pages),
    })


def phrase_detail(request):
    title = (request.GET.get('title') or '').strip()
    entry = DictionaryEntry.objects.filter(title=title).first() if title else None

    if entry is None:
        entry = DictionaryEntry.objects.order_by('title').first()

    related = []
    if entry is not None:
        related = list(
            DictionaryEntry.objects.filter(category=entry.category)
            .exclude(pk=entry.pk)
            .order_by('title')[:5]
        )

    category = getattr(entry, 'category', 'green')
    data = {
        'title': entry.title if entry else title,
        'category': category,
        'category_label': CATEGORY_DISPLAY.get(category, category),
        'layer': 'Axloqiy-maʼnaviy',
        'meaning': (entry.meaning if entry else '') or 'Ma’no kiritilmagan.',
        'description': (entry.notes if entry else '') or 'Ma’lumot mavjud emas.',
        'example': (entry.example if entry else '') or '',
        'page': (entry.pages if entry else '') or '',
    }
    return render(request, 'phrase_detail.html', {'phrase': data, 'related': related})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
