import glob, os, hashlib
from accessConnection import get_session, Files, Videos, ConversionRequests

home = "Z:\ACRS\Requests"

def importFilesFromDisk(request_id):

    hasher = hashlib.sha256()
    session = get_session()

    request = session.query(ConversionRequests).filter_by(id=request_id).first()
    import_folder = os.path.join(home, request.import_folder)
    conversion_requester = request.conversion_requester
    files = glob.glob(import_folder + '\**' + '\*.pdf', recursive=True)

    for file in files:

        if os.path.isfile(file):
            with open(file, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
                file_hash = hasher.hexdigest()
        file_exists = session.query(Files).filter_by(file_location=file).first()

        if not file_exists:
            file = Files(
                file_hash = hasher.hexdigest(),
                file_name = os.path.basename(file),
                file_location = file,
                file_type = os.path.splitext(file)[1],
                origin_requester_id=conversion_requester
            )
            session.add(file)
            session.commit()
            session.close()


