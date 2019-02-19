from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('homepage.html', title="Generate a maze")
    

@app.route('/mazes')
def maze_list():
    return render_template('viewmazes.html', title="View all mazes")

@app.route('/mazes/<int:maze>')
def view_maze(maze):
    print()
    print(os.getcwd())
    print()
    return render_template('viewmaze.html', title=f"Viewing maze {maze}")

if __name__ == "__main__":
    app.run()
