# Films & Serials Database
## 1. **About**
* App name: Digital library of films and serials
* Developer: Vadim Zhur
* Group: 153501

## 2. **Functional requirements**
* User authorization
* User management (CRUD)
* Role system: admins and users
* History of user actions
* After authorization user can:
   * look for a film
   * get some info about the film
   * give a rating to the film
   * watch history of actions
* After authorization admins can:
   * the same as users
   * get info about users
   * manage users (CRUD)

## 3. **List of tables**
1. ### FilmsSerials Table (One-to-Many with Genres and Ratings)
    * FilmID (Primary Key, INT, Auto-increment)
    * Title (VARCHAR, 255 characters)
    * Release Year (INT, 4 digits)
    * Duration (INT, in minutes)
    * Plot Summary (TEXT)
    * Genre (Foreign Key)
    * Director (Foreign Key)
    * Actors (Foreign Key)
    * Ratings (Foreign Key)
    * Average User Rating (DECIMAL, 2 decimal places, between 1.0 and 10.0)
2. ### Genres Table (One-to-Many with Films and Serials)
    * GenreID (Primary Key, INT, Auto-increment)
    * Genre Name (VARCHAR, 255 characters)
3. ### Actors Table (Many-to-Many with Films and Serials)
    * ActorID (Primary Key, INT, Auto-increment)
    * First Name (VARCHAR, 50 characters)
    * Last Name (VARCHAR, 50 characters)
    * Date of Birth (DATE)
    * Nationality (VARCHAR, 50 characters)
4. ### Directors Table (Many-to-Many with Films and Serials)
    * DirectorID (Primary Key, INT, Auto-increment)
    * First Name (VARCHAR, 50 characters)
    * Last Name  (VARCHAR, 50 characters)
    * Date of Birth (DATE)
    * Nationality (VARCHAR, 50 characters)
5. ### Ratings Table (Many-to-One with Films or Serials)
    * RatingID (Primary Key, INT, Auto-increment)
    * Film or Serial (Foreign Key referencing Films or Serials)
    * User Rating (DECIMAL(3, 1), between 1.0 and 10.0)
    * Review Text (TEXT, optional)
6. ### Awards Table (Many-to-One with Films and Serials)
    * AwardID (Primary Key, INT, Auto-increment)
    * Film or Serial (Foreign Key referencing Films or Serials)
    * Award Name (VARCHAR(255) or ENUM, e.g., 'Best Picture')
    * Award Category (VARCHAR(255) or ENUM, e.g., 'Drama')
    * Year Received  (INT, 4 digits)
7. ### Languages Table (One-to-Many with Films)
    * LanguageID (Primary Key, INT, Auto-increment)
    * Language Name (VARCHAR(50))
    * Film (Foreign Key referencing Films, Unique Constraint)
8. ### Roles Table (One-to-Many relationship with User Accounts)
    * RoleID  (Primary Key, INT, Auto-increment)
    * Role Name (VARCHAR(50))
9. ### User Accounts Table (Many-to-One relationship with Watch History)
    * UserID  (Primary Key, INT, Auto-increment)
    * RoleID (Foreign Key)
    * HistoryID (Foreign Key)
    * Username (VARCHAR, 50 characters)
    * Email (VARCHAR, 255 characters)
    * Password (VARCHAR, hashed and salted, longer than 255 characters)
    * Registration Date (DATE)
10. ### Watch History Table (Many-to-Many with User Accounts)
    * HistoryID (Primary Key, INT, Auto-increment)
    * UserID (Foreign Key INT referencing User Accounts)
    * Film or Serial (Foreign Key INT referencing Films or Serials)
    * Date Watched (DATE)

## 4. **Database scheme**
draw.io diagram
