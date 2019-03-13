from flask import Flask, render_template, request, redirect, url_for, jsonify

from model_output import *

from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def main():

    if request.method == 'GET':
        
        plots = []
        plots.append(make_plot([[0 for i in range(10)]]))

        return render_template('paint.html', plots=plots)

    if request.method == "POST":
        
        data_url = request.form['save_image']
     
        img = handle_image(data_url)

        prediction, softmax = predict(img)
        plots = []
        plots.append(make_plot(softmax))

        return jsonify(prediction=str(prediction), plots=plots)

def make_plot(softmax):

    y = [str(i) for i in range(10)]
    x = [i for i in softmax[0]]

    plot = figure(title='Prediction Probabilities',
    y_range=y, plot_height=400, plot_width=400, 
    toolbar_location=None, tools='')
    
    plot.hbar(y=y, right=x, height=0.9, fill_alpha=0.8, fill_color='navy')

    plot.ygrid.grid_line_color = None
    plot.xgrid.grid_line_color = None

    plot.x_range.start = 0
    plot.x_range.end = 1

    script, div = components(plot)

    return script, div


if __name__ == '__main__':

    app.run()