
######
# Lines 1 to 72 added to gitignore
######

@app.route('/users/<int:id>/password/reset')
@login_required
def reset_password(id):
    """ Resets password for the user who matches `id` """
    user = User.query.filter_by(id=id).first()
    if current_user.role in admins:
        user.reset_password()
        db.session.commit()
        flash(f'You have reset {user.fullname}\'s password')
    else:
        flash(f'You cannot reset {user.fullname}\'s password')
    return redirect(url_for('users'))


@app.route('/users/<id>/delete')
@login_required
def delete_user(id):
    try:
        going = User.query.filter_by(id=id).first()
        gone_name = going.fullname
        his_id = going.id
        if going:
            if current_user.role in admins:
                going.delete()
                flash(
                    f'You have deleted {gone_name if not current_user.id == his_id else "yourself"} successfully')
            else:
                flash(
                    f'You can\'t delete {gone_name if not current_user.id == his_id else "yourself"}')
    except AttributeError:
        flash('That user does not exist')
    return redirect(url_for('users'))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    """ User Profile editor"""
    form = UserForm()
    if form.is_submitted():
        current_user.firstname = change_in_db(
            current_user.firstname, form.firstname.data)
        current_user.lastname = change_in_db(
            current_user.lastname, form.lastname.data)
        current_user.email = change_in_db(current_user.email, form.email.data)
        current_user.password = change_in_db(
            current_user.password, form.password.data)
        current_user.tel = change_in_db(current_user.tel, form.tel.data)
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('users'))
    return render_template('profile.html', form=form, title='Your Profile', homes=homes)


@app.route('/logout')
def logout():
    """Logs out a user"""
    logout_user()
    flash('You just logged out')
    return redirect(url_for('index'))


@app.route('/notices')
@login_required
def notices():
    """Notice page handler"""
    page = request.args.get('page', 1, type=int)
    notices = Notice.query.order_by(
        Notice.id.desc()).paginate(page, per_page=5)
    return render_template('notices.html', title='Notice Board', notices=notices, admins=admins, User=User, homes=homes)


