import os.path
import time
from accessConnection import get_session, Files, AbbyyServerJobs, FileConversions


import comtypes.client as cc

serverLocation = 'localhost'
workflowName = 'ComApiWorkflow'
client = cc.CreateObject("ABBYYFineReaderServer14.Client")
document = cc.CreateObject("ABBYYFineReaderServer14.JobDocument")

client.Connect(serverLocation)



workflows = client.Workflows

if workflows.Count == 0:
    raise Exception("No workflows available")

print("Available workflows:")

workflowFound = False
for i in range(0, workflows.Count):
    print("    %s" % (workflows.Item(i)))
    if workflows.Item(i) == workflowName:
        workflowFound = True

if not workflowFound:
    raise Exception("Workflow \"%s\" not found" % (workflowName))

import comtypes.gen.ABBYYFineReaderServer as clientTypeLib
session = get_session()






# files_to_process = session.query(Files).all()
# for each in files_to_process:
#     print(each.file_location)
#     jobId = client.ProcessFileAsync(os.path.realpath(each.file_location), workflowName)
#
#     newJob = AbbyyServerJobs(
#         jobId = jobId,
#         state = 'Active'
#     )
#     session.add(newJob)
#     session.commit()
#
#
#
# print(dir(document))
# print(document.Attributes.DocumentType)





# JobIdsQuery = session.query(AbbyyServerJobs).all()
#
# allJobIds = [JobIdQuery.jobId for JobIdQuery in JobIdsQuery]
#
