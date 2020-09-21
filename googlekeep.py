
import gkeepapi

keep = gkeepapi.Keep()


# create note with keep
def createNote(title, list, email, password):
    success = keep.login(email, password)
    # check if the note with that title exists
    note = keep.find(query=title)
    for n in note:
        # delete old content
        n.delete()
    glist = keep.createList(title, list)
    glist.pinned = True
    glist.color = gkeepapi.node.ColorValue.Red
    keep.sync()
    return True