@app.route('/notices/new', methods=['GET', 'POST'])
@login_required
def new_notice():
    """Creates a new Notice and alerts users"""
    form = NoticeForm()
    users = User.query.filter(User.role!=None).all()
    if form.is_submitted():
        note = Notice(subject=form.subject.data, message=request.form.get(
            'ckeditor'), user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        with mail.connect() as conn:
            for user in users:
                note.subject = f"Athric Notice - {form.subject.data}"
                message = f"""
Hello {user.firstname},<br><br> There is a new notice you need to view.<br>
Its details:<hr><b>{form.subject.data}<b><br> {note.message}<br>From: {current_user.fullname}<hr>
<a href='http://localhost:5000/notices?page=1'><button style='border:none;border-radius:12px;background:blue;color:white;padding:5px 10px'>
View Notice</button></a> <br><br> Date: {note.date} <br><br>
Best regards, <br> Athric <br><br><br><br>
<small>Athric &copy; All rights reserved</small>
"""
                msg = Message(note.subject, sender=('Athric', os.getenv('ansah_gmail')), recipients=[user.email], html=message)
                conn.send(msg)
        flash('Your notice is received')
        return redirect(url_for('notices'))
    return render_template('new_notice.html', form=form, title='Add New Notice', ckeditor=ckeditor, homes=homes)


@app.route('/notices/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_notice(id):
    """Edits an already posted notice"""
    form = NewArticle()
    art = Notice.query.filter_by(id=id).first()
    if form.is_submitted():
        art.subject = change_in_db(art.subject, form.subject.data)
        art.message = change_in_db(art.message, request.form.get('ckeditor'))
        art.user_id = current_user.id if not art.user_id else art.user_id
        db.session.commit()
        flash('Your change is saved successfully')
        return redirect(url_for('notices'))
    return render_template('edit_article.html', title='Editing Notice', article=art, form=form, homes=homes)


@app.route('/notices/<id>/delete')
@login_required
def del_notice(id):
    """Deletes a notice"""
    note = Notice.query.filter_by(id=id).first()
    note.delete() if note else flash('Unable to delete note')
    db.session.commit()
    flash('Notice deleted')
    return redirect(url_for('notices'))


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    """Contact page and auto mailer"""
    form = Contact()
    users = User.query.filter(User.role.in_(admins)).all()
    if form.is_submitted():
        name,  email = form.name.data, form.email.data
        with mail.connect() as conn:
            for user in users:
                message = f"""
Hello {user.firstname}, <br><br>
There is a new notice from {name or email}.
Check it out immediately and take the required action.<br><br>
<i>Here is the message received:</i><hr>
<b>{form.subject.data or 'No Subject'}</b> <br>
{request.form.get('ckeditor')} <hr>
Name: {name or 'Not provided'} <br>
Email: {email}<br><br>Best regards, <br>Athric <br><br><br><br>
<small>Athric &copy; All rights reserved</small>
"""
                subject = f"Someone contacted you from Athric"
                msg = Message(subject, sender=('Athric', os.getenv('ansah_gmail')), recipients=[user.email], html=message)
                conn.send(msg)
            ###### Saving to the notices #######
            note = Notice(subject=form.subject.data, message=request.form.get(
                'ckeditor'), user_id=current_user.id)
            db.session.add(note)
            db.session.commit()
        flash('Thank you. We received your message')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, title='Send us a message', homes=homes)


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    """Opens the articles page ordered by newest first"""
    page = request.args.get('page', 1, type=int)
    form = Search()
    if form.is_submitted():
        query = form.search.data
        arts = Article.query.msearch(query).paginate(page, per_page=8)
        count = len(arts.items)
        return render_template('articles.html', title='All articles', count=count, articles=arts,
                               User=User, homes=homes, categories=at_categories, form=form)

    articles = Article.query.order_by(
        Article.id.desc()).paginate(page, per_page=8)
    return render_template('articles.html', title='All articles', articles=articles,
                           User=User, homes=homes, categories=at_categories, form=form)


@app.route('/articles/new', methods=['GET', 'POST'])
@login_required
def new_article():
    """Route for creating a new article"""
    form = NewArticle()
    if form.is_submitted():
        """ Saving the cover image """
        f = form.cover.data
        unique_name = str(uuid4()) + '.png'
        full_path = os.path.join('static', 'images', unique_name)
        f.save(full_path)
        article = Article(subject=request.form.get('subject'),
                          message=request.form.get('ckeditor'),
                          category=form.category.data)
        article.user_id, article.cover, article.unique_name = current_user.id, full_path, unique_name
        db.session.add(article)
        db.session.commit()
        flash('You created a new article')
        return redirect(url_for('articles'))
    return render_template('new_article.html', form=form, title='Add New Article', homes=homes)


@app.route('/articles/cover/<unique_name>')
def display_image(unique_name):
    """Displays an article's cover image"""
    pth = os.path.join('static', 'images')
    return send_from_directory(pth, unique_name)


@app.route('/articles/<id>/view')
def view_article(id):
    """Opens an article"""
    article = Article.query.filter_by(id=id).first()
    f_type = article.cover.split('.')[-1]
    print(article.cover.split('/')[-1])
    return render_template('view_article.html', title=article.subject, article=article, f_type=f_type, User=User, homes=homes)


@app.route('/articles/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    """Edits an already posted article"""
    form = NewArticle()
    art = Article.query.filter_by(id=id).first()
    if form.is_submitted():
        art.subject = change_in_db(art.subject, form.subject.data)
        art.message = change_in_db(art.message, request.form.get('ckeditor'))
        db.session.commit()
        flash('Your change is saved successfully')
        return redirect(url_for('articles'))
    return render_template('edit_article.html', title='Edit Article', article=art, form=form, homes=homes)


@app.route('/articles/categories/<category>')
def article_categories(category):
    """Returns the articles in the specified `category`"""
    articles = Article.query.filter_by(category=category).all()
    return render_template('article_categories.html', title=category.replace('_', ' ')+'s', homes=homes, articles=articles, User=User)


#### Lines 245 to 264 added to gitignore ####

@app.route('/files/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """Returns upload file page"""
    form = UploadFile()
    if form.is_submitted():
        f = form.content.data
        category = form.category.data
        o_name = form.f_name.data or f.filename.split('.')[0]
        _, extention = os.path.splitext(f.filename)
        unique_name = str(uuid4())
        f_path = os.path.join('static', category, unique_name + extention)
        f.save(f_path)
        file = File(user_id=current_user.id, original_name=o_name, u_name=unique_name,
                    f_type=category, path=f_path, fmt=extention[1:], message=request.form.get('ckeditor'))
        db.session.add(file)
        db.session.commit()
        flash(f'Your {category[:-1]} has been saved')
        return redirect(url_for('gallery', category=category))
    return render_template('upload_file.html', title='Upload a File', form=form, ckeditor=ckeditor, homes=homes)


@app.route('/files/<category>/view/<unique_name>')
@login_required
def view_file(category, unique_name):
    """Displays images, files, and videos with their details"""
    file = File.query.filter_by(f_type=category, u_name=unique_name).first()
    if category == 'documents':
        pth = os.path.join('static', category)
        return send_from_directory(pth, unique_name + '.' + file.fmt)
    return render_template('view_file.html', title=file.original_name, file=file, homes=homes, all=File, User=User, enumerate=enumerate)


@app.route('/files/<category>')
@login_required
def gallery(category):
    """Return Gallery for images, videos, and documents"""
    files = File.query.filter_by(f_type=category).all()
    return render_template('gallery.html',  files=files, title=category, homes=homes)


@app.route('/files/<category>/<id>/delete')
@login_required
def delete_file(category, id):
    """Deletes a file based on its id and type"""
    going = File.query.filter_by(f_type=category, id=id).first()
    if going:
        going.delete()
        flash(f'The {category[:-1]} is deleted')
    else:
        flash('file doesn not exist')
    return redirect(url_for('gallery', category=category))


if __name__ == '__main__':
    app.run()
