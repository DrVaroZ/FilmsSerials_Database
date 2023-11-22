import tkinter as tk
from tkinter import messagebox
import psycopg2
from password_remove import PASSWORD, DATABASE_NAME, USER_NAME


class FilmLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Film Library")
        self.connection = self.connect_to_database()

        if self.connection:
            self.create_gui()
        else:
            messagebox.showerror("Error", "Failed to connect to the database.")
            self.root.destroy()

    def connect_to_database(self):
        try:
            # Update these parameters with your PostgreSQL connection details
            connection = psycopg2.connect(
                database=DATABASE_NAME,
                user=USER_NAME,
                password=PASSWORD,
                host="localhost",
                port="5432"
            )
            messagebox.showinfo("Success", "Connected to the PostgreSQL database!")
            return connection
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error connecting to the database:\n{e}")
            return None

    def create_gui(self):
        # Create and place widgets
        self.label = tk.Label(self.root, text="Welcome to the Digital Film Library")
        self.label.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.create_user_button = tk.Button(self.root, text="Create User", command=self.create_user_window)
        self.create_user_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(pady=10)

    def create_user_window(self):
        self.create_user_window = tk.Toplevel(self.root)
        self.create_user_window.title("Create User")

        self.new_username_label = tk.Label(self.create_user_window, text="Username:")
        self.new_username_label.grid(row=0, column=0, pady=10)

        self.new_username_entry = tk.Entry(self.create_user_window)
        self.new_username_entry.grid(row=0, column=1, pady=10)

        self.new_email_label = tk.Label(self.create_user_window, text="Email:")
        self.new_email_label.grid(row=1, column=0, pady=10)

        self.new_email_entry = tk.Entry(self.create_user_window)
        self.new_email_entry.grid(row=1, column=1, pady=10)

        self.new_password_label = tk.Label(self.create_user_window, text="Password:")
        self.new_password_label.grid(row=2, column=0, pady=10)

        self.new_password_entry = tk.Entry(self.create_user_window, show="*")
        self.new_password_entry.grid(row=2, column=1, pady=10)

        self.create_user_button = tk.Button(self.create_user_window, text="Create User", command=self.create_user)
        self.create_user_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_user(self):
        new_username = self.new_username_entry.get()
        new_email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()

        with self.connection.cursor() as cursor:
            cursor.execute("CALL create_user(%s, %s, %s, %s)",
                           (1, new_username, new_email, new_password))
            self.connection.commit()
            messagebox.showinfo("User Created", f"User {new_username} created successfully!")
            self.create_user_window.destroy()

    def login(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")

        self.username_label = tk.Label(self.login_window, text="Username:")
        self.username_label.grid(row=0, column=0, pady=10)

        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.grid(row=0, column=1, pady=10)

        self.password_label = tk.Label(self.login_window, text="Password:")
        self.password_label.grid(row=1, column=0, pady=10)

        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        self.login_button = tk.Button(self.login_window, text="Login", command=self.validate_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with self.connection.cursor() as cursor:
            cursor.execute('SELECT "RoleID_FK" FROM "Users" WHERE "Username" = %s AND "Password" = %s',
                           (username, password))
            role = cursor.fetchone()

            if role:
                messagebox.showinfo("Login Successful", f"Welcome, {username} ({role[0]})!")
                self.show_user_info(username, role[0])
                self.login_window.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

    def show_user_info(self, username, role):
        self.user_info_window = tk.Toplevel(self.root)
        self.user_info_window.title("User Information")

        self.current_username = username

        self.user_info_label = tk.Label(self.user_info_window, text=f"Welcome, {username} ({role})!")
        self.user_info_label.grid(row=0, column=0, pady=10)

        # Add more widgets to display additional information based on the user's role
        if role == 2:  # admin id - 2
            # Add admin-specific information
            self.search_user_label = tk.Label(self.user_info_window, text="Enter user name to get info about:")
            self.search_user_label.grid(row=1, column=0, pady=10)

            self.search_user_entry = tk.Entry(self.user_info_window)
            self.search_user_entry.grid(row=1, column=1, pady=10, padx=10)

            self.search_user_button = tk.Button(self.user_info_window, text="Search", command=self.search_users)
            self.search_user_button.grid(row=1, column=2, pady=10, padx=10)

            self.create_user_label = tk.Label(self.user_info_window, text="Press button to create new user:")
            self.create_user_label.grid(row=2, column=0, pady=10)

            self.create_user_button = tk.Button(self.user_info_window, text="Create user",
                                                command=self.create_users_window_popup)
            self.create_user_button.grid(row=2, column=1, pady=10, padx=10)

            self.update_user_label = tk.Label(self.user_info_window, text="Press button to update existing user:")
            self.update_user_label.grid(row=3, column=0, pady=10)

            self.update_user_button = tk.Button(self.user_info_window, text="Update user",
                                                command=self.update_users_window_popup)
            self.update_user_button.grid(row=3, column=1, pady=10, padx=10)

            self.delete_user_label = tk.Label(self.user_info_window, text="Enter username to delete existing user:")
            self.delete_user_label.grid(row=4, column=0, pady=10)

            self.delete_user_entry = tk.Entry(self.user_info_window)
            self.delete_user_entry.grid(row=4, column=1, pady=10, padx=10)

            self.delete_user_button = tk.Button(self.user_info_window, text="Delete user",
                                                command=self.delete_users)
            self.delete_user_button.grid(row=4, column=2, pady=10, padx=10)

            self.search_film_label = tk.Label(self.user_info_window, text="Enter film title to get info about:")
            self.search_film_label.grid(row=5, column=0, pady=10)

            self.search_film_entry = tk.Entry(self.user_info_window)
            self.search_film_entry.grid(row=5, column=1, pady=10, padx=10)

            self.search_film_button = tk.Button(self.user_info_window, text="Search", command=self.search_films)
            self.search_film_button.grid(row=5, column=2, pady=10, padx=10)

            self.search_film_list_label = tk.Label(self.user_info_window, text="Enter film title to get list of films:")
            self.search_film_list_label.grid(row=6, column=0, pady=10)

            self.search_film_list_entry = tk.Entry(self.user_info_window)
            self.search_film_list_entry.grid(row=6, column=1, pady=10, padx=10)

            self.search_film_list_button = tk.Button(self.user_info_window, text="Search",
                                                     command=self.search_films_by_like)
            self.search_film_list_button.grid(row=6, column=2, pady=10, padx=10)

            self.create_review_label = tk.Label(self.user_info_window, text="Press the button to leave review:")
            self.create_review_label.grid(row=7, column=0, pady=10)

            self.create_review_button = tk.Button(self.user_info_window, text="Create review",
                                                  command=self.create_review_popup)
            self.create_review_button.grid(row=7, column=2, pady=10, padx=10)

            self.user_history_label = tk.Label(self.user_info_window, text="Press the button to get user history:")
            self.user_history_label.grid(row=8, column=0, pady=10)

            self.user_history_button = tk.Button(self.user_info_window, text="Watch history",
                                                 command=self.get_user_history)
            self.user_history_button.grid(row=8, column=2, pady=10, padx=10)

            self.get_reviews_label = tk.Label(self.user_info_window,
                                              text="Press the button to get reviews by film title:")
            self.get_reviews_label.grid(row=9, column=0, pady=10)

            self.get_reviews_entry = tk.Entry(self.user_info_window)
            self.get_reviews_entry.grid(row=9, column=1, pady=10, padx=10)

            self.get_reviews_button = tk.Button(self.user_info_window, text="Get reviews",
                                                command=self.get_reviews_by_film)
            self.get_reviews_button.grid(row=9, column=2, pady=10, padx=10)

            self.get_user_reviews_label = tk.Label(self.user_info_window,
                                                   text="Press the button to get reviews by username:")
            self.get_user_reviews_label.grid(row=10, column=0, pady=10)

            self.get_user_reviews_entry = tk.Entry(self.user_info_window)
            self.get_user_reviews_entry.grid(row=10, column=1, pady=10, padx=10)

            self.get_user_reviews_button = tk.Button(self.user_info_window, text="Get reviews",
                                                     command=self.get_reviews_by_username)
            self.get_user_reviews_button.grid(row=10, column=2, pady=10, padx=10)
        elif role == 1:  # user id - 1
            # Add user-specific information
            self.search_film_label = tk.Label(self.user_info_window, text="Enter film title to get info about:")
            self.search_film_label.grid(row=1, column=0, pady=10)

            self.search_film_entry = tk.Entry(self.user_info_window)
            self.search_film_entry.grid(row=1, column=1, pady=10, padx=10)

            self.search_film_button = tk.Button(self.user_info_window, text="Search", command=self.search_films)
            self.search_film_button.grid(row=1, column=2, pady=10, padx=10)

            self.search_film_list_label = tk.Label(self.user_info_window, text="Enter film title to get list of films:")
            self.search_film_list_label.grid(row=2, column=0, pady=10)

            self.search_film_list_entry = tk.Entry(self.user_info_window)
            self.search_film_list_entry.grid(row=2, column=1, pady=10, padx=10)

            self.search_film_list_button = tk.Button(self.user_info_window, text="Search",
                                                     command=self.search_films_by_like)
            self.search_film_list_button.grid(row=2, column=2, pady=10, padx=10)

            self.create_review_label = tk.Label(self.user_info_window, text="Press the button to leave review:")
            self.create_review_label.grid(row=3, column=0, pady=10)

            self.create_review_button = tk.Button(self.user_info_window, text="Create review",
                                                  command=self.create_review_popup)
            self.create_review_button.grid(row=3, column=2, pady=10, padx=10)

            self.user_history_label = tk.Label(self.user_info_window, text="Press the button to get user history:")
            self.user_history_label.grid(row=4, column=0, pady=10)

            self.user_history_button = tk.Button(self.user_info_window, text="Watch history",
                                                 command=self.get_user_history)
            self.user_history_button.grid(row=4, column=2, pady=10, padx=10)

            self.get_reviews_label = tk.Label(self.user_info_window,
                                              text="Press the button to get reviews by film title:")
            self.get_reviews_label.grid(row=5, column=0, pady=10)

            self.get_reviews_entry = tk.Entry(self.user_info_window)
            self.get_reviews_entry.grid(row=5, column=1, pady=10, padx=10)

            self.get_reviews_button = tk.Button(self.user_info_window, text="Get reviews",
                                                command=self.get_reviews_by_film)
            self.get_reviews_button.grid(row=5, column=2, pady=10, padx=10)

            self.get_user_reviews_label = tk.Label(self.user_info_window,
                                                   text="Press the button to get reviews by username:")
            self.get_user_reviews_label.grid(row=6, column=0, pady=10)

            self.get_user_reviews_entry = tk.Entry(self.user_info_window)
            self.get_user_reviews_entry.grid(row=6, column=1, pady=10, padx=10)

            self.get_user_reviews_button = tk.Button(self.user_info_window, text="Get reviews",
                                                     command=self.get_reviews_by_username)
            self.get_user_reviews_button.grid(row=6, column=2, pady=10, padx=10)

    def search_films(self):
        film_title = self.search_film_entry.get()

        search_results_window = tk.Toplevel(self.root)
        search_results_window.title("Search Results")

        result_text = tk.Text(search_results_window, wrap=tk.WORD, width=80, height=20)
        result_text.pack(pady=10, padx=10)

        seen_titles = set()  # Keep track of film titles to avoid duplicates

        with self.connection.cursor() as cursor:
            cursor.execute('select * from find_film_by_title_with_details(%s)', (film_title,))
            film_info = cursor.fetchall()

            if film_info:
                for film in film_info:
                    title = film[1]
                    if title not in seen_titles:
                        seen_titles.add(title)

                        # Format the film information for better readability
                        formatted_info = f"Title: {film[1]}\nRelease Year: {film[2]}\nDuration: {film[3]}\n" \
                                         f"Plot Summary: {film[4]}\nAverage Rating: {film[5]}\nLanguage: {film[6]}\n" \
                                         f"Award: {film[7]}\nDirector: {film[8]}\n"

                        # Use sets to store unique actors and genres
                        unique_actors = set(actor[9] for actor in film_info if actor[1] == title)
                        unique_genres = set(genre[10] for genre in film_info if genre[1] == title)

                        # Add all actors for the film
                        formatted_info += "Actors: " + ", ".join(unique_actors) + "\n"

                        # Add all genres for the film
                        formatted_info += "Genres: " + ", ".join(unique_genres) + "\n\n"

                        result_text.insert(tk.END, formatted_info)
            else:
                # Display a message if no results found
                result_text.insert(tk.END, "No films found with the given title.")

    def search_films_by_like(self):
        film_title_partial = self.search_film_list_entry.get()

        search_results_window = tk.Toplevel(self.root)
        search_results_window.title("Search Results")

        result_text = tk.Text(search_results_window, wrap=tk.WORD, width=80, height=20)
        result_text.pack(pady=10, padx=10)

        with self.connection.cursor() as cursor:
            cursor.execute("select * from get_films_by_title_partial(%s)", (film_title_partial,))
            film_titles = cursor.fetchall()

            if film_titles:
                result_text.insert(tk.END, "Matching Film Titles:\n\n")
                for title in film_titles:
                    result_text.insert(tk.END, f"{title[0]}\n")
            else:
                result_text.insert(tk.END, "No films found with the given search term.")

    def search_users(self):
        username = self.search_user_entry.get()

        search_results_window = tk.Toplevel(self.root)
        search_results_window.title("User Search Results")

        result_text = tk.Text(search_results_window, wrap=tk.WORD, width=80, height=20)
        result_text.pack(pady=10, padx=10)

        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM find_user_by_name(%s)', (username,))
            user_info = cursor.fetchall()

            if user_info:
                for user in user_info:
                    result_text.insert(tk.END, f"User ID: {user[0]}\n")
                    result_text.insert(tk.END, f"Role: {user[1]}\n")
                    result_text.insert(tk.END, f"Username: {user[2]}\n")
                    result_text.insert(tk.END, f"Email: {user[3]}\n")
                    result_text.insert(tk.END, f"Password: {user[4]}\n")
                    result_text.insert(tk.END, f"Registration Date: {user[5]}\n")
                    result_text.insert(tk.END, "-" * 40 + "\n")
            else:
                result_text.insert(tk.END, "No users found with the given username.")

    def create_users_window_popup(self):
        self.create_user_window = tk.Toplevel(self.root)
        self.create_user_window.title("Create User")

        self.new_username_label = tk.Label(self.create_user_window, text="Username:")
        self.new_username_label.grid(row=0, column=0, pady=10)

        self.new_username_entry = tk.Entry(self.create_user_window)
        self.new_username_entry.grid(row=0, column=1, pady=10)

        self.new_email_label = tk.Label(self.create_user_window, text="Email:")
        self.new_email_label.grid(row=1, column=0, pady=10)

        self.new_email_entry = tk.Entry(self.create_user_window)
        self.new_email_entry.grid(row=1, column=1, pady=10)

        self.new_password_label = tk.Label(self.create_user_window, text="Password:")
        self.new_password_label.grid(row=2, column=0, pady=10)

        self.new_password_entry = tk.Entry(self.create_user_window, show="*")
        self.new_password_entry.grid(row=2, column=1, pady=10)

        self.new_role_label = tk.Label(self.create_user_window, text="Role:")
        self.new_role_label.grid(row=3, column=0, pady=10)

        self.new_role_entry = tk.Entry(self.create_user_window)
        self.new_role_entry.grid(row=3, column=1, pady=10)

        self.create_user_button = tk.Button(self.create_user_window, text="Create User",
                                            command=self.create_user_by_admin)
        self.create_user_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_user_by_admin(self):
        new_username = self.new_username_entry.get()
        new_email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()
        new_role = self.new_role_entry.get()

        with self.connection.cursor() as cursor:
            cursor.execute("CALL create_user(%s, %s, %s, %s)",
                           (new_role, new_username, new_email, new_password))
            self.connection.commit()
            messagebox.showinfo("User Created", f"User {new_username} was created successfully!")
            self.create_user_window.destroy()

    def update_users_window_popup(self):
        self.update_user_window = tk.Toplevel(self.root)
        self.update_user_window.title("Update User")

        self.new_id_label = tk.Label(self.update_user_window, text="ID:")
        self.new_id_label.grid(row=0, column=0, pady=10)

        self.new_id_entry = tk.Entry(self.update_user_window)
        self.new_id_entry.grid(row=0, column=1, pady=10)

        self.new_username_label = tk.Label(self.update_user_window, text="Username:")
        self.new_username_label.grid(row=1, column=0, pady=10)

        self.new_username_entry = tk.Entry(self.update_user_window)
        self.new_username_entry.grid(row=1, column=1, pady=10)

        self.new_email_label = tk.Label(self.update_user_window, text="Email:")
        self.new_email_label.grid(row=2, column=0, pady=10)

        self.new_email_entry = tk.Entry(self.update_user_window)
        self.new_email_entry.grid(row=2, column=1, pady=10)

        self.new_password_label = tk.Label(self.update_user_window, text="Password:")
        self.new_password_label.grid(row=3, column=0, pady=10)

        self.new_password_entry = tk.Entry(self.update_user_window, show="*")
        self.new_password_entry.grid(row=3, column=1, pady=10)

        self.update_user_button = tk.Button(self.update_user_window, text="Update User",
                                            command=self.update_user_by_admin)
        self.update_user_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_user_by_admin(self):
        new_username = self.new_username_entry.get()
        new_email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()
        new_id = self.new_id_entry.get()

        with self.connection.cursor() as cursor:
            cursor.execute("CALL update_user(%s, %s, %s, %s)",
                           (new_id, new_username, new_email, new_password))
            self.connection.commit()
            messagebox.showinfo("User Updated", f"User {new_username} was updated successfully!")
            self.update_user_window.destroy()

    def delete_users(self):
        username = self.delete_user_entry.get()

        with self.connection.cursor() as cursor:
            cursor.execute('CALL delete_user(%s)', (username,))
            self.connection.commit()
            messagebox.showinfo("User Deleted", f"User {username} was deleted successfully!")

    def create_review_popup(self):
        self.create_review_window = tk.Toplevel(self.root)
        self.create_review_window.title("Create review")

        self.film_title_label = tk.Label(self.create_review_window, text="Film Title:")
        self.film_title_label.grid(row=0, column=0, pady=10)

        self.film_title_entry = tk.Entry(self.create_review_window)
        self.film_title_entry.grid(row=0, column=1, pady=10)

        self.rating_label = tk.Label(self.create_review_window, text="Rating:")
        self.rating_label.grid(row=1, column=0, pady=10)

        self.rating_entry = tk.Entry(self.create_review_window)
        self.rating_entry.grid(row=1, column=1, pady=10)

        self.review_text_label = tk.Label(self.create_review_window, text="Review Text:")
        self.review_text_label.grid(row=2, column=0, pady=10)

        self.review_text_entry = tk.Entry(self.create_review_window)
        self.review_text_entry.grid(row=2, column=1, pady=10)

        self.create_review_button = tk.Button(self.create_review_window, text="Create Review",
                                              command=self.create_review_by_user)
        self.create_review_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_review_by_user(self):
        username = self.current_username
        film_title = self.film_title_entry.get()
        rating = self.rating_entry.get()
        review_text = self.review_text_entry.get()

        with self.connection.cursor() as cursor:
            cursor.execute("CALL create_review(%s, %s, %s, %s)",
                           (username, film_title, rating, review_text))
            self.connection.commit()
            messagebox.showinfo("Review is created", f"Review was created successfully!")
            self.create_review_window.destroy()

    def get_user_history(self):
        username = self.current_username

        history_results_window = tk.Toplevel(self.root)
        history_results_window.title("User History Results")

        result_text = tk.Text(history_results_window, wrap=tk.WORD, width=80, height=20)
        result_text.pack(pady=10, padx=10)

        with self.connection.cursor() as cursor:
            cursor.execute("select * from get_history_by_username(%s)", (username, ))
            history_info = cursor.fetchall()

            if history_info:
                for history in history_info:
                    result_text.insert(tk.END, f"Date Watched: {history[0]}\n")
                    result_text.insert(tk.END, f"Film Title: {history[1]}\n")
                    result_text.insert(tk.END, "-" * 40 + "\n")
            else:
                result_text.insert(tk.END, "History is empty")

    def get_reviews_by_film(self):
        film_title = self.get_reviews_entry.get()

        film_reviews_window = tk.Toplevel(self.root)
        film_reviews_window.title("Film Reviews Results")

        result_text = tk.Text(film_reviews_window, wrap=tk.WORD, width=80, height=20)
        result_text.pack(pady=10, padx=10)

        with self.connection.cursor() as cursor:
            cursor.execute("select * from get_reviews_by_film(%s)", (film_title, ))
            reviews_info = cursor.fetchall()

            if reviews_info:
                for review in reviews_info:
                    result_text.insert(tk.END, f"Username: {review[0]}\n")
                    result_text.insert(tk.END, f"Rating: {review[1]}\n")
                    result_text.insert(tk.END, f"Review Text: {review[2]}\n")
                    result_text.insert(tk.END, "-" * 40 + "\n")
            else:
                result_text.insert(tk.END, "There are no reviews")

    def get_reviews_by_username(self):
        username = self.get_user_reviews_entry.get()

        film_user_reviews_window = tk.Toplevel(self.root)
        film_user_reviews_window.title("Film User Reviews Results")

        result_text = tk.Text(film_user_reviews_window, wrap=tk.WORD, width=80, height=20)
        result_text.pack(pady=10, padx=10)

        with self.connection.cursor() as cursor:
            cursor.execute("select * from get_reviews_by_user(%s)", (username, ))
            reviews_info = cursor.fetchall()

            if reviews_info:
                for review in reviews_info:
                    result_text.insert(tk.END, f"Film Title: {review[0]}\n")
                    result_text.insert(tk.END, f"Rating: {review[1]}\n")
                    result_text.insert(tk.END, f"Review Text: {review[2]}\n")
                    result_text.insert(tk.END, "-" * 40 + "\n")
            else:
                result_text.insert(tk.END, "There are no reviews")


if __name__ == "__main__":
    root = tk.Tk()
    app = FilmLibraryApp(root)
    root.mainloop()
