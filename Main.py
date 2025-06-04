import pandas as pd
import tkinter as tk
from tkinter import messagebox
from the_model import get_recommendations  


df_cleaned = pd.read_csv('Processed_Dataset.csv')
df_cleaned['Title'] = df_cleaned['Title'].astype(str)
movie_titles = df_cleaned['Title'].tolist()

# Functions for a interactive window (buttons and getting lists, etc)
def get_user_input():
    user_liked_movies = []
    listbox = None

    def add_movie(event=None):
        movie_title = entry.get()
        if movie_title.strip():
            user_liked_movies.append(movie_title.strip())
            entry.delete(0, tk.END)
            update_listbox()

    def delete_movie():
        selected_index = listbox.curselection()
        if selected_index:
            user_liked_movies.pop(selected_index[0])
            update_listbox()

    def update_listbox():
        listbox.delete(0, tk.END)        
        for movie in user_liked_movies:
            listbox.insert(tk.END, movie)

    def done():
        nonlocal user_liked_movies
        if len(user_liked_movies) == 0:
            messagebox.showwarning("warning", "Please add at least two movies.")
        else:
            recommendations = get_recommendations(user_liked_movies)
            recommendations_window = tk.Toplevel(root)
            recommendations_window.title("Recommended Movies")
            recommendations_window.geometry("600x400")

            scrollbar = tk.Scrollbar(recommendations_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox_recommendations = tk.Listbox(recommendations_window, yscrollcommand=scrollbar.set)
            for movie in recommendations:
                listbox_recommendations.insert(tk.END, movie)
            listbox_recommendations.pack(fill=tk.BOTH, expand=True)

            scrollbar.config(command=listbox_recommendations.yview)

    root = tk.Tk()
    root.title("Movie recommendations")
    root.geometry('500x400')

    label = tk.Label(root, text="Enter the movies you like:")
    label.pack(pady=10)

    entry = tk.Entry(root, width=50)
    entry.pack(pady=10)
    entry.focus_set()

    add_button = tk.Button(root, text="Add Movie", command=add_movie)
    add_button.pack(pady=5)
    entry.bind('<Return>', lambda event: add_movie())

    delete_button = tk.Button(root, text="Delete Movie", command=delete_movie)
    delete_button.pack(pady=5)

    listbox = tk.Listbox(root, width=60, height =10)
    listbox.pack(pady=10)

    done_button = tk.Button(root, text="Done!", command=done)
    done_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    get_user_input()
