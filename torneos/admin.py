from django.contrib import admin

# Register your models here.
from .models.torneo_model import Torneo
from .models.profile_model import Profile
from .models.registration_model import Registration
from .models.registration_model import RegistrationQuestion
from .models.registration_model import RegistrationQuestionChoice
from .models.registration_model import RegistrationQuestionResponse
from .models.score_model import Score

class TorneoAdmin(admin.ModelAdmin):
	list_display = ('title', 'end_date')
	list_display_links = ('title',)
	list_filter = ('end_date', 'recruiting')
	#prepopulated_fields = {'slug': ('title', )}

admin.site.register(Torneo, TorneoAdmin)

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)


class ScoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Score, ScoreAdmin)


class InlineRegistrationAdmin(admin.TabularInline):
    model = Registration
    fields = ('user', 'signup_date',)
    readonly_fields = ('user', 'signup_date',)


class InlineRegistrationQuestionAdmin(admin.StackedInline):
    model = RegistrationQuestion


class InlineRegistrationQuestionChoiceAdmin(admin.StackedInline):
    model = RegistrationQuestionChoice


class InlineResponseAdmin(admin.TabularInline):
    extra = 0
    max_num = 0
    supported_question_types = ('SA', 'SC', 'MC', 'AB')

    def queryset(self, request):
        qs = super(InlineResponseAdmin, self).queryset(request)
        supported = self.supported_question_types
        queries = [Q(question__question_type=t) for t in supported]
        query = reduce(lambda x, y: x | y, queries)
        return qs.filter(query)

class InlineShortAnswerResponseAdmin(InlineResponseAdmin):
    model = RegistrationQuestionResponse
    fields = ('question', 'text_response')
    readonly_fields = ('question', 'text_response')
    supported_question_types = ('SA',)


class InlineMultipleChoiceResponseAdmin(InlineResponseAdmin):
    model = RegistrationQuestionResponse
    fields = ('question', 'choices')
    readonly_fields = ('question', 'choices')
    supported_question_types = ('SC', 'MC')


class InlineAgreementResponseAdmin(InlineResponseAdmin):
    model = RegistrationQuestionResponse
    fields = ('question', 'agreed')
    readonly_fields = ('question', 'agreed')
    supported_question_types = ('AB',)



class RegistrationAdmin(admin.ModelAdmin):
    inlines = (InlineShortAnswerResponseAdmin,
               InlineMultipleChoiceResponseAdmin,
               InlineAgreementResponseAdmin)
    list_display = ('user', 'competition', 'signup_date', 'active')
    list_filter = ('signup_date', 'active')


class RegistrationQuestionAdmin(admin.ModelAdmin):
    inlines = (InlineRegistrationQuestionChoiceAdmin,)
    list_display = ('question_type', 'question')
    list_filter = ('question_type',)

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(RegistrationQuestion, RegistrationQuestionAdmin)


