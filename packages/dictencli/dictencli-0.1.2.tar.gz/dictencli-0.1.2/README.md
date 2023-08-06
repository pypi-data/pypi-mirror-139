# dictencli

---

*A command line dictionary, for those who spend their day in terminal. Get definitons, origin, example and many more information inside your terminal. You are just one command away* 😊 ...

  

### Features

with functionalities like:

- word definition

- example

- origin

- synonyms

- antonyms

- phrases

- pronunciation

  

### Installation

`pip install dictencli`

  

#### Usage

`dictencli [commands] [optional flags] word(required with look command)`

  

##### **Commands:**

1. look - used with optional flags below provided.

`dictencli look word`

2. help - will just show you the help options dicussed above

`dictencli help`

3. about

`dictencli about`

  

##### **Optional flags:**

- orgin: use either '-origin' or '-or'

- example: use either '-example' or '-ex'

- synonyms: use either 'synonyms' or '-syn'

- antonyms: use either '-antonyms' or '-ant'

- pronunciation: use either '-pronunciation' or '-pro'

- phrases: use either '-phrases' or '-phr'

  
  

### Note

#### **Windows**

If pronunciation doesn't work:

`pip uninstall playsound`

`pip install playsound == 1.2.2`

  

unicode symbols might not be displayed correctly in cmd.

  

#### **Linux**

If pronunciation doesn't work:

`sudo apt install libgirepository1.0-dev`

`pip install pygobject`

  

Namespace Gst not available:

`sudo apt install python3-gst-1.0`

  

*These are the known issues that I had encountered in 'pronunciation', if you face any other issue or wan't to get in contact, feel free to mail at 'nikhilomkar99@gmail.com'. Thanks* 🙌🏻.

  

---