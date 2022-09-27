# ATHRIC - THE PROJECT YOU CAN'T MISS OUT
An intelligent software created by [Obed Amoako](https://ericob.sytes.net)

![Screenshot (41)](https://user-images.githubusercontent.com/84608830/190366532-233b8ee9-2bcf-4e62-9bcf-e9156821e654.png)

## ⚡Important Notice ⚠
Athric is a web application I built for an Agric institution in the Ghana Ministry of Food and Agriculture.  
This is a real world project. Therefore, for security and privacy reasons, some files like `models.py`, `app.db`, and some lines in `routes.py`, `base.html`, and static files like `images` and `videos` are not checked to source control.

> Setup and Installation NOT given out

## Demo videos
Watch live demos of every page (over 22 pages) in the links below
>  
> [**Part One - Youtube**](https://youtu.be/z3FIbhvlzHQ)  
> [**Part Two - Youtube**](https://youtu.be/HsVuH_rm3P4)  
> [**Part Three - Google Drive**](https://drive.google.com/file/d/1xeSTLRd2YX76gzrIRFyrupTgy-YEpwwP/view?usp=sharing)  
>  

## How To Use - Non-exhaustive

> Updated UI for `Users` page: 27/09/2022

### The Home Page
 It displays a slideshow of images with some brief informations about athric and some quick navigations
 - The top 3 most viewed articles display in the home page as popular articles
 - You can open particular categories of articles and files from the home page with one click
 - You can also contact the athric team in the home page (if you are not a staff)
 - You can request for a staff account in from the footer if you are not a staff
 - When logged out, you will see a `sign up` and `sign in` buttons expecting you to take action
 - If you are logged in and you are a staff, your role will display in the bar above the page. Else, an info about athric

#### Sidebar and titlebar
  The sidebar is the main navigation bar
  - It displays `Home`, `Notice`, `Articles`, `Files`, `User`, and `Login` navigation links
  - The `Articles`, `Files`, and `User` are not direct links. They are dropdown buttons
  - The `Articles` button opens a dropdown menu of all the article categories and a link to all articles
  - The `Files` button opens a dropdown menu of all the file categories
  - The `User` button opens a dropdown menu of User profile link, All users link, and a Logout link
  - The Title Bar contains a link to the home page on the left. Content: Site name and (Current user's role or an info about the site)
  - The title bar also contains the title of the current page on the right
 
 ![Screenshot (42)](https://user-images.githubusercontent.com/84608830/190368968-3e0e6f51-d3b9-47d8-a6ac-bdebc21c52be.png)
 
 ### Has a simple 404 Page
 ![Screenshot (48)](https://user-images.githubusercontent.com/84608830/190393299-0d213934-5e14-468f-8e78-b12f6b7b9cab.png)
 
 ### Has a nice UI on small-size media
 
 ![Screenshot (47)](https://user-images.githubusercontent.com/84608830/190384360-c3b5329a-c6e0-4e9c-a6df-e66e258fdbae.png)

 
 ### The Notice Board
 It displays notices for only staff members. Not ordinary users
  - Notices that are automatically created (either by someone sending a message form `Contact Us` or someone requesting an account) dark themes
  - *New notices (except account requests) are sent to all staff in their emails immediately*. Contact messages from users are received by **admins only**
  - If you are an administrator or you are the author of a particular notice, there will be an ellipsis icon on which you can click to view a dropdown of Edit and Delete buttons to take actions on the notice
  - Those notices can only be seen by the administrators
  - To create a new notice, you can click on the floating `+` icon on the notices page to do so
  - Notices that are deliberately created by a staff have a blue theme
  - Notices are paginated. They are displayed 4 notices per page. You can click on a page number or `Next` and `Prev` buttons to select a page
  - You will see `- Contact` appended to the title of a message from `Contact us` page [ Update: now `(Contact)` not ` - Contact`]
  
  ![Screenshot (31)](https://user-images.githubusercontent.com/84608830/190374842-42aa8076-d303-4ad9-b936-bf6e8de74db5.png)

### Articles
The articles page displays a list of articles created on the site ordered by date in a descending order, paginated into 8 items per page
- You can click on the Next and Prev or a page's number to view a particular article page
- The articles list displays a preview of the article's cover image, a truncated (if long) article title, and a part of the article's message content
- You can click on an article to read it.
- To create a new article, you can click on the floating `+` icon on the articles page to complete that
- If you are an administrator or you are the author of a particular article, there will be an ellipsis icon on which you can click to view a dropdown of Edit and Delete buttons to take actions on the article
- The articles page contains a **Search Bar** in which you can type some keywords to search for articles. There is a grammatical display of the number of articles containing your search
- You can search a particular category of articles to view them
![Screenshot (29)](https://user-images.githubusercontent.com/84608830/190383052-8473fdfe-ef26-414d-9154-9bd2cee67bcd.png)

#### Article categories
- The articles are categorized into different types. Users select which category an article fall into when creating them.
- You can click on the articles button on the sidebar to select which category you want
- If you prefer, you can search the name of a particular category to view all its articles
- on small media, a search icon will display in the navigation bar, which you can select to display the search bar and start typing

![Screenshot (44)](https://user-images.githubusercontent.com/84608830/190378796-55032da0-2cd4-4151-8c59-b7d85b69ee3f.png)


### Files
This is a function that allows staff to upload files such as Images, Videos, and Documents
 - There is no route to view all files in one page
 - You can select an image, video, or a ducument from the dropdown that shows when you click on the `Files` icon
 - You can also view a particular category of files by selecting in the home page
 - A page called Gallery displays a category of file when you select.
 - When viewing the gallery of a particular file, you can click on the `❌` icon to delete (if you are an admin or you created it). You will need to confirm you want to delete it.
 - When viewing videos or documents, you will need to select its name to view full details. You can click on an image to view its details
 - You can play a video in the gallery page. But you cannot see its description from there.
 - You can also view a document from the gallery page, but opens crearly when its name is selected.
 - Documents do not require any descriptions.
 - When you click on a video or an image, its full title, description, author, date, etc. will show up
 - When viewing an image or a video, you can see some links to other videos, images, and documennts below in the page. The current file is not listed. Files listed in each category are up to 3.
 - You can delete a file when viewing as well as upload a new file
 - You can click on the floating `back` Icon on the left to move one step back
 
![Screenshot (35)](https://user-images.githubusercontent.com/84608830/190385043-6def8e2e-f5c4-4729-b698-1b46f1f875c7.png)


### Users
You can view/edit your profile, view all users and their details, reset users' password, delete users, add users, etc. SEE HOW
- To modify your profile, you can click on the User icon on the navigation bar and select `Edit your account`
- When editing your account, you can change your name, email, phone, and password
- You will need to be a staff to view a list of all users
- You will need to be an administrator to delete, add, or reset a user's password
- If you are an administrator, you will see a trash icon and a 🔄 on the users. (trash icon won't show for administrators)
- When the trash icon or the reset icon is selected, you will be asked to confirm to delete or reset the user's password respectively
- The reset icon will not show for the current user. A pencil that directs you to edit your account rather
- The current user will see `(You)` appended to his name to indicate his account in the list
- To  add a new user, click on the ➕ icon floating on the right and fill the form
![Screenshot (52)](https://user-images.githubusercontent.com/84608830/192594842-022441ca-c9d1-482f-b2d5-9bee0a9fd778.png)

### Requesting for a staff account
Click on the **Request An Acocunt** Link in the footer (will show if you're not a staff)  
You will need to submit the form for that  

###  Contacting the administrators 
Click on the **Contact us** Link in the footer (will show if you're not a staff)  
You will need to submit the form for that as well

  
&nbsp;&nbsp;  
Thank you for taking time to read to this end. Did you view the videos above? Find them [here](#demo-videos)
## Learn more about me
[#Obed Amoako](https://ericob.sytes.net) Software engineer, since May 2022  
  
>> Please leave a star on this repository 🌟
