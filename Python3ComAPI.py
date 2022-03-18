import os.path
import time

# pip install comtypes
import comtypes.client as cc

########### Configuration ############

# Location of ABBYY FineReader Server 14 Server Manager
serverLocation = 'localhost'

# The name of the workflow to use
workflowName = 'ComApiWorkflow'

# The path to the input file to process
filePath = r"Z:\ACRS\Requests\New folder\Naipaul on Indonesian Islam.pdf"

########### Create a client and connect to server ############

client = cc.CreateObject("ABBYYFineReaderServer14.Client")
client.Connect(serverLocation)

# Import the auto-generated module to access enum values from type library
import comtypes.gen.ABBYYFineReaderServer as clientTypeLib

########### Get a list of available workflows and verify that workflowName is among them ##############

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

print("Using workflow: %s" % (workflowName))

########### Start file processing ##############

# Resolve path before calling ProcessFileAsync method
print("Starting processing of \"%s\"" %(filePath))
jobId = client.ProcessFileAsync(os.path.realpath(filePath), workflowName)

print("Processing started, jobId = %s" %(jobId))

########### Query job state and wait until it is processed ##############

print("Waiting until job is processed:")

while True:
    time.sleep(1)
    state, progress = client.GetJobState(jobId)
    if state == clientTypeLib.JS_Complete:
        print("  Job complete")
        break
    elif state == clientTypeLib.JS_NoSuchJob:
        raise Exception("Job \"%s\" not found" % (jobId))
    else:
        print("  Job state is %d, %d%% complete" %(state, progress))

########### Retrieve job result and print it ##############

xmlResult = client.GetJobResult(jobId)

if xmlResult.IsFailed:
    print("Processing failed!")
else:
    print("Processing succeeded!")

def printOutputDocuments(outputDocuments):
    for i in range(0, outputDocuments.Count):
        outputDocument = outputDocuments.Item(i)
        outputLocation = outputDocument.OutputLocation
        fileNames = outputDocument.FileNames
        for j in range(0, fileNames.Count):
            fullPath = os.path.join(outputLocation, fileNames.Item(j))
            print("    %s" % (fullPath))

print("Output documents for input files:")
inputFiles = xmlResult.InputFiles
for i in range(0, inputFiles.Count):
    inputFile = inputFiles.Item(i)
    print("  %s:" % (inputFile.FileName))
    printOutputDocuments(inputFile.OutputDocuments)

print("Output documents for job documents:")
jobDocuments = xmlResult.JobDocuments
for i in range(0, jobDocuments.Count):
    jobDocument = jobDocuments.Item(i)
    print("  %s:" % (jobDocument.Name))
    printOutputDocuments(jobDocument.OutputDocuments)

########### Delete the job and files after they are no longer needed ##############

client.DeleteJob(jobId)
print("Job and files deleted")

print("Successfully finished")
