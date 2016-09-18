from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))
	# publish = forms.DateTimeInput()  DODELATT	
	class Meta:
		model = Post
		fields = [
			'title',
			'image',
			'content',
			'draft',
			'publish',
		]










# <!-- <div class="share_link">
# 	<p>
# 	<a href="https://www.facebook.com/sharer/sharer.php?u={{ request.build_absolute_uri }}">Facebook</a>
# 	<a href="https://twitter.com/home?status={{ instance.get_markdown|urlify }}%20{{ request.build_absolute_uri }}">Twitter</a>
# 	<a href="https://www.linkedin.com/shareArticle?mini=true&url={{ request.build_absolute_uri }}&title={{ instance.title }}&summary={{ instance.get_markdown|urlify }}&source=http://swiftforentrepreneurs.com/">
# 	Linkedin</a>
# 	</p>
# </div> -->