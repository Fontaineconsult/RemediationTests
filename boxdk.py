from boxsdk import OAuth2, Client, object
import os
auth = OAuth2(

    client_id="zamp86vr1wge5m2p5txtmwiyv0sfwtes",
    client_secret="zamp86vr1wge5m2p5txtmwiyv0sfwtes",
    access_token="trGACGmilwkOZgtcAGvhzTKpD4jqQ90u" #expires after 60 min


)


auth_json = {
    "boxAppSettings": {
        "clientID": "zamp86vr1wge5m2p5txtmwiyv0sfwtes",
        "clientSecret": "clypFeeezcp48KDE8rUEuLtaSzjHDqTd",
        "appAuth": {
            "publicKeyID": "",
            "privateKey": "",
            "passphrase": ""
        }
    },
    "enterpriseID": "281439"
}


client = Client(auth)


# https://sfsu.app.box.com/s/dk0bwi0aslvsyup7df94hj5xvluvx4xq


download_drive = "Z:/ACRS/Requests"

test = client.get_shared_item('https://sfsu.app.box.com/s/vhq2kb23k9hruk0wpv3v49103i6sz7oc')


# items = test.get_items()


print(test.response_object)


# def walk_box_folders(item, path):
#
#     if item.type == 'file':
#         location = download_drive + path + item.name
#         location = os.path.normpath(location)
#         print(location)
#         print(dir(item.get()))
#         download = client.file("865878726485").content()
#         with open(item.name, 'wb') as f:
#             print(dir(item))
#
#             f.write(download)
#             f.close()
#
#     if item.type == 'folder':
#
#         for new_item in item.get_items():
#             location = path + item.name + "/"
#             walk_box_folders(new_item, location)
#
#
#
# walk_box_folders(test, '/')