from django.http import JsonResponse
from django.shortcuts import render

from note.models import Note
from utils.jwt import login_required
from utils.note_params_check import note_params_check
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone

# Create your views here.
@login_required
def get_categories(request):
    """
    获取类别列表
    """
    if request.method == "GET":
        user = request.user
        categories = Note.objects.filter(user=user).values("category").distinct()

        return JsonResponse(
            {
                "categories": [category["category"] for category in categories],
                "total": len(categories),
            },
            status=200,
        )
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def create_note(request):
    """
    创建笔记
    """
    if request.method == "POST":
        title, textContent, category, errors = note_params_check(request)

        if errors:
            return JsonResponse(errors, status=400)

        picture = request.FILES.get('picture')
        audio = request.FILES.get('audio')

        now=timezone.now()
        note = Note.objects.create(
            user=request.user,
            title=title,
            textContent=textContent,
            category=category,
            picture=picture,
            audio=audio,
            created=now,
            updated=now
        )
        note.save()
        return JsonResponse({
            "message": "Note created successfully",
            "note_id": note.id
        }, status=201)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def update_note(request):
    """
    更新笔记
    """
    if request.method == "POST":
        note_id = request.POST.get('note_id')

        try:
            with transaction.atomic():
                note = Note.objects.get(id=note_id, user=request.user)

                note.title = request.POST.get('title', note.title)
                note.textContent = request.POST.get('textContent', note.textContent)
                note.category = request.POST.get('category', note.category)

                if 'picture' in request.FILES:
                    note.picture = request.FILES['picture']
                if 'audio' in request.FILES:
                    note.audio = request.FILES['audio']

                note.updated = timezone.now()

                note.save()

            return JsonResponse({
                "message": "Note updated successfully",
                "note_id": note.id
            }, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "Note not found"}, status=404)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def delete_note(request):
    """
    删除笔记
    """
    if request.method == "POST":
        note_id = request.POST.get('note_id')
        note = Note.objects.get(id=note_id, user=request.user)
        note.delete()
        return JsonResponse({"message": "Note deleted successfully"}, status=200)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def get_notes(request):
    """
    根据类别获取笔记列表
    """
    if request.method == "GET":
        user = request.user
        category = request.GET.get("category")
        notes = Note.objects.filter(user=user, category=category).values("id", "title", "textContent", "created", "updated")

        return JsonResponse(
            {
                "notes": list(notes),
                "total": len(notes),
            },
            status=200,
        )
    
    else :
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def get_note_detail(request):
    """
    获取笔记详情
    """
    if request.method == "GET":
        note_id = request.GET.get("note_id")
        note = Note.objects.filter(id=note_id).values("id", "category", "title", "textContent", "picture", "audio", "created", "updated")

        return JsonResponse(
            {
                "category": note[0]["category"],
                "title": note[0]["title"],
                "textContent": note[0]["textContent"],
                "picture": note[0]["picture"],
                "audio": note[0]["audio"],
                "created": note[0]["created"],
                "updated": note[0]["updated"],
            },
            status=200,
        )
    
    else: 
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def search_notes_by_keyword(request):
    """
    根据关键词搜索笔记
    """
    if request.method == "GET":
        user = request.user
        keyword = request.GET.get("keyword")

        if not keyword:
            return JsonResponse({"message": "Keyword parameter is required and cannot be empty."}, status=400)


        query = Q(title__contains=keyword) | Q(textContent__contains=keyword) | Q(category__contains=keyword)
        notes = Note.objects.filter(query, user=user)


        return JsonResponse(
            {
                "notes": list(notes.values()),
                "total": notes.count(),
            },
            status=200,
        )

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
