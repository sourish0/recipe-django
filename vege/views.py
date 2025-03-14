from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Recipe

def recipe_list(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to create a recipe.")
            return redirect('login')
        
        data = request.POST
        user=request.user
        title = data.get('title', '')
        description = data.get('description', '')
        image = request.FILES.get('image')

        Recipe.objects.create(user=user,title=title, description=description, recipe_image=image)
        messages.success(request, "Recipe added successfully!")
        return redirect('recipe_list')

    recipe_list = Recipe.objects.all()
    if request.GET.get('search'):
        recipe_list = recipe_list.filter(title__icontains=request.GET.get('search'))

    return render(request, 'recipe_list.html', {'recipe_list': recipe_list})


def recipe_delete(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to delete a recipe.")
        return redirect('login')
    recipe = get_object_or_404(Recipe, id=pk)
    if recipe.user != request.user or recipe.user==None:
        messages.error(request, "You are not the owner of this recipe.")
        return redirect('recipe_list')
    recipe.delete()
    messages.success(request, "Recipe deleted successfully!")
    return redirect('recipe_list')


def recipe_update(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to update a recipe.")
        return redirect('login')

    recipe = get_object_or_404(Recipe, id=pk)
    if recipe.user != request.user:
        messages.error(request, "You are not the owner of this recipe.")
        return redirect('recipe_list')
    if request.method == 'POST':
        data = request.POST
        title = data.get('title', '')
        description = data.get('description', '')
        image = request.FILES.get('image')

        recipe.title = title
        recipe.description = description
        if image:
            recipe.recipe_image = image
        recipe.save()

        messages.success(request, "Recipe updated successfully!")
        return redirect('recipe_list')

    return render(request, 'recipe_update.html', {'recipe': recipe})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('recipe_list')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password')
            return redirect('/login/')

        login(request, user)
        messages.success(request, "Login successful!")
        return redirect('recipe_list')

    return render(request, 'login.html')


def signin_page(request):
    if request.user.is_authenticated:
        return redirect('recipe_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signin.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('recipe_list')

    return render(request, 'signin.html')


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/login')
