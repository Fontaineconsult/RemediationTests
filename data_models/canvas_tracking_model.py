from sqlalchemy import Integer, Column, String, DateTime, Boolean, ARRAY, LargeBinary

from base import Base

class CanvasImport(Base):

    __tablename__ = 'canvas_import'
    id = Column(Integer, primary_key=True)
    resource_type = Column(String())
    content_type = Column(String())
    downloadable = Column(Boolean(), default=True)
    is_hidden = Column(Boolean(), default=False)
    mime_type = Column(String())
    order = Column(Integer())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    uri = Column(String())
    course_id = Column(Integer())
    alt_tag_present = Column(Boolean(), default=False)
    semester = Column(String())
    course_gen_id = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))
    scan_object = Column(LargeBinary())


class CanvasImages(Base):

    __tablename__ = 'canvas_images'
    id = Column(Integer(), primary_key=True)
    uri = Column(String())
    resource_type = Column(String())
    content_type = Column(String())
    mime_type = Column(String())
    order = Column(Integer())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    canvas_id = Column(Integer())
    alt_tag_present = Column(Boolean(), default=False)
    semester = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))


class CanvasDocuments(Base):

    __tablename__ = 'canvas_documents'
    id = Column(Integer, primary_key=True)
    uri = Column(String())
    resource_type = Column(String())
    content_type = Column(String())
    mime_type = Column(String())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    canvas_id = Column(Integer())
    semester = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))

class CanvasVideoLinks(Base):

    __tablename__ = 'canvas_video_links'
    id = Column(Integer, primary_key=True)
    uri = Column(String())
    resource_type = Column(String())
    content_type = Column(String())
    mime_type = Column(String())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    canvas_id = Column(Integer())
    semester = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))

class CanvasVideoFiles(Base):

    __tablename__ = 'canvas_video_files'
    id = Column(Integer, primary_key=True)
    resource_type = Column(String())
    content_type = Column(String())
    mime_type = Column(String())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    canvas_id = Column(Integer())
    semester = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))

class CanvasAudioLinks(Base):

    __tablename__ = 'canvas_audio_links'
    id = Column(Integer, primary_key=True)
    uri = Column(String())
    resource_type = Column(String())
    content_type = Column(String())
    mime_type = Column(String())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    canvas_id = Column(Integer())
    semester = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))

class CanvasAudioFiles(Base):

    __tablename__ = 'canvas_audio_files'
    id = Column(Integer, primary_key=True)
    resource_type = Column(String())
    content_type = Column(String())
    mime_type = Column(String())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    canvas_id = Column(Integer())
    semester = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))

class CanvasPseudoContent(Base):

    __tablename__ = 'canvas_pseudo_content'
    id = Column(Integer, primary_key=True)
    uri = Column(String())
    resource_type = Column(String())
    content_type = Column(String())
    mime_type = Column(String())
    scan_date = Column(DateTime())
    source_page_title = Column(String())
    source_page_url = Column(String())
    title = Column(String())
    canvas_id = Column(Integer())
    semester = Column(String())
    page_component_count = Column(Integer())
    parent_url = Column(String())
    content_hidden = Column(String())
    content_path = Column(ARRAY(String()))
    title_path = Column(ARRAY(String()))


class CanvasScanBinaries(Base):

    __tablename__ = 'canvas_scan_binaries'
    id = Column(Integer, primary_key=True)
    scan_object = Column(LargeBinary())
    scan_date = Column(DateTime())
    canvas_id = Column(Integer())