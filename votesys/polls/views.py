from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import JsonResponse
from .models import Question, Choice, Comment, Reaction, Vote
from .forms import CreatePollForm
import json

class IndexView(generic.ListView):
  template_name = "polls/index.html"
  context_object_name = "latest_question_list"

  def get_queryset(self):
    """Return the last five published questions."""
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:20]

def results(request, pk):
    question = get_object_or_404(Question, pk=pk)
    choices = question.choice_set.all()
    total_votes = sum(c.votes for c in choices)

    return render(request, 'polls/results.html', {
        'question': question,
        'choices': choices,
        'total_votes': total_votes,
        'chart_labels': json.dumps([c.choice_text for c in choices]),
        'chart_votes': json.dumps([c.votes for c in choices]),
    })

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # check if user already voted
    if Vote.objects.filter(question=question, user=request.user).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You have already voted on this poll.',
            'comments': question.comments.order_by('-created_at'),
            'reaction_choices': Reaction._meta.get_field('reaction_type').choices,
            'reaction_counts': {
                r[0]: question.reactions.filter(reaction_type=r[0]).count()
                for r in Reaction._meta.get_field('reaction_type').choices
            },
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            'comments': question.comments.order_by('-created_at'),
            'reaction_choices': Reaction._meta.get_field('reaction_type').choices,
            'reaction_counts': {
                r[0]: question.reactions.filter(reaction_type=r[0]).count()
                for r in Reaction._meta.get_field('reaction_type').choices
            },
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        Vote.objects.create(question=question, user=request.user, choice=selected_choice)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
  

def share_poll(request, token):
    # resolves /polls/share/<token>/ to the correct poll
    question = get_object_or_404(Question, share_token=token)
    return redirect('polls:detail', pk=question.pk)


@login_required
def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            comment = Comment.objects.create(question=question, user=request.user, text=text)
            return JsonResponse({
                'success': True,
                'username': comment.user.username,
                'text': comment.text,
                'time': 'just now'
            })
    return JsonResponse({'success': False, 'error': 'Empty comment'})

@login_required
def add_reaction(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        reaction_type = request.POST.get('reaction_type')
        valid = [r[0] for r in Reaction._meta.get_field('reaction_type').choices]

        if reaction_type in valid:
            existing = Reaction.objects.filter(question=question, user=request.user).first()
            if existing:
                if existing.reaction_type == reaction_type:
                    existing.delete()
                    action = 'removed'
                else:
                    existing.reaction_type = reaction_type
                    existing.save()
                    action = 'switched'
            else:
                Reaction.objects.create(question=question, user=request.user, reaction_type=reaction_type)
                action = 'added'

            # return updated counts for all reactions
            counts = {
                r[0]: question.reactions.filter(reaction_type=r[0]).count()
                for r in Reaction._meta.get_field('reaction_type').choices
            }
            return JsonResponse({'success': True, 'action': action, 'counts': counts, 'reaction_type': reaction_type})

    return JsonResponse({'success': False})


def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    comments = question.comments.order_by('-created_at')
    reaction_choices = Reaction._meta.get_field('reaction_type').choices
    reaction_counts = {
        r[0]: question.reactions.filter(reaction_type=r[0]).count()
        for r in reaction_choices
    }
    user_has_voted = Vote.objects.filter(question=question, user=request.user).exists()

    return render(request, 'polls/detail.html', {
        'question': question,
        'comments': comments,
        'reaction_choices': reaction_choices,
        'reaction_counts': reaction_counts,
        'user_has_voted': user_has_voted,
    })

@login_required
def create_poll(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        choices = [v.strip() for v in request.POST.getlist('choices') if v.strip()]

        if form.is_valid() and len(choices) >= 2:
            question = Question.objects.create(
                question_text=form.cleaned_data['question_text'],
                pub_date=timezone.now(),
                created_by=request.user,
            )
            for choice_text in choices:
                Choice.objects.create(question=question, choice_text=choice_text)

            return redirect('polls:detail', pk=question.pk)

        return render(request, 'polls/create.html', {
            'form': form,
            'errors': 'Please enter a question and at least 2 choices.',
            'prev_choices': request.POST.getlist('choices'),
        })

    return render(request, 'polls/create.html', {'form': CreatePollForm()})