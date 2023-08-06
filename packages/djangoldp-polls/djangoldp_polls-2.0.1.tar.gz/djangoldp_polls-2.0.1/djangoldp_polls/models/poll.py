from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import functools

from djangoldp.models import Model
from django.db import models, transaction
from djangoldp_conversation.models import Conversation
from djangoldp_circle.models import Circle
from djangoldp_notification.models import Notification
from djangoldp.activities.services import ActivityQueueService

from django.utils.timezone import localdate, timedelta
from django.template import loader

from djangoldp_polls.permissions import *
from djangoldp_polls.models.legacy import Tag

from djangoldp.views import LDPViewSet


def onMonthLater():
    return localdate() + timedelta(days=30)


class QuestionRecorder:
    def record(self, request, poll):
        if request['type'] == 'free-text':
            question = QuestionFreeText(
                name=request['name']
            )
            question.poll = poll
            question.save()
        elif request['type'] == 'range':
            question = QuestionRange(
                name=request['name'],
                start=request['start'],
                end=request['end']
            )
            question.poll = poll
            question.save()
        elif request['type'] == 'radio':
            question = QuestionRadio(name=request['name'])
            question.poll = poll
            question.save()
            for choice in request['choices']['ldp:contains']:
                choice = QuestionRadioProposition(name=''.join(choice.values()))
                choice.question = question
                choice.save()
        elif request['type'] == 'checkboxes':
            question = QuestionCheckboxes(name=request['name'])
            question.poll = poll
            question.save()
            for choice in request['choices']['ldp:contains']:
                choice = QuestionCheckboxesProposition(name=''.join(choice.values()))
                choice.question = question
                choice.save()
        elif request['type'] == 'singlechoice':
            question = QuestionSingleChoice(name=request['name'])
            question.poll = poll
            question.save()
            for choice in request['choices']['ldp:contains']:
                choice = QuestionSingleChoiceProposition(name=''.join(choice.values()))
                choice.question = question
                choice.save()
        elif request['type'] == 'multiplechoice':
            question = QuestionMultipleChoice(name=request['name'])
            question.poll = poll
            question.save()
            for choice in request['choices']['ldp:contains']:
                choice = QuestionMultipleChoiceProposition(name=''.join(choice.values()))
                choice.question = question
                choice.save()

        else:
            raise AttributeError('Invalid field type')

        return question


# Here to avoid circular dependencies problem
class PollViewSet(LDPViewSet):
    def perform_create(self, serializer, **kwargs):
        instance = super().perform_create(serializer, **kwargs)

        recorder = QuestionRecorder()


        if('type' in self.request.data['questionsUnmaped']['ldp:contains']): #single queston
            questions = [self.request.data['questionsUnmaped']['ldp:contains']]
        else:
            questions = self.request.data['questionsUnmaped']['ldp:contains']

        for questionRequest in questions:
            recorder.record(questionRequest, instance)
        return instance


class Poll(Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='createdVotes', null=True, blank=True,
                               on_delete=models.SET_NULL)
    title = models.CharField(max_length=250, verbose_name="Title", null=True, blank=True)
    image = models.URLField(verbose_name="Illustration",
                            default="https://unpkg.com/@startinblox/component-poll@2.1/img/defaultpoll.png", null=True,
                            blank=True)
    hostingOrganisation = models.CharField(max_length=250, verbose_name="Name of the hosting organisation", null=True,
                                           blank=True)
    startDate = models.DateField(verbose_name="Start date", blank=True, null=True)
    endDate = models.DateField(verbose_name="End data", default=onMonthLater, null=True, blank=True)
    shortDescription = models.CharField(max_length=250, verbose_name="Short description", null=True, blank=True)
    longDescription = models.TextField(verbose_name="Long description", null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='polls', blank=True)
    debate = models.ManyToManyField(Conversation, related_name='polls', blank=True)
    circle = models.ForeignKey(Circle, blank=True, null=True, related_name="polls", on_delete=models.SET_NULL)
    creationDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    authorNotificationOnComment = models.BooleanField(default=True)

    class Meta(Model.Meta):
        auto_author = 'author'
        serializer_fields = ['@id', 'created_at', 'debate', 'author', 'title', 'image', 'circle', \
                             'hostingOrganisation', 'startDate', 'endDate', 'shortDescription', 'longDescription',
                             'tags', 'authorNotificationOnComment', 'questions']
        nested_fields = ['tags', 'debate', 'circle', "questions"]
        anonymous_perms = ['view', 'add']
        authenticated_perms = ['inherit']
        owner_perms = ['inherit', 'change', 'delete']
        owner_field = 'author'
        # permission_classes = [PollPermissions]
        rdf_type = 'sib:poll'
        view_set = PollViewSet

    def __str__(self):
        return self.title or ''


class Question(Model):
    name = models.CharField(max_length=250, verbose_name="Name of the question")
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)

    class Meta(Model.Meta):
        serializer_fields = ['@id', 'name', 'type']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'delete', 'change']
        rdf_type = 'sib:question'

    def __str__(self):
        return self.name


