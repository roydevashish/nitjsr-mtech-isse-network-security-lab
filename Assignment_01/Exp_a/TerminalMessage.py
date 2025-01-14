import colorama as CM

terminalIcon = "[>]"

def PrintTry(status:bool, message:str):
    '''
        TODO: Function description
    '''

    if(status):
        statusMessage = "Success"
        color = CM.Fore.GREEN
    else:
        statusMessage = "Error"
        color = CM.Fore.RED

    print(color + f"{terminalIcon} {statusMessage}: {message}")

def PrintMessage(message:str):
    '''
        TODO: Function description
    '''

    print(CM.Fore.BLACK + f"{terminalIcon} {message}")