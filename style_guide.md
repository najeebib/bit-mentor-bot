
## Code Lay-out

### 1.1 Indentation

* Use 4 spaces per indentation level.
```python
def start(update: Update, context: CallbackContext) -> None:  
    update.message.reply_text('Hello ! This is your bot')``
```
### 1.2 Maximum Line Length

* Limit all lines to a maximum of 79 characters.
### 1.3 Blank Lines
* Use two blank lines between method definitions inside a class. 

```python
	def method_one(self): 
	
	
	def method_two(self): 
```
	
### 1.4 **Imports**

-   Imports should be on separate lines.
-   Group imports into three categories: standard library imports, related third-party imports, and local application/library-specific imports.
```python
import os
import sys

from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext

from my_bot.handlers import start_handler

```
---

## Naming

2.1 **Variables and Functions**
* Use lowercase words separated by underscores. (snake_case)
```python
def process_message(update, context): 
	message_text = update.message.text

```

2.2 **Constants**
* Use all uppercase letters with underscores separating words.
	
```python
TOKEN = "YOUR_BOT_TOKEN"
```
---

2.3 **Class**
* Class names should normally use the CapWords convention.
```python
Class PokemonTrainer:
```

## Comments and Documentation

### 3.1 Docstrings:
*  Use triple double quotes for docstrings.
```python
def start(update: Update, context: CallbackContext) -> None:
"""
This function sends a welcome message to the user
 when they start a chat with the bot or send the /start command.

 Args: update
  (Update): An object representing the incoming update. Contains the message details.
   context (CallbackContext): An object containing additional context for the callback, 
   including bot data and user data.
    Returns: None """
"""
 update.message.reply_text('Hello ! This is your bot')
```


### 3.2 **Inline Comments**

* Use inline comments sparingly and ensure they are clear and concise.
```python
message = update.message.text # Get the text of the incoming message
```
---
## Error Handling
* Use specific exceptions rather than a general `except`.
```python
try:
    response = some_function()
except ValueError as e:
    logging.error(f"ValueError occurred: {e}")

```
