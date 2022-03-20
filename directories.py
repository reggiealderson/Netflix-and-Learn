def get_directory(language, show, filetype):

    show_u = show.replace(" ", "_")
    direc = f"{language}/{filetype}/{show_u}__show"

    return str(direc)

def get_main_show_image(directory, show):

    show_u = show.replace(" ", "_")
    dir1 = directory
    
    return f"{dir1}/{show_u}.jpg"
