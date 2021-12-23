## 20-books Client Instruction Manual
This user manual provides a basic understanding of the client application's capabilities.<br/>
See README.md for instructions on setting up the client application. 
<br/>
<br/>

### Homepage
After starting the application, user will arrive at the homepage. A user will be presented with the following options:
```sh
lookup a book                  f
borrow a book                  b
publish a book                 p
review a book                  r
checkout a book                c
recommand a book               e
exit                           q
```
The user may select any option by typing in their respective character key, then press ENTER. 
If the user failed to select a valid option, the application will prompt the user to try again.
At any point in time, the user may quit the application by pressing CTRL C

<br/>
<br/>

### Looking Up A Book
One of the most common use case of the client application is looking up a book from our database. 
This application allows users to mix and match multiple search criterias.
Upon enter the lookup page, the user will be presented with the following options:
```sh
ISBN number                    i
book title                     t
author full name               n
publisher name                 p
publication year               y
publication month              m
publication day                d
language code                  u
MIN number of pages            c
MIN average score              r
complete criteria selection    x
```
To specify a criteria, simply type the option character and press enter<br/>
For example, if the user want to search books by review score, he/she may enter R<br/>
```sh
Select criteria: r
```
Once an option is selected, the user will be asked to specify a valid condition. 
In the case of an review score, for example, only a floating point values will be accepted:<br/>

```sh
Enter MIN average score: 4.5
```
Once a search criteria is specified, the user may add additional search critieras, or simply redefine his/her previous criterias. For example, if the user want to want to also filter by title, the user may enter T, and then enter the title of the book:
```sh
Select criteria: t
Enter book title: database
```
For titles, the client will automatically perform fuzzy matching to provide better results. For certain other search criterias, the client will also perform automatic input conversions. For example, the client application will automatically convert ISBN10 to ISBN13.

Once the user has specified all criterias he/she needs, the user may press X to complete the criteria selection. <br/>
_note: at least one criteria must be entered to preform the search_

```sh
--------------------------------------------------------------------------------------------------------------------------
ISBN13         Title    Author              Publisher           Score   Language  Pages     Publication Dat
9780071613705  Applied Oracle Security: ...  David C. Knox       McGraw-Hill Educat  4.0     ENG       610       01 Oct 2009
9780072231304  Effective Oracle Database...  David C. Knox       McGraw-Hill Educat  3.69    ENG       512       08 Jul 2004
9780120887996  Moving Objects Databases      Ralf Hartmut Gütin  Morgan Kaufmann Pu  4.5     ENG       389       23 Aug 2005
9780130353009  A First Course in Databas...  Jeffrey D. Ullman   Prentice Hall       3.55    ENG       528       12 Oct 2001
9780201107159  Concurrency Control and R...  Philip A. Bernstei  Addison Wesley Pub  4.17    ENG       370       01 Jan 1987
9780201537710  Foundations of Databases:...  Richard G. Hull     Pearson             4.43    ENG       704       02 Dec 1994
9780321204486  Fundamentals of Database ...  Ramez Elmasri       Addison Wesley      3.81    ENG       1009      21 Aug 2003
9780470101865  Wiley Pathways Introducti...  Mark L. Gillenson   Wiley               3.56    ENG       478       01 Feb 2007
9780596002732  Access Database Design & ...  Steven Roman        O'Reilly Media      3.6     ENG       448       17 Jan 2002
9780976830221  Tera-Tom on Teradata Data...  Tom Coffing         Coffing Publishing  3.52    ENG       312       01 Nov 2004
--------------------------------------------------------------------------------------------------------------------------
<!> too many results, showing the first 10 matches...
```

_note: if the number of results returned exceeds 10, the application will only show the first 10 records_<br/>


<br/>
<br/>

### Reviewing A Book
A user may wish to add a review to a title. To do so, the user must first enter his/her interger userID. For example, 5400. After entering a userID, the user will be redirected to the lookup page to select one ISBN book. Once the book is selected, the user will be prompted to add a rating for the ISBN book:
```sh
did not like it                1
it was ok                      2
liked it                       3
really liked it                4
it was amazing                 5
```
Once a valid rating is added, the review will be published to our database. 

<br/>
<br/>

### Borrowing A Book
A user may wish to borrow a book. To do so, the user must input either the library BibNumber or a valid ISBN number. Upon enter the book's identifier, the application will list the item's avalibility and location as well as the last checkout date of any physical copies of the book. For example:
```sh
--------------------------------------------------------------------------------------------------------------------------
BibNumber           WHERE TO FIND IT              Type        Collection  Location    Report Date         Count
29747               Central Library, 1000 4TH AV  acbk        canf        cen         2017-09-01          1
--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
Barcode  Last Checkout Time
1004459232017-08-08 12:16:00
--------------------------------------------------------------------------------------------------------------------------
```

<br/>
<br/>

