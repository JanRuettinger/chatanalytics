from flask import current_app
import os
import sys
import project.main.data_analytics as data_analytics
from ..models import Analysis
from ..factory import db
import project.main.mail as mail


def analyse_new_chats():
    new_chats = mail.get_new_chats()
    for chat in new_chats:
        filepath = chat[3]  # path to txt chat file
        print("Starte Anaylse...")

        # Folder name  for plots = Filename
        folder = filepath.split(".")
        folder.pop()
        plot_path = "/".join(folder)
        if not os.path.exists(plot_path):
            os.makedirs(plot_path)

        data_raw = data_analytics.open_data(filepath)
        df = data_analytics.preprocess_data(data_raw)
        data_analytics.calculate_total_numbers(df)
        data_analytics.calculate_averages(df)
        data_analytics.make_plots(data_analytics.calculate_activity(df), plot_path)
        print("Analysis finished successfully!")
        print("Speichere Analyse in der Datenbank...")
        os.remove(filepath)
        analysis = Analysis(email=chat[2], name=chat[1], path=plot_path)
        db.session.add(analysis)
        try:
            db.session.commit()
        except:
            print("Error: Couldn't store analysis in database")
            break
        try:
            mail.send_email(analysis.email, "Your Result is ready!", 'email/result', name=analysis.name, link_hash=analysis.link_hash)
        except:
            print("Unexpected error:", sys.exc_info()[0])



