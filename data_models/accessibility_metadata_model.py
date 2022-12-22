from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from base import Base


class AccessibilityMetaDataAssignment(Base):

    __tablename__ = 'accessibility_metadata_assignment'

    id = Column(Integer, primary_key=True)
    master_media_id = Column(Integer(), ForeignKey("master_media_register.id"))
    pdf_accessibility_meta = Column(Integer(), ForeignKey("pdf_accessibility_metadata.id"))
    msword_accessibility_meta = Column(Integer(), ForeignKey("msword_accessibility_metadata.id"))
    image_file_id = Column(Integer(), ForeignKey("images.id"))
    image_meta_id = Column(Integer(), ForeignKey("images_accessibility_metadata.id"))
    video_links_id = Column(Integer(), ForeignKey("video_links.id"))
    video_links_meta_id = Column(Integer(), ForeignKey("video_links_accessibility_metadata.id"))
    video_files_id = Column(Integer(), ForeignKey("video_files.id"))
    video_files_meta_id = Column(Integer(), ForeignKey("video_files_accessibility_metadata.id"))
    audio_links_id = Column(Integer(), ForeignKey("audio_links.id"))
    audio_links_meta_id = Column(Integer(), ForeignKey("audio_links_accessibility_metadata.id"))
    audio_files_id = Column(Integer(), ForeignKey("audio_files.id"))
    audio_files_meta_id = Column(Integer(), ForeignKey("audio_files_accessibility_metadata.id"))
    pseudo_content_id = Column(Integer(), ForeignKey("pseudo_content.id"))
    pseudo_content_meta_id = Column(Integer(), ForeignKey("pseudo_content_accessibility_metadata.id"))


class ImagesAccessibilityMeta(Base):

    __tablename__ = 'images_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class PDFAccessibilityMeta(Base):

    __tablename__ = 'pdf_accessibility_metadata'
    id = Column(Integer, primary_key=True)
    is_tagged = Column(Boolean(), default=False)
    text_type = Column(Integer())
    total_figures = Column(Integer())
    total_alt_tags = Column(Integer())
    has_doc_desc = Column(Boolean(), default=False)
    stage_folder = Column(String())
    title_set = Column(Boolean(), default=False)
    lang_set = Column(Boolean(), default=False)
    number_of_pages = Column(Integer())
    headings_pass = Column(Boolean(), default=False)
    has_bookmarks = Column(Boolean(), default=False)


class MSWordAccessibilityMeta(Base):

    __tablename__ = 'msword_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class VideoLinksAccessibilityMeta(Base):

    __tablename__ = 'video_links_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class VideoFilesAccessibilityMeta(Base):

    __tablename__ = 'video_files_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class AudioLinksAccessibilityMeta(Base):

    __tablename__ = 'audio_links_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class AudioFilesAccessibilityMeta(Base):

    __tablename__ = 'audio_files_accessibility_metadata'
    id = Column(Integer, primary_key=True)


class PseudoContentAccessibilityMeta(Base):

    __tablename__ = 'pseudo_content_accessibility_metadata'
    id = Column(Integer, primary_key=True)
