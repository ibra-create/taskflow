import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import webview

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    due_date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/task/create', methods=['POST'])
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    start_time_str = request.form.get('start_time', '00:00')
    end_time_str = request.form.get('end_time', '23:59')
    priority = request.form.get('priority', 'medium')
    
    try:
        if due_date_str and start_time_str:
            # Combine date with start time for the due_date
            start_datetime_str = f"{due_date_str} {start_time_str}"
            due_date = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
            
            # Combine date with end time
            end_datetime_str = f"{due_date_str} {end_time_str}"
            end_time = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')
        else:
            due_date = None
            end_time = None
        
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            end_time=end_time,
            priority=priority,
            status='pending'
        )
        
        db.session.add(task)
        db.session.commit()
        
    except Exception as e:
        print(f"Error creating task: {e}")
        db.session.rollback()
    
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    new_status = request.form.get('status', task.status)
    
    # Update the task status and times
    if new_status == 'in_progress' and task.status != 'in_progress':
        task.start_time = datetime.now()
    
    task.status = new_status
    task.priority = request.form.get('priority', task.priority)
    task.title = request.form.get('title', task.title)
    task.description = request.form.get('description', task.description)
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/static/notification.mp3')
def serve_notification_sound():
    return send_file('static/notification.mp3', mimetype='audio/mpeg')

def start_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)