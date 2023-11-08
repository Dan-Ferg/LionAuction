I started this project late and wasn't able to implement everything.

This app starts by routing to first.html where you have to option to load the database, enter your password userID and password,
or create a new user

The load database button routes to the loaddb() function. loaddb() creates a connection to my database, drops all tables,
creates tables i will use if they dont exist, runs through loops to populate each table from the csv's. Once loaded, the page
will tell you "Database loaded" and see a button which prompts you to go back. This should probably be invisible to the user
if the app were to launch.

For entering your password and userID, the html page routes you to the trylogin() function when you hit enter. It reads your
ID, hashes your password, and checks if theres a match in the users table. If successfull, you are logged in and redirected to
the start of the homepage (second.html), if not you are asked to enter a valid pair (third.html). trylogin() uses a helper
function valid_login(userID,hashedPass) to select users from the user table with the entered ID and hashed password.

The create new user button routes you to newuser which loades newuser.html. Here you can enter any user id and password
you want and are also prompted to select a role (bidder,seller,bidseller). If I had more time i would put more time into
only allowing correct user ID's to be entered (lsu domain and verified businesses)but right now anything goes.
Once create you hit the create user button with your information entered, you will be routed to /createnew and the
createuser()function runs. This adds your newly entered userid and hashed password into the users table and renders createbidder.html
createseller.html or createbidseller.html depending on what role you chose. Each of these basically functions the same,
asking you to enter your personal or business information and adding everything to the correct table (sellers,bidders, or both
tables). After this, you are redirected to the correct homepage for bidder/seller/bidseller. IF YOU GOT HERE BY LOGGING IN
NORMALLY, you are redirected to an inbetween page (second.html) which simply asks to load your homepage or logout. Clicking the
button to load your homepage routes you to /pagebyrole and the getPageForRole() function. This finds what role you are by
querying bidders/sellers tables and checking if its in one or both, then returning the correct homepage. Bidders, sellers, and
bidsellers.html are a all very similar, asking you to enter or edit more information you werent prompted to enter at the
beginning. Each field to enter/edit routes to an edit function that updates the table. There is also a button to load your 
info into the table shown, to review your information. This button routes you to the correct bidder/seller/bidseller load_info
functions which select the whole row in whatever database and sends that to the correct homepage to loop through
and display your information.

Finally, bidders and bidsellers have an extra button in their homepage to check current item listings. I did not have time
to implement actually bidding, but you can traverse through categories. The button to check biddings routes you to biddings
function. When first loaded (request.method=='GET'), the function makes a list of all parent category entries and removes the 
duplicates. Then it sends this list to biddings.html where it loops through each parent category and presents each
in a table. Clicking on any parent category triggers a javascript on click event that basically just routes to bidding again,
but now with request.method "POST" and also creates and sends a variable of the category to the python code. Now in method
"post", it strips the extra characters from what you clicked so it can search again under that category. It saves the category
you picked and the subcategories that correspond to it to the session (imported from flask). Now it routes to /sub_category
goto_subcat() function. On method=="get" it loads data and subcategory mentioned, loads subcategory.html, sending selected
category (data) and corresponding subcat's with it. Subcategory basically works the same way as category html, showing 
what sub categories you can pick, and directing you to that when clicked. Anywhere along the line you can click show listings
which will route to /show_listings and show_listing function that checks the database for all listings under the selected 
category type. It sends relevant data to show_listings.html and it presents it there.