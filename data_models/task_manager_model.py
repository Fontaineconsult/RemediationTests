
from sqlalchemy import Integer, Column, String,  ForeignKey
from base import Base
from sqlalchemy.dialects.postgresql import ENUM

class RemediationTaskQueue(Base):

    __tablename__ = 'remediation_task_queue'
    id = Column(Integer(), primary_key=True)
    stage = Column(ENUM('Open', 'Working', 'Complete', 'Cancelled', 'On Hold'))


class ReviewTaskQueue(Base):

    __tablename__ = 'review_task_queue'
    id = Column(Integer(), primary_key=True)
    stage = Column(ENUM('Open', 'Reviewing', 'Remediating', 'Reviewed',  'Cancelled', 'On Hold'))
    result = Column(ENUM('Open', 'Passed', 'Failed'))


class ReviewToRemediationAssignment(Base):

    __tablename__ = 'review_to_remediation_assignment'
    id = Column(Integer(), primary_key=True)
    review_id = Column(Integer(), ForeignKey("pseudo_content.id"))
    remediation_id = Column(Integer(), ForeignKey("pseudo_content.id"))