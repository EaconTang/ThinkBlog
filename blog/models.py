from django.db import models

# Create your models here.
class MDFile(models.Model):
    # md_id = models.AutoField(primary_key=True, verbose_name="md_id", auto_created=True)
    md_url = models.CharField(max_length=256, unique=True)
    md_filename = models.CharField(max_length=128, unique=True)
    md_text = models.TextField(blank=True)
    md_pub_time = models.DateTimeField(verbose_name='publish date', null=True)
    md_mod_time = models.DateTimeField(verbose_name='modify date', null=True)
    md_modified = models.NullBooleanField()
    md_visit = models.IntegerField(null=True)

    def __unicode__(self):
        return self.md_filename


class MDFileCategory(models.Model):
    md_category_name = models.CharField(max_length=32, unique=True)
    
    def __unicode__(self):
        return self.md_category_name
    

class MDFileTag(models.Model):
    md_tag_name = models.CharField(max_length=32, unique=True)
    # md_file = models.ForeignKey(MDFile, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.md_tag_name


class MDFileComment(models.Model):
    md_comment_author = models.CharField(max_length=32, default="Anonymous", blank=True)
    md_comment_mail = models.EmailField(blank=True)
    md_comment_time = models.DateTimeField('comment time', null=True)
    md_comment = models.TextField()
    # md_file = models.ForeignKey(MDFile, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.md_comment

