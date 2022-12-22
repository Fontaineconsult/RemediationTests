from sqlalchemy import Integer, Column, ForeignKey
from base import Base


class CanvasReviewRequests(Base):

    __tablename__ = 'canvas_review_requests'
    id = Column(Integer(), primary_key=True)
    requester_id = Column(Integer(),  ForeignKey("requester.id"))


class CanvasReviewContentAssignments(Base):

    __tablename__ = 'canvas_conversion_assignments'
    id = Column(Integer(), primary_key=True)
    review_id = Column(Integer(),  ForeignKey("canvas_review_requests.id"))
    accessibility_metadata_assignment_id = Column(Integer(), ForeignKey("accessibility_metadata_assignment.id"))