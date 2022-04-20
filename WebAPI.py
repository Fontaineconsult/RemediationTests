import os
import os.path
import time

# pip install zeep
# see https://python-zeep.readthedocs.io/en/master/
import zeep

########### Configuration ############

# Location of ABBYY FineReader Server 14 Web Service
serviceUrl = 'http://localhost:8081/FineReaderServer14/WebService.asmx'

# Location of ABBYY FineReader Server 14 Server Manager relative to the
# machine where ABBYY FineReader Server 14 Web Service is installed
# If Server Manager and Web Service are installed on the same machine,
# this value should be localhost.
# This parameter is passed as an argument to all Web Service methods.
serverLocation = 'localhost'

# The name of the workflow to use
workflowName = 'MainWorkFlow'

# The path to the input file to process
filePath = "..\\..\\..\\..\\SampleImages\\sample.tif"

# The path to the directory in which output files will be saved
outputDirPath = ".\\Output"
########### Create server client from WSDL using zeep module ############

client = zeep.Client(wsdl=serviceUrl + '?wsdl')



def create_abbyy_job(filePath):

    dirPath, fileName = os.path.split(filePath)

    with open(filePath, "rb") as inputFile:
        fileContents = inputFile.read()

    fileContainer = {
        'FileContents': fileContents,
        'FileName': fileName
    }
    jobId = client.service.StartProcessFile(serverLocation, workflowName, fileContainer)

    return jobId


def check_abbyy_job_status(job_id):

    stateInfo = client.service.GetJobStateInfo(serverLocation, job_id)
    return stateInfo

def get_abbyy_job_result(abbyy_jobId):

    jobResult = client.service.GetJobResultEx(serverLocation, abbyy_jobId, None, ['DoNotDeleteJob'])
    print(jobResult['JobDocuments']['JobDocument'][0]['OutputDocuments']['OutputDocument'][0]['Files']['FileContainer'][0])
    return jobResult['JobDocuments']['JobDocument'][0]['OutputDocuments']['OutputDocument'][0]['Files']['FileContainer'][0]


def save_job_file(fileContainer, dirPath):
    with open(os.path.join(dirPath, fileContainer.FileName), "wb") as outputFile:
        outputFile.write(fileContainer.FileContents)



#
# ########### Get a list of available workflows and verify that workflowName is among them ##############
#
# workflows = client.service.GetWorkflows(serverLocation)
#
# if workflows.count == 0:
#     raise Exception("No workflows available")
#
# print("Available workflows:")
# for workflow in workflows:
#     print("  %s" % workflow)
#
# if not workflowName in workflows:
#     raise Exception("Workflow \"%s\" not found" % (workflowName))
#
# print("Using workflow: %s" % (workflowName))
#
# ########### Start file processing ##############
#
# dirPath, fileName = os.path.split(filePath)
# print("Starting processing of \"%s\"" %(fileName))
#
# # Files are sent as byte arrays
# with open(filePath, "rb") as inputFile:
#     fileContents = inputFile.read()
#
# fileContainer = {
#     'FileContents': fileContents,
#     'FileName': fileName
# }
# jobId = client.service.StartProcessFile(serverLocation, workflowName, fileContainer)
#
# print("Processing started, jobId = %s" %(jobId))
#
# ########### Query job state and wait until it is processed ##############
#
# print("Waiting until job is processed:")
#
# while True:
#     time.sleep(1)
#     stateInfo = client.service.GetJobStateInfo(serverLocation, jobId)
#     if stateInfo.State == 'JS_Complete':
#         print("  Job complete")
#         break
#     elif stateInfo.State == 'JS_NoSuchJob':
#         raise Exception("Job \"%s\" not found" % (jobId))
#     else:
#         print("  Job state is %s, %d%% complete" %(stateInfo.State, stateInfo.Progress))
#
########### Retrieve job result and print warnings and errors ##############

# If you do not specify DoNotDeleteJob flag you won't be able to retrieve job result
# the second time for the same job (this must be needed in case the first call
# fails due to network problem)
# If you do specify this flag, you must delete the job manually after you're done with it
# jobResult = client.service.GetJobResultEx(serverLocation, jobId, None, ['DoNotDeleteJob'])
#
# if jobResult.IsFailed:
#     print("Processing failed")
# else:
#     print("Processing succeeded")
#
# if jobResult.Messages != None:
#     print("Messages: ")
#     for message in jobResult.Messages.JobMessage:
#         print("  %s: %s" % (message.Type, message.UnicodeStr))
# #
# ########### Save output files ##############
#
# def saveFileContainer(fileContainer, dirPath):
#     with open(os.path.join(dirPath, fileContainer.FileName), "wb") as outputFile:
#         outputFile.write(fileContainer.FileContents)
#
# # Create separate output folder for a job
# jobDirPath = os.path.join(outputDirPath, jobId)
# if not os.path.exists(jobDirPath):
#     os.makedirs(jobDirPath)
# print("Results will be saved to %s" % (jobDirPath))
#
# # JobDocuments are created from input files based on Document Separation settings
# # OutputDocument is the result of exporting one JobDocument to one specific output format
# # Some output formats may produce more that one file
# # In case of "1 input file => 1 output file" there will be only one JobDocument for one input file
# # In case of only one export format there will be only one OutputDocument for one JobDocument
# # In case of PDF format there will be only one file FileContainer for one OutputDocument
# if jobResult.JobDocuments != None:
#     print("JobDocuments:")
#     for index, jobDocument in enumerate(jobResult.JobDocuments.JobDocument):
#         print("  [%d]:" % (index))
#         if jobDocument.OutputDocuments != None:
#             for outputDocument in jobDocument.OutputDocuments.OutputDocument:
#                 print("    OutputDocument for format \"%s\":" % (outputDocument.FileFormat))
#                 if outputDocument.Files != None:
#                     for fileContainer in outputDocument.Files.FileContainer:
#                         print("      %s" % (fileContainer.FileName))
#                         saveFileContainer(fileContainer, jobDirPath)
#
# # Some files may be copied to output without processing.
# # This includes files converted to PDF with office.
# # JobDocuments for such files are not generated, so OutputDocument
# # nodes will be created under corresponding InputFile nodes
# if jobResult.InputFiles != None:
#     print("InputFiles:")
#     for index, inputFile in enumerate(jobResult.InputFiles.InputFile):
#         if inputFile.OutputDocuments != None:
#             print("  [%d]:" % (index))
#             for outputDocument in inputFile.OutputDocuments.OutputDocument:
#                 print("    OutputDocument for format \"%s\":" % (outputDocument.FileFormat))
#                 if outputDocument.Files != None:
#                     for fileContainer in outputDocument.Files.FileContainer:
#                         print("      %s" % (fileContainer.FileName))
#                         saveFileContainer(fileContainer, jobDirPath)
#
# ########### Delete the job manually ##############
#
# client.service.DeleteJob(serverLocation, jobId)
# print("Job and files deleted")
#
# print("Successfully finished")
