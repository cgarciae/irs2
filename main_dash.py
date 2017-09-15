#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 22:54:06 2017

@author: J. C. Vasquez-Correa
"""

import sys
sys.path.append('./')
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import base64
import os
import numpy as np




def get_images_radom(path_images,list_images):
    pos=np.random.permutation(list_images)
    name_file=[]
    images=[]
    for j in range(6):
        image_names=path_images+pos[j]
        images.append(base64.b64encode(open(image_names, 'rb').read()))
        name_file.append(pos[j])
    return images, name_file

def get_image(path_images,file_image):
    return base64.b64encode(open(path_images+file_image, 'rb').read())



images_to_plot=[]
image_filename="./logo-brandon-logan-tm1.png"
image_folder="./data/images2440/imgs/"
list_images=os.listdir(image_folder)

initial_images, name_files=get_images_radom(image_folder, list_images)
img_sel=[]
name_file=[]
app = dash.Dash('Brandon')

selected_image=[]


encoded_image=base64.b64encode(open(image_filename, 'rb').read())

styles = {
    'column': {
        'display': 'inline-block',
        'width': '33%',
        'padding': 10,
        'boxSizing': 'border-box',
        'minHeight': '200px'
    },
    'pre': {'border': 'thin lightgrey solid'}
}



app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width':600, 'height':300}),
    
    
   html.Div([
        dcc.Markdown("""
            **Please select one of the following images**
        """.replace('    ', '')),
        html.Pre(id='selected-data', style=styles['pre']),
    ]),
    
    dcc.RadioItems(
        id='Image-str',
        options=[{'label': i, 'value': i} for i in ['Image '+str(j) for j in range(1,7)]],
        #value='',
        labelStyle={'display': 'inline-block'},
        style={'align': 'middle', 'columnCount': 1}
    ),
    
    
    html.Div([
            html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
             ], style={'columnCount': 3}, id='images1'),    

 
    
    html.Div([
            html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),
            ], style={'columnCount': 3},id='images2'),

    
    html.Button('Submit', id='button'),
    html.Div(id='output-a'),
    html.Div(id='output-b'),
    
    
    
    
], style={'align':'middle'})
    
    

@app.callback(
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('Image-str', 'value')])
def callback_a(dropdown_value):
    print(dropdown_value[-1]+"HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    img_sel.append(int(dropdown_value[-1]))
    return 'You\'ve selected Image "{}"'.format(dropdown_value)

@app.callback(
    dash.dependencies.Output('images1', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def callback_c(n_clicks):
    if n_clicks==3:
        if img_sel[-1]<=3:
            selected_image=name_files[img_sel[-1]-1]
            images_to_plot.append(get_image(image_folder,selected_image))
            print(selected_image) 
            
    

            
        return [
                dcc.Markdown("""
                    **The images selected where**
                """.replace('    ', '')),
                html.Pre(id='selected-data', style=styles['pre']),
                 ]    
    else:
        if img_sel[-1]<=3:
            selected_image=name_files[img_sel[-1]-1]
            images_to_plot.append(get_image(image_folder,selected_image))
            print(selected_image) 
            
            
        initial_images, name_files2=get_images_radom(image_folder,list_images) # comment after run the API
        return [
                html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
                ]


@app.callback(
    dash.dependencies.Output('images2', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def callback_d(n_clicks):
    
    
    if n_clicks==3:
        if img_sel[-1]>3:
            selected_image=name_files[img_sel[-1]-1]
            images_to_plot.append(get_image(image_folder,selected_image))
            print(selected_image)   
            

        return [
                html.Img(src='data:image/png;base64,{}'.format(images_to_plot[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(images_to_plot[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(images_to_plot[2].decode()), style={'width':'300px', 'height':'200px'}),
                 ]    
    else:
        if img_sel[-1]>3:
            selected_image=name_files[img_sel[-1]-1]
            images_to_plot.append(get_image(image_folder,selected_image))
            print(selected_image)  
        initial_images, name_files2=get_images_radom(image_folder,list_images) # comment after run the API
        return [
                html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),
                 ]

if __name__ == '__main__':
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"}) # to change fontstyle
    app.run_server()
