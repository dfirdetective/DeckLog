# DeckLog
A simple method to create a log of whatever you like from your Stream Deck! Good for bullet journaling, habit tracking, or time tracking.

![image](https://github.com/user-attachments/assets/acbe123f-5304-479d-bffc-5e9ebd2e3cc1)  
*(Deck Emojis from the Free 3D Teams Emojis pack)*

# Usage
Each button uses the System > Open functionality to open the DeckLog.py script or DeckLog.exe executable and passes a one word argument. The argument comes from the `prompts.json` file. 
Example: `C:\Users\User\Documents\DeckLog\DeckLog.py Meal` will provide a pop up with the Meal prompts. Can be run from the command line as well for any hotkey usage using the same method.
![image](https://github.com/user-attachments/assets/77fdae39-02d2-4704-abfe-226ad9a3cd9e)  
This prompt will auto-focus, allow you to use Tab to go to the next input box, and use Enter to submit.  
![image](https://github.com/user-attachments/assets/e9cf845c-6855-4d99-841b-fbcae0b27fc7)  
The output file will look similar to this depending on changes to your configuration.  

# DeckLog Setup
If using the python script, the requirements are Python 3 and tkinter for the pop-ups.  
If using the executable, simply download `DeckLog.exe`  
Output CSV files will go to the location that the script is running from. A suggested set up would be a Desktop or Documents folder named `DeckLog` that contains the py/exe and the `deck_log.csv` will output to the same folder.  
Open StreamDeck Configuration, choose an unused button location and add an `Open` button. Title it however you like and select the py/exe file as the App/File and add the prompt argument to the end. Ex: Title: Meal App/File: `C:\User\User\Documents\DeckLog.exe Meal` Repeat this for however many buttons/prompts you would like to have their own button.   
With your last button slot, I recommend adding the `List` button (Ex: `C:\User\User\Documents\DeckLog.exe List`) which will list all of the prompts in the `prompts.json` in a drop down for your selection allowing you to see those less used/important prompts.  

# `prompts.json`
This file is what defines what your pop-up will prompt you for, how many prompts it will provide, and what column it will output to in your output csv.  
```
"CLIArgument": [
    ["OutputColumn", "PopupPrompt?"]
  ]
```
For example, the default `Meal` prompt will provide 3 prompts. `What meal is this?` will be logged to the `Reason` column, `What did you eat?` will go to the `Log` column, etc.   
```
"Meal": [
      ["Reason", "What meal is this?"],
      ["Log", "What did you eat?"],
      ["Quality", "What was the quality of this food?"]
    ]
```
When customizing prompts.json, you can create new columns if the default `Reason`, `Log`, `Quantity`, and `Quality` are not enough or you'd like more specific separation. You can also pre-create the output file or rearrange the header rows in the way you prefer once created.  
If you use the exe, you will not be able to customize the prompts at this point. However, it is something I could implement, if interested. You **can** rearranged the output file headers.  

# Basic Troubleshooting
**I'm getting an access error for the CSV file. Help?**  
The CSV file cannot be open while the script is trying to write to it. Make sure you close the CSV before logging more data.  
**Hitting Enter submits the input before I'm ready!**  
That is by design. This is not intended as a full journalling tool but quick prompt answers with no "new lines".  
