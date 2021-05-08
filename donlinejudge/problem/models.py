from django.db import models
from accounts.models import User

class ProblemDifficulty(object):
    hard = "Hard"
    medium = "Medium"
    easy = "Easy"
    DIFF = [hard, medium, easy]
    choices = [(easy, easy), (medium, medium), (hard, hard)]

class ProblemTag(models.Model):
    tagName = models.TextField()

    class Meta:
        db_table = "problemtag"


class Problem(models.Model):
    display_id = models.TextField(db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    # author = models.OneToOneField() ## TODO: Foreign key to user
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    #== Content to be displayed
    title = models.TextField()
    statement = models.TextField() ## TODO RichTextField support

    #== Tag, Difficulty, Source
    difficulty = models.CharField(choices=ProblemDifficulty.choices, max_length=50, default=ProblemDifficulty.easy)
    tags = models.ManyToManyField(ProblemTag)
    source = models.TextField(null=True)

    sample_test = models.JSONField(default=dict, null=True)
    ### [{input: "hello", output: "world"}, {input: "i am", output: "django"}]

    #== The Problem tests location
    testset_dir = models.TextField(null=True)
    testset_count = models.PositiveIntegerField(default=0)

    #== Problem constraints
    time_limit = models.IntegerField(default=1000)      ## millisecond
    memory_limit = models.IntegerField(default=256)    ## MB


    #== Statistics
    total_submission = models.BigIntegerField(default=0)
    correct_submission = models.BigIntegerField(default=0)
    statistic_info = models.JSONField(default=dict)
    ### {_.ACCEPTED: 5, _.WRONG_ANSWER: 4, ...}

    class Meta:
        db_table = "problem"
        ordering = ["created"]