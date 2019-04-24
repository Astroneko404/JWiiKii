from  flask import Flask, render_template, request, session, redirect
from test import searchResult
from Search.Search import get_result
from PseudoRFSearch.returnOriginContent import returnOriginContent

import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'zheshiirzuoye'


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    session['query'] = ''
    session['num'] = 1
    session['result_list'] = []
    if request.method == 'GET':

        return render_template('index.html')

    if request.method == 'POST':
        query = request.form.get('query', None)
        session['query'] = query

        return redirect('/search')

@app.route('/search', methods=['GET', 'POST'])
# @app.route('/search_Page<num>', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        output = []
        searchquery = session['query']
        print(searchquery)
        result_list = get_result(searchquery)
        session['result_list'] = result_list
        for i in range(0, 5):
            content = returnOriginContent(result_list[i]).readDocument()
            output.append(content)

        return render_template('results.html', que=output, queries=searchquery, display="inline")

    if request.method == 'POST':
        posttype = request.form.get('posttype')
        if posttype == 'search':
            output = []
            newquery = request.form.get('query', None)
            session['query'] = newquery
            result_list = get_result(newquery)
            session['result_list'] = result_list
            for i in range(0, 5):
                output.append(returnOriginContent(result_list[i]).readDocument())

            return render_template('results.html', que=output, queries=newquery, display="inline")

        if posttype == 'page':
            output = []
            result_list = session['result_list']
            num = request.form.get('btn')

            if num == "next":
                session['num'] = session['num'] + 1

            else:
                session['num'] = int(num)

            lower_bound = (session['num']-1) * 5
            upper_bound = (session['num']-1) * 5 + 5

            for i in range(lower_bound, upper_bound):
                output.append(returnOriginContent(result_list[i]).readDocument())

            if session['num'] == 5:
                display = "none"
            else:
                display = "inline"

            # print(num)
            # print(session['num'])

            return render_template('results.html', que=output, queries=session['query'], display=display)


if __name__ == '__main__':
    app.run(debug=True)
