import os

def main():
    while(1):
        command = input('Please enter a command or help or stop: ')
        command = command.lower()
        if (command == "help") :
            print(Help())
        elif ("new note" in command and len(command.split()) == 3):
            print(newNote(command))
        elif ("list" in command):
            print(printNotes(command));
        elif ("append" in command):
            print(append(command))
        elif ("display" in command):
            print(display(command))
        elif ("delete" in command):
            print(delete(command))
        elif ("clear" in command):
            print(clear(command))
        elif ("stop" in command and len(command.split()) == 1):
            break
        else:
            print("Invalid command, type help for a list of commands")

def Help():
    print("Commands:\n\tnew note <note name>: Makes a new note with the name. ex new note blank\n\tappend <note name>; <text>: appends the text to the note with \"<note name>\" ex append blank\n\tdisplay <note name>: displays the content in the note. ex display blank\n\tdelete <line number> <note name>: deletes the line number from the note then calls display. ex delete 1 blank\n\tclear <note name>: clears the contents of the note. ex clear blank\n\tlist: lists all note names")

def newNote(command):
    name = command.split() 
    f = open('notes/'+name[2]+'.txt', 'w')
    f.close()
    return "Note created: " + name[2]

def append(command):
    tokens = command.split(';')
    names = tokens[0].split()
    if (len(names) != 2):
        return "Invalid Usage, type help for help"
    f = open('notes/'+names[1]+'.txt', 'a')
    f.write(tokens[1] + "\n")
    return "Appened \"" + tokens[1] + "\" to " + names[1]

def display(command):
    tokens = command.split()
    if (len(tokens) != 2):
        return "Invalid Usage, type help for help"
    try:
        f = open('notes/'+tokens[1]+'.txt', 'r')
    except FileNotFoundError:
        return "This note does not exist"
    i = 1
    res = ""
    for line in f:
        res += str(i)+". "+ line
        i += 1
    f.close()
    return res

def delete(command):
    tokens = command.split()
    if (len(tokens) != 3):
        return "Invalid Usage, type help for help"
    num = int(tokens[1])
    try:
        f = open('notes/'+tokens[2]+'.txt', 'r+')
    except FileNotFoundError:
        return "This note does not exist"
    lines = f.readlines()
    f.close()
    f = open('notes/'+tokens[2]+'.txt', 'w')
    count = 1
    for line in lines:
        if (count == num):
            count += 1
            continue
        f.write(line)
        count += 1
    f.close()
    return display("display " + tokens[2])

def clear(command):
    tokens = command.split()
    if (len(tokens) != 2):
        return "Invalid Usage, type help for help"
    f = open('notes/'+tokens[1]+'.txt', 'w')
    f.close()
    return "Cleared " + tokens[1]

def printNotes(command):
    tokens = command.split()
    if (len(tokens) != 1):
        return "Invalid Usage, type help for help"
    files = os.listdir('notes')
    i = 1
    res = ""
    for f in files:
        temp = f.split('.')
        res += str(i) + ". " + temp[0] + "\n"
    return res

if __name__ == '__main__':
    main()
