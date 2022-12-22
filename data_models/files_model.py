from sqlalchemy import Integer, Column, String, ForeignKey

from base import Base

class TempCanvasFilesAssignment(Base):

    __tablename__ = 'temp_canvas_files_assignment'
    id = Column(Integer(), primary_key=True)
    file_id = Column(Integer(),  ForeignKey("files.id"))
    canvas_image_id = Column(Integer(),  ForeignKey("canvas_images.id"))
    canvas_documents_id = Column(Integer(),  ForeignKey("canvas_documents.id"))
    canvas_video_files_id = Column(Integer(),  ForeignKey("canvas_video_files.id"))
    canvas_audio_files_id = Column(Integer(),  ForeignKey("canvas_audio_files.id"))


class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_hash = Column(String())
    file_name = Column(String())
    file_location = Column(String())
    file_type = Column(String())
