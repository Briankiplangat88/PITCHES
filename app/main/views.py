from flask import render_template,request,redirect,url_for,abort
from ..models import User,Pitches,Comments
from .. import db,photos
import markdown2  
from .forms import UpdateProfile,CommentForm,PitchForm
# from app import auth
from . import main
from flask_login import login_required,current_user
#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
 
    title='Pitch site'
    return render_template('index.html',title=title)
    
@main.route('/pitch/newpitch', methods=['POST', 'GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        # newPitch = form.pitch_info.data
        new_pitch = Pitches(pitch_title=title,pitch_category=category,user=current_user)
        new_pitch.save_pitch()
        return redirect(url_for('.index'))
    title = 'Add pitch'
    return render_template('pitches.html', title=title, pitchesform=form)

@main.route('/categories/<category>')
def categories(category):
    '''
    view function to display interview pitches
    '''
    pitches=Pitches.get_pitches (category)
    title = category + "pitches"
 
    return render_template('categories.html',title=title,pitches=pitches)


@main.route('/comments/<id>')
@login_required
def comment(id):
    '''
    function to return the comments
    '''
    comments =Comments.get_comments(id)
   
    title = 'comments'
    return render_template('comments.html',comments = comments,title = title)

@main.route('/new_comment/<int:pitches_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(pitches_id):
    pitches = Pitches.query.filter_by(id = pitches_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(pitch_comment=comment,user_id=current_user.id, pitches_id=pitches_id)

        new_comment.save_comment()

        return redirect(url_for('main.index'))
    title='New Pitch'
    return render_template('new_comment.html',title=title,comment_form = form,pitches_id=pitches_id)
@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname = user.username))
    return render_template('profile/update.html',form = form)
@main.route('/user/<uname>/update/pic',methods = ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname = uname))