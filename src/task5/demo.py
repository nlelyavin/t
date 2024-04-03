from flask import Flask, request, render_template
from sklearn.metrics.pairwise import cosine_similarity

from task5.main_5 import main

app = Flask(__name__)

df, tf_idf, vectorizer = main()


@app.route("/")
def index():
    print(request.args)
    query = request.args.get('query', '')
    result = []

    if query:
        query_vec = vectorizer.transform([query])
        results = cosine_similarity(tf_idf, query_vec).reshape((-1,))
        for i in results.argsort()[-10:][::-1]:
            result.append(df.iloc[i, 0])

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run('127.0.0.1', 8000)
