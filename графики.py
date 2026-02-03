import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine('sqlite:///exam_bot.db')

def plot_student_progress(student_id):
    query = f"SELECT * FROM progress WHERE student_id = {student_id}"
    user_progress = pd.read_sql(query, con=engine)

    if user_progress.empty:
        print(f"There is no data on student {student_id}")
        return

    # Вычисляем процент правильных ответов
    user_progress['percent_correct'] = user_progress['correct_answers'] / user_progress['total_questions'] * 100

    # Сортировка тем
    user_progress['theme_order'] = user_progress['subj'] + "_" + user_progress['theme']
    user_progress = user_progress.sort_values('theme_order')

    sns.set(style="whitegrid")
    plt.figure(figsize=(16,7))

    # График по темам
    plt.subplot(1, 2, 1)
    theme_avg = user_progress.groupby('theme')['percent_correct'].mean().reset_index()
    sns.barplot(data=theme_avg, x='theme', y='percent_correct', palette="viridis", alpha=0.3)

    for subj in user_progress['subj'].unique():
        subj_data = user_progress[user_progress['subj'] == subj]
        subj_theme_avg = subj_data.groupby('theme')['percent_correct'].mean().reset_index()
        subj_theme_avg = subj_theme_avg.set_index('theme').reindex(theme_avg['theme']).reset_index()
        sns.lineplot(
            data=subj_theme_avg,
            x='theme',
            y='percent_correct',
            marker='o',
            label=subj
        )

    plt.ylim(0, 100)
    plt.title("Progress by topics with subjects")
    plt.ylabel("Percentage of correct answers")
    plt.xlabel("Theme")
    plt.xticks(rotation=45)

    # График по тестам
    plt.subplot(1, 2, 2)
    sns.lineplot(
        data=user_progress.sort_values('testid'),
        x='testid',
        y='percent_correct',
        marker='o',
        hue='subj'
    )
    plt.ylim(0, 100)
    plt.title("Test progress")
    plt.xlabel("Test number")
    plt.ylabel("Percentage of correct answers")
    plt.xticks(user_progress['testid'].unique())

    plt.tight_layout()
    plt.savefig()
