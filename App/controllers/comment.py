from App.models import Comment
from App.models import Review
from App.models import Staff
from App.database import db
from datetime import datetime
from .reply import delete_reply


def get_all_comments():
    return Comment.query.all()

def get_all_comments_review(reviewID):
    return Comment.query.filter_by(reviewID=reviewID).all()

def get_comment_staff(createdByStaffID):

    return Comment.query.filter_by(createdByStaffID=createdByStaffID).all()


def get_comment(id):
    return Comment.query.filter_by(ID=id).first()

def create_comment(reviewID, staffID, details):
    new_comment= Comment(reviewID=reviewID, staffID=staffID, details=details) 
    new_comment.replies =[]

    if new_comment:
        existing_review = Review.query.get(reviewID)

        if existing_review:
            existing_review.comments.append(new_comment)
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        else:
            return None
    else:
        return None


def delete_comment(comment_id, staff_id):
    comment = get_comment(comment_id)
    if comment:
        if comment.createdByStaffID == staff_id:
            for reply in comment.replies:
                delete_reply(reply.ID, staff_id)
            db.session.delete(comment)
            db.session.commit()
            return True
        else:
            return None
    else:
        return None

def edit_comment(details, comment_id, staff_id):
    
    existing_comment = get_comment(comment_id)
    if existing_comment:

        if existing_comment.createdByStaffID == staff_id:

            existing_comment.details = details
            existing_comment.dateCreated = datetime.now()
            db.session.add(existing_comment)
            db.session.commit()
            return True
        else:
            return None
    else:
        return None