class QuestionFreeText(Question):
    class Meta(Model.Meta):
        serializer_fields = ['@id', 'name']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'delete', 'change']
        rdf_type = 'sib:question_free_text'

class QuestionRange(Question):
    start = models.IntegerField()
    end = models.IntegerField()

    class Meta(Model.Meta):
        serializer_fields = ['@id', 'name', 'start', 'end']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'delete', 'change']
        rdf_type = 'sib:question_range'

class QuestionRadio(Question):
    class Meta(Model.Meta):
        serializer_fields = ['@id', 'name']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'delete', 'change']
        rdf_type = 'sib:question_radio'


class QuestionRadioProposition(Model):
    name = models.CharField(max_length=250, verbose_name="Title", null=True, blank=True)
    question = models.ForeignKey(QuestionRadio, related_name='propositions', on_delete=models.CASCADE)

class QuestionCheckboxes(Question):
    class Meta(Model.Meta):
        serializer_fields = ['@id', 'name']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'delete', 'change']
        rdf_type = 'sib:question_checkboxes'

class QuestionCheckboxesProposition(Model):
    name = models.CharField(max_length=250, verbose_name="Title", null=True, blank=True)
    question = models.ForeignKey(QuestionCheckboxes, related_name='propositions', on_delete=models.CASCADE)

class QuestionSingleChoice(Question):
    class Meta(Model.Meta):
        serializer_fields = ['@id', 'name']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'delete', 'change']
        rdf_type = 'sib:question_singlechoice'

class QuestionSingleChoiceProposition(Model):
    name = models.CharField(max_length=250, verbose_name="Title", null=True, blank=True)
    question = models.ForeignKey(QuestionSingleChoice, related_name='propositions', on_delete=models.CASCADE)

class QuestionMultipleChoice(Question):
    class Meta(Model.Meta):
        serializer_fields = ['@id', 'name']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'delete', 'change']
        rdf_type = 'sib:question_multiplechoices'

class QuestionMultipleChoiceProposition(Model):
    name = models.CharField(max_length=250, verbose_name="Title", null=True, blank=True)
    question = models.ForeignKey(QuestionMultipleChoice, related_name='propositions', on_delete=models.CASCADE)

# used to execute func after a DB transaction is commited
# https://docs.djangoproject.com/en/dev/topics/db/transactions/#django.db.transaction.on_commit
def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


# I know this shouldn't live here, but putting it in views results in circular dependency problems
# https://git.startinblox.com/djangoldp-packages/djangoldp/issues/278
# class VoteViewSet(LDPViewSet):
# 	def is_safe_create(self, user, validated_data, *args, **kwargs):
# 		try:
# 			if 'poll' in validated_data.keys():
# 				poll = Poll.objects.get(urlid=validated_data['poll']['urlid'])
# 			else:
# 				poll = self.get_parent()
#
# 			if Vote.objects.filter(relatedPoll=poll, user=user).exists():
# 				raise serializers.ValidationError('You may only vote on this poll once!')
#
# 		except Poll.DoesNotExist:
# 			return True
# 		except (KeyError, AttributeError):
# 			raise Http404('circle not specified with urlid')
#
# 		return True

@receiver(m2m_changed, sender=Poll.debate.through)
def send_notification(instance, action, **kwargs):
    if action != 'post_add':
        return

    poll = instance.polls.all()[0]
    if instance.author_user.urlid == poll.author.urlid:
        return

    if not poll.authorNotificationOnComment:
        return

    # local inbox
    if poll.author.urlid.startswith(settings.SITE_URL):
        Notification.objects.create(
            user=poll.author,
            object=poll.urlid,
            type="Poll_debate",
            author=instance.author_user.urlid,
            summary="A commenté votre proposition."
        )
    # external inbox
    else:
        json = {
            "@context": settings.LDP_RDF_CONTEXT,
            "object": poll.urlid,
            "type": "Poll_debate",
            "author": instance.author_user.urlid,
            "summary": "A commenté votre proposition."
        }
        ActivityQueueService.send_activity(poll.author.urlid, json)

    # Send email
    html_message = loader.render_to_string(
        'debate_notification.html',
        {
            'author': instance.author_user.first_name + ' ' + instance.author_user.last_name,
            'pollName': poll.title,
            'link': (getattr(settings, 'INSTANCE_DEFAULT_CLIENT', False) or settings.JABBER_DEFAULT_HOST),
            'content': instance.title
        }
    )

    if poll.author.settings.receiveMail:
        send_mail(
            'Vous avez une nouvelle notification sur la République de l’ESS !',
            'Vous avez une nouvelle notification sur la République de l’ESS !',
            (getattr(settings, 'EMAIL_HOST_USER', False) or "noreply@" + settings.JABBER_DEFAULT_HOST),
            [poll.author.email],
            fail_silently=True,
            html_message=html_message
        )
