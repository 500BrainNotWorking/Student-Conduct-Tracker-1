from App.models import Karma
from App.database import db
from .review import (get_total_positive_review_starRating, get_total_negative_review_starRating, get_unique_reviewers_count)
from .accomplishment import (get_total_accomplishment_points)
from .incidentReport import (get_total_incident_points)
from .transcript import (calculate_academic_score)


def get_karma(studentID):
  karma = Karma.query.filter_by(studentID=studentID).first()
  if karma:
    return karma
  else:
    return None

def get_karma_student(student):
  karma = Karma.query.filter_by(studentID=student.ID).first()
  if karma:
    return karma
  else:
    return None


def create_karma(studentID):
  newKarma = Karma(points=0.0,
                   academicPoints=0.0,
                   accomplishmentPoints=0.0,
                   reviewsPoints=0.0,
                   incidentPoints=0.0,
                   rank=-99,
                   studentID=studentID)
  db.session.add(newKarma)
  try:
    db.session.commit()
    return True
  except Exception as e:
    print("[karma.create_karma] Error occurred while creating new karma: ",
          str(e))
    return False


def calculate_review_points(studentID):
  
  karma = get_karma(studentID) # fetching the current karma for the student
  
  # Get total star ratings for positive and negative reviews
  positive_star_rating = get_total_positive_review_starRating(studentID)
  negative_star_rating = get_total_negative_review_starRating(studentID)

  # Unique reviewer count: integrity factor for karma calculation

  unique_reviewers_count = get_unique_reviewers_count(studentID)
  #202412 Added cap of 5 for unique reviewers
  integrity_factor = 1.0 + (min(unique_reviewers_count,5) * 0.1) # bonus for more diverse reviewers

  review_points = (positive_star_rating * 1.0) + (negative_star_rating * -0.5)

  # Apply the integrity factor (adjustment based on unique reviewers)

  review_points *= integrity_factor
  #review_points = get_total_positive_review_starRating(studentID) + get_total_negative_review_starRating(studentID)

  # Updating karma
  if karma:
    karma.reviewsPoints = review_points
    db.session.commit()
    return True
  else:
    return False



def calculate_accomplishment_points(studentID):
  karma = get_karma(studentID)
  accomplishmentPoints = get_total_accomplishment_points(studentID)
  if karma:
    #print("accomplishment points from controller:", accomplishmentPoints)
    karma.accomplishmentPoints = accomplishmentPoints

    db.session.commit()
    return True
  else:
    return False

def calculate_incident_points(studentID):
  karma = get_karma(studentID)
  incidentPoints = get_total_incident_points(studentID)
  if karma:
    #print("incident points from controller:", incidentPoints)
    karma.incidentPoints = incidentPoints

    db.session.commit()
    return True
  else:
    return False

def calculate_academic_points(studentID):
  karma = get_karma(studentID)

  if karma:
    academic_points = calculate_academic_score(studentID)
    # print("[karma.calculate_academic_points] Academic points: " + str(academic_points))
    karma.academicPoints = academic_points
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[karma.calculate_academic_points] Error occurred: academic score was not updated. ",
          str(e))
      db.session.rollback()
      return False
  else:
    return False


# calculate_total_points() is in the model itself
def update_total_points(studentID):
  karma = get_karma(studentID)
  if karma:
    #print("calculating total points of student: ", studentID)
    karma.points = karma.reviewsPoints
    db.session.commit()
    return True
  #print("student not found with id", studentID)
  return False


def update_review_points(studentID):
  karmaScore = Karma.query.filter_by(studentID=studentID).first()
  if karmaScore:
    karmaScore.reviewPoints = calculate_review_points(studentID)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print("[karma.update_karma] Error occurred while updating karma:",
            str(e))
      db.session.rollback()
      return False
  else:
    print("Karma score not found for student:", studentID)
    return False


#calculating ranks based on points
def calculate_ranks():
  karma = Karma.query.all()
  if karma:
    karma.sort(key=lambda x: x.points, reverse=True)
    print("calcing ranks")
    for i in range(len(karma)):
      karma[i].rank = i + 1
    try:
      db.session.commit()
      return True
    except Exception as e:
      print("[karma.calculate_rank] Error occurred while updating ranks:",
            str(e))
      db.session.rollback()
      return False
  else:
    print("Karma score not found")
    return False
