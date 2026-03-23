from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import ProfileEditForm
from polls.models import Vote


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    vote_history = Vote.objects.filter(
        user=user
    ).select_related('question', 'choice').order_by('-voted_at')

    return render(request, 'users/profile.html', {
        'profile_user': user,
        'profile': profile,
        'vote_history': vote_history,
        'is_own_profile': request.user == user,
    })


@login_required
def edit_profile(request, username):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.username = request.POST.get('username', request.user.username)
            request.user.email = request.POST.get('email', request.user.email)
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile, initial={
            'username': request.user.username,
            'email': request.user.email,
        })

    return render(request, 'users/edit_profile.html', {'form': form})