from flask import Flask, render_template, request, redirect, session
import pandas as pd

app = Flask(__name__)
app.secret_key = '1212'  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'upload' in request.form:
            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)

            df = pd.read_csv(file)

            required_columns = ['id', 'brand', 'model', 'price']
            if not all(column in df.columns for column in required_columns):
                return "File CSV harus memiliki kolom: id, brand, model, price"

            table_html = df.to_html(classes='data', index=False)

            session['table_html'] = table_html
            return render_template('index.html', table_html=table_html)

        elif 'clear' in request.form:
            session.pop('table_html', None)  
            return render_template('index.html', table_html=None)

    table_html = session.get('table_html', None)
    return render_template('index.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
