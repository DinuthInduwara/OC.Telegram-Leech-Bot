from Bot_Client import UploadCLI
import os

if __name__ == "__main__":
    print("Bot Ready TO Use!")
    if not os.path.isdir('downloads'):  
        os.makedirs('downloads')
    if not os.path.isdir('Bot_Client/plugins/requirements'):  
        os.makedirs('Bot_Client/plugins/requirements')
    UploadCLI.run()



