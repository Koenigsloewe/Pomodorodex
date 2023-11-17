import os
import sqlite3


def generate_config_file():
    try:
        with open("config.json", "r") as f:
            pass

    except FileNotFoundError:
        with open("config.json", "w") as f:
            f.write("""{
    "routines": [
        {
            "time": "00:25:00",
            "label": "Pomodoro"
        },
        {
            "time": "00:05:00",
            "label": "Short Break"
        },
        {
            "time": "00:25:00",
            "label": "Pomodoro"
        },
        {
            "time": "00:05:00",
            "label": "Short Break"
        },
        {
            "time": "00:25:00",
            "label": "Pomodoro"
        },
        {
            "time": "00:05:00",
            "label": "Short Break"
        },
        {
            "time": "00:25:00",
            "label": "Pomodoro"
        },
        {
            "time": "00:05:00",
            "label": "Short Break"
        },
        {
            "time": "00:25:00",
            "label": "Pomodoro"
        },
        {
            "time": "00:20:00",
            "label": "Long Break"
        }
    ],
    "tasks": []
}""")


def generate_stylesheet():
    try:
        with open("app/resources/styles.qss", "r") as f:
            pass
    except FileNotFoundError:
        os.makedirs("app/resources", exist_ok=True)

        with open("app/resources/styles.qss", "w") as f:
            print("no file exists")
            f.write("""*{
    color:white;
    font-size:14px;
}

#centralwidget{
    background-color: #121212;
}

QLabel{
    font-size: 28px;
}

#primary_btn{
    border: none;
    border-radius: 20px;
    color: #f0f0f0;
    background-color: #5647ae;
    padding-left: 20px;
    padding-right: 20px;
}

#primary_btn:hover{
	background-color: #483d94;
}

#secondary_btn{
    border: solid ;
    border-color: #5647ae;
    border-width: 3px;
    border-radius: 20px;
    color: #f0f0f0;
    background-color: rgba(0,0,0,0);
}

#secondary_btn:hover{
    background-color: rgba( 86, 71, 174, 0.16)
}

#myTimer{
    background-color: #2a2929;
    border: solid;
    border-radius: 20px;
}

#circle_bg{
    background-color: #3f3f3f;
    border-radius: 149px;
}

#circle_fg{
    background-color: #2a2929;
    border-radius: 137px;
}

#timer_label{
    font-size: 40px;
}

#menubar_widget{
    background-color: #2a2929;
    border: solid;
    border-radius: 20px;
}

#content_widget{
    background-color: #2a2929;
    border: solid;
    border-radius: 20px;
}

#line_edit{
    border: solid ;
    border-color: #5647ae;
    border-width: 3px;
    border-radius: 20px;
    color: #f0f0f0;
    background-color: rgba(0,0,0,0);
    padding-left: 5px;
    padding-right: 5px;
}

#text_line_edit{
    background-color: #2a2929;
    border: none;
}

#task_finished{
    background-color: #2a2929;
    border: none;
    text-decoration: line-through;
    color: #808080;
}

QCheckBox::indicator:unchecked{
    background-image: url(:/svg/uncheck-square.svg)
}

QCheckBox::indicator:checked{
    background-image: url(:/svg/check-square.svg);
}

#scroll_area{
    background-color: #2a2929;
    border: none;
}

#task_widget{
    background-color: #2a2929;
}

QScrollBar:vertical{
    border: none;
    width:6px;
    border-radius: 20px;
}

QScrollBar::handle:vertical{
    background-color: #9e9e9e;
    border-radius:3px;
    margin-top: 0px;
    margin-bottom: 0px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{
    height: 0;
    width: 0;
}

#UwU {
    background-color: white;
}

#w {
    background-color: green;
}

#a {
    background-color: yellow;
}""")

def generate_db():
    try:
        with open("app/components/pomodorodex.db") as f:
            pass
    except FileNotFoundError:
        with sqlite3.connect("app/components/pomodorodex.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE pomodoro_sessions (
                    id INTEGER PRIMARY KEY,
                    date DATE,
                    focus_time INTEGER,
                    break_time INTEGER
                )
            ''')
            conn.commit()

            cursor.execute('''
                CREATE TABLE task_list (
                    id INTEGER PRIMARY KEY,
                    task TEXT,
                    status TEXT CHECK(status IN ('checked', 'unchecked'))
                );

            ''')
            conn.commit()

            conn.close()
