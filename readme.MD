**Scamfinder-Pinterest**\
Scamfinder-Pinterest is a tool used for finding scammers numbers and active pages from pinterest.
It uses the pinterest search function to search the query you entered(i.e 'tech support') and attempt to parse a phone numbers from the results.

**Example Output**\
[29 days]Parsed nr: 6006188847702 - https://www.pinterest.com/pin/636766834799714695 - https://www.247tech****.us/fix-quickbooks-error-6006/

**How does it work?**\
It works by using the pinterest search mechanism and parsing the titles and descriptions of every given result.\
Example title: Pogo Technical Problems? Get Pogo Support Number 1 (234) 567 7890 \
The script parses the number from the title by cleaning and doing some more tricks.

**How do I use it?**\
In order to use it you must first create a Pinterest account.
https://pinterest.com
Paste your account email, password and username into the code.

**Dependencies**\
The script uses py3-pinterest - [https://github.com/bstoilov/py3-pinterest/](https://github.com/bstoilov/py3-pinterest/)
You can install py3-pinterest using pip.

     pip install py3-pinterest

or

    python -m pip install py3-pinterest

**How to run?**

    python scamfinder-pinterest.py
