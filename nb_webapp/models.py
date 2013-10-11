from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# BasicInfo Table
class BasicInfo(models.Model):
    #user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, primary_key=True)
    #account_email= models.EmailField()
    #password = models.CharField(max_length=100)
    #first_name = models.CharField(max_length=30)
    #last_name = models.CharField(max_length=40)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    account_type = models.CharField(max_length=1)
    linkedin_member_id=models.CharField(max_length=20, blank=True)
    facebook_member_id=models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    #work is different form the db design
    about_me = models.CharField(max_length=300, blank=True)
    ACCESS_RIGHTS = (
        ('PUB', 'Public'),
        ('PRI', 'Private')
    )
    access_rights = models.CharField(max_length=3, choices=ACCESS_RIGHTS, blank=True)

    def __unicode__(self):
        name = [self.user.first_name, self.user.last_name]
        return ' '.join(p for p in name)


# WorkInfo Table
class WorkInfo(models.Model):
    basic_info = models.ForeignKey(BasicInfo)
    company_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300,blank=True)
    position = models.CharField(max_length=30, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __unicode__(self):
        p = BasicInfo.objects.get(user__pk = self.basic_info_id)
        name = [p.user.first_name, p.user.last_name]
        return ' '.join(q for q in name)


# KnowledgeProfile Table
class KnowledgeProfile(models.Model):
    basic_info = models.ForeignKey(BasicInfo)
    interests = models.CharField(max_length=50, blank=True)
    num_flowers = models.PositiveIntegerField()
    num_posts = models.PositiveIntegerField()
    num_tags = models.PositiveIntegerField()
    num_thumbs = models.PositiveIntegerField()
    num_followings = models.PositiveIntegerField()
    num_followers = models.PositiveIntegerField()
    ACCESS_RIGHTS = (
        ('PUB', 'Public'),
        ('PRI', 'Private'),
    )
    access_rights = models.CharField(max_length=3, choices=ACCESS_RIGHTS, blank=True)
    # knowledge_board = models.OneToOneField(KnowledgeBoard)

    def __unicode__(self):
        p = BasicInfo.objects.get(user__pk = self.basic_info_id)
        name = [p.user.first_name, p.user.last_name]
        return ' '.join(q for q in name)

# KnowledgeBoard
# class KnowledgeBoard(models.Model):
#    def __unicode__(self):
#        return ""


# KnowledgeCard Table
class KnowledgeCard(models.Model):
    # knowledge_card = models.ForeignKey(KnowledgeCard)
    card_id = models.AutoField(primary_key=True)
    basic_info = models.ForeignKey(BasicInfo)
    title = models.CharField(max_length=30)
    #need to verify max chars
    contents = models.CharField(max_length=150)
    # picture = models.ImageField(upload_to='/Users/jinguangzhou/git/NoahBoard/images')
    video_link = models.URLField(blank=True)
    source_link = models.URLField(blank=True)
    CATEGORIES = (
        ('MI', 'Mobile & Internet industry'),
        ('BE', 'Business & Entrepreneur'),
        ('LM', 'Leadership & Management'),
        ('MA', 'Marketing & Advertising'),
        ('CS', 'Consulting & Strategy'),
        ('SD', 'Sales & Distribution'),
        ('CT', 'Computer & Technology'),
        ('DU', 'Design & User experience'),
        ('NS', 'NGO & Social enterprise'),
    )
    category = models.CharField(max_length=2, choices=CATEGORIES)
    #TAGS = (
    #    ('JAVA', 'Java'),
    #    ('Python', 'Python'),
    #)
    tags = models.CharField(max_length=50, blank=True)
    post_date = models.DateField()
    num_thumbs = models.PositiveIntegerField()
    num_reposts = models.PositiveIntegerField()
    num_shares = models.PositiveIntegerField()
    num_comments = models.PositiveIntegerField()
    ACCESS_RIGHTS = (
        ('PUB', 'Public'),
        ('PRI', 'Private'),
    )
    access_rights = models.CharField(max_length=3, choices=ACCESS_RIGHTS, blank=True)

    def __unicode__(self):
        return self.title
#UserProfile
#class UserProfile(models.Model):
#    basic_info = models.OneToOneField(BasicInfo)
#    followers = models.ManyToManyField(BasicInfo,related_name="followers_basic_info")
#    knowledge_profile = models.OneToOneField(KnowledgeProfile)


# CommentInfo Table
class CommentInfo(models.Model):
    comment_id = models.AutoField(primary_key=True)
    knowledge_card = models.ForeignKey(KnowledgeCard)
    commentator_id = models.ForeignKey(BasicInfo)
    contents = models.CharField(max_length=100)
    post_date = models.DateField()
    num_upvotes = models.PositiveIntegerField()

    def __unicode__(self):
        p = KnowledgeCard.objects.get(card_id = self.knowledge_card_id)
        return p.title


# FollowerInfo Table
class FollowerInfo(models.Model):
    basic_info = models.ForeignKey(BasicInfo, related_name='+')
    follower_info = models.ForeignKey(BasicInfo, related_name='+')


# FollowingInfo Table
class FollowingInfo(models.Model):
    basic_info = models.ForeignKey(BasicInfo, related_name='+')
    following_info = models.ForeignKey(BasicInfo, related_name='+')


# RepostInfo Table
class RepostInfo(models.Model):
    knowledge_card = models.ForeignKey(KnowledgeCard)
    sharer_info = models.ForeignKey(BasicInfo)
    share_type = models.BooleanField() # True: reposts, False: share