### Checking Out A Book
This is the final step to borrow a book. A user can check out any book with a physical barcode. The application will prompt the user for a valid barcode and upon receiving a valid input, the application will add a new checkout record to the database with checkout time set to the current time. 

<br/>
<br/>

### Publishing Out A Book
This is designed for users who wish to add a new ISBN book to our database. After loading the page, the user will be prompted to enter various attributes of the ISBN book. The application will ensure the correctness of user inputs, in addition to the uniqueness of the ISBN edition. (In other words, if there already exists a record in our database, the user may not add a duplicate). For example:
```sh
lets start by entering some required information for your book...
Enter ISBN13 (or ISBN10): 9780552993692
Enter book title: paul ward's dumpster fire database
Enter author name(or enter nothing to skip): Jeff Zarnett
Enter publisher name(or enter nothing to skip): University of Waterloo
Enter number of pages: 2434
Enter language code (eg. ENG): ENG
Enter publication year: 2022
Enter publication month(or enter nothing to skip): 12
Enter publication day(or enter nothing to skip):
are you sure you want to publish the book paul ward's dumpster fire database ? (y/n):
```


<br/>
<br/>

### Recommanding A Book
The application has the capability to recommand a user new books based on his/her existing ratings of books. The recommandation engine works by finding books that the user has not read before, and that is highly liked by users who share similar taste to the current user. Recommandation weighting depends both on the degree of overlap of the taste of similar users as well as the number of similar users who enjoyed a certain book that may be recommanded. The application will only show the top 20 recommandations. Here is an example of the recommandation engine in action:
```sh
Enter your userId: 10986
here are some of the books you liked in the past, we will find recommandations based on these
--------------------------------------------------------------------------------------------------------------------------
ISBN13              Your Rating    Title
9780030957673       4              The Return of the Native
9780060172220       4              Cosette: The Sequel to Les Miserables
9780060467210       4              Adventures of Huckleberry Finn
9780099428640       5              The Trial
9780099511540       4              Heart of Darkness
9780140005295       5              Lord Jim
9780140009071       5              The Trial
9780140038835       4              Daisy Miller
9780140186222       5              The Trial
9780140281637       4              Heart of Darkness
--------------------------------------------------------------------------------------------------------------------------
looking for recommandations, please wait...

:) based on books you really liked, here is our top recommandations:
--------------------------------------------------------------------------------------------------------------------------
ISBN13         Title                        Author              Publisher           Score   Language  Pages     Publication 
9780060740450  One Hundred Years of Sol...  Gabriel García Már  Harper Perennial    4.07    ENG       458       20 Jan 2004
9780141321097  The Adventures of Huckle...  Mark Twain          Puffin              3.82    ENG       466       06 Mar 2008
9780140012484  The Catcher in the Rye       J.D. Salinger       Penguin Books       3.8     ENG       220       01 Nov 1986
9780060173227  To Kill a Mockingbird        Harper Lee          HarperCollins Publ  4.28    ENG       323       01 Sep 1995
9780060735555  Slaughterhouse-Five          Kurt Vonnegut Jr.   Harper Audio        4.08    ENG       6         11 Nov 2003
9780075535751  The Brothers Karamazov       Fyodor Dostoyevsky  Random House, Inc.  4.32    ENG       940       01 Sep 1950
9780140185546  Dubliners                    James Joyce         Penguin Books       3.85    ???       317       05 Nov 1992
9780176048136  Hamlet                       William Shakespear  Thomson South-West  4.02    ???       208       02 Dec 2005
9780020198826  The Great Gatsby             F. Scott Fitzgeral  Scribner            3.92    ???       193       01 Jun 1992
9780345294661  Fahrenheit 451               Ray Bradbury        Del Rey             3.99    ???       167       12 Feb 1981
9780007258055  Macbeth                      William Shakespear  HarperCollins Publ  3.9     ENG       264       23 May 2007
9780140620658  King Lear                    William Shakespear  Penguin Ltd.        3.91    EN-GB     160       28 Apr 1994
9780198319955  Othello                      William Shakespear  Oxford University   3.9     ???       162       01 Jan 1996
9780571229116  Waiting for Godot            Samuel Beckett      Faber and Faber     3.83    EN-GB     87        05 Jan 2006
9780140447231  Anna Karenina                Leo Tolstoy         Penguin Books Ltd   4.05    ENG       864       06 Dec 2001
9780142437209  Jane Eyre                    Charlotte Brontë    Penguin             4.12    ENG       532       04 Feb 2003
9780020518709  The Sun Also Rises           Ernest Hemingway    Collier Books; Mac  3.82    ENG       247       01 Mar 1987
9780399502675  Lolita                       Vladimir Nabokov    Perigee Trade       3.89    ???       320       17 Aug 1972
9780140455366  The Odyssey                  Homer               Penguin Classics    3.77    ENG       416       29 Aug 2006
9780194228787  The Adventures of Tom Sawyer Nick Bullard        Oxford University   4.1     ENG       44        01 Jan 1999
--------------------------------------------------------------------------------------------------------------------------
```

