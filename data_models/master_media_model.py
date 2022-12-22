
from sqlalchemy import Integer, Column, ForeignKey
from base import Base



class MasterMediaRegister(Base):

    __tablename__ = 'master_media_register'
    id = Column(Integer(), primary_key=True)
    file_id = Column(Integer(), ForeignKey("files.id"))
    pdf_id = Column(Integer(), ForeignKey("media_pdf.id"))
    ms_word_id = Column(Integer(), ForeignKey("media_msword.id"))
    txt_id = Column(Integer(), ForeignKey("media_txt.id"))
    mp3_id = Column(Integer(), ForeignKey("media_mp3.id"))
    m4a_id = Column(Integer(), ForeignKey("media_m4a.id"))
    mp4_id = Column(Integer(), ForeignKey("media_mp4.id"))
    kurzweil_id = Column(Integer(), ForeignKey("media_kurzweil.id"))
    large_print_id = Column(Integer(), ForeignKey("media_large_print.id"))
    epub_id = Column(Integer(), ForeignKey("media_epub.id"))


class MediaPdf(Base):

    __tablename__ = 'media_pdf'
    id = Column(Integer(), primary_key=True)



class MediaMsword(Base):

    __tablename__ = 'media_msword'
    id = Column(Integer(), primary_key=True)



class MediaTxt(Base):

    __tablename__ = 'media_txt'
    id = Column(Integer(), primary_key=True)


class MediaMp3(Base):

    __tablename__ = 'media_mp3'
    id = Column(Integer(), primary_key=True)



class MediaM4a(Base):

    __tablename__ = 'media_m4a'
    id = Column(Integer(), primary_key=True)



class MediaMp4(Base):

    __tablename__ = 'media_mp4'
    id = Column(Integer(), primary_key=True)



class MediaKurzweil(Base):

    __tablename__ = 'media_kurzweil'
    id = Column(Integer(), primary_key=True)



class MediaLargePrint(Base):

    __tablename__ = 'media_large_print'
    id = Column(Integer(), primary_key=True)



class MediaEpub(Base):

    __tablename__ = 'media_epub'
    id = Column(Integer(), primary_key=True)

