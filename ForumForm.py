from wtforms import Form, StringField, FloatField, IntegerField, RadioField, SelectField, TextAreaField, validators

class createForumPost(Form):
    post_subject = StringField('Post Subject:', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Give your topic a subject title."})    # category = SelectField('Category:', [validators.DataRequired()], choices=[('', 'Select'), ('Pinned Posts', 'Pinned Posts'), ('Announcements', 'Announcements'), ('Unified Help Community', 'Unified Help Community')], default='')
    post_message = TextAreaField('Post Message:', [validators.Length(min=1, max=10000), validators.DataRequired()], id='contentcode', render_kw={'placeholder':'Write your comment here.','rows':'4'})

class updateForumPost(Form):
    post_message = TextAreaField('Post Message:', [validators.Length(min=1, max=10000), validators.DataRequired()], id='contentcode', render_kw={'placeholder':'Write your comment here.','rows':'4'})

class staff_createForumPost(Form):
    username = StringField('Username:', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'placeholder':'Enter your username here.'})
    post_subject = StringField('Post Subject:', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Give your topic a subject title."})
    category = SelectField('Category:', [validators.DataRequired()], choices=[('', 'Select'), ('Pinned Posts', 'Pinned Posts'), ('Announcements', 'Announcements'), ('Unified Help Community', 'Unified Help Community')], default='')
    post_message = TextAreaField('Post Message:', [validators.Length(min=1, max=10000), validators.DataRequired()], id='contentcode', render_kw={'placeholder':'Write your comment here.','rows':'4'})
