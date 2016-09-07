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
	return "Commands:\n\tnew note name: Makes a new note as name ie new note blank\n\tappend name; text: Appends text to note w/\"name\" ex append blank\n\tdisplay name: Disp the cont in note\n\tdelete line name: Del line from note then calls disp. ex delete 1 blank\n\tclear name: Clears the cont of note\n\tlist: Lists all notes"

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
    if (len(res) == 0):
	res = tokens[1] + " is empty"
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
	i += 1
    return res

if __name__ == '__main__':
    main()
