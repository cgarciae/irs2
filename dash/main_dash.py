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
from test_color import get_main_colors, generate_colormap




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



styles = {
    'column': {
        'display': 'inline-block',
        'width': '33%',
        'padding': 10,
        'boxSizing': 'border-box',
        'minHeight': '200px'
    },
    'pre': {'border': 'thin lightgrey solid', 'align':'center'}
}


global state
global img_sel
state=0
img_sel=0
image_filename="./logo-brandon-logan-tm1.png"
image_folder="./data/images2440/imgs/"

images_to_plot=[]
list_images=os.listdir(image_folder)

name_files_all=[]

initial_images, name_files=get_images_radom(image_folder, list_images)

name_files_all.append(name_files)


app = dash.Dash('Brandon')

selected_image=[]


encoded_image=base64.b64encode(open(image_filename, 'rb').read())




app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width':300, 'height':100}),
    
    
   html.Div([
        dcc.Markdown("""
            ### Intuitive Brief         
            **Please select one of the following images that you like the most to inspire our designers**
        """.replace('    ', '')),
        html.Pre(id='selected-data', style=styles['pre']),
    ]),
    
    dcc.RadioItems(
        id='Image-str',
        options=[{'label': i, 'value': i} for i in ['Image '+str(j) for j in range(1,7)]],
        value='',
        labelStyle={'display': 'inline-block'},
        style={'align': 'center', 'columnCount': 1}
    ),
    
    
    html.Div([
            html.Div([
            html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),]),
            html.Div([
            html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
            html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),  ])          
             ], id='images1'),    


    
    html.Button('Submit', id='button'),
    html.Div(id='output-a'),
    
    
    
    
], style={'align':'center'})
    
    

@app.callback(
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('Image-str', 'value')])
def callback_a(dropdown_value):
    global img_sel
    print(dropdown_value[-1]+"HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    img_sel=int(dropdown_value[-1])
    return 'You\'ve selected Image "{}"'.format(dropdown_value)



@app.callback(
    dash.dependencies.Output('images1', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def callback_c(n_clicks):
    global state, img_sel, selected_image, name_files_all

    print("----------------------------------------------------------------------------------------------------------------")
    print(state)
    print("--------------------------------------------------------------------------")
    if state==0:
        if img_sel>0:
            state=1
            selected_image=[]
            selected_image.append(name_files_all[0][img_sel-1])
            print(selected_image)
            print(name_files_all)
            initial_images, name_files2=get_images_radom(image_folder,list_images) # comment after run the API
            name_files_all.append(name_files2)
            
            return [
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
                ]),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),  ])          
                ]


        else: 
            state=0
            selected_image=[]
            return [
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
                ]),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),  ])          
                ]
        
    if state==1:

        if img_sel>0:
            state=2
            selected_image.append(name_files_all[1][img_sel-1])
            print(selected_image)
            print(name_files_all)
            initial_images, name_files3=get_images_radom(image_folder,list_images) # comment after run the API
            name_files_all.append(name_files3)
            
            return [
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
                ]),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),  ])          
                ]


        else: 
            state=1
            return [
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
                ]),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),  ])          
                
                ]





    if state==2:

        if img_sel>0:
            state=3
            selected_image.append(name_files_all[2][img_sel-1])
            print(selected_image)
            print(name_files_all)
            initial_images, name_files4=get_images_radom(image_folder,list_images) # comment after run the API
            name_files_all.append(name_files4)
            
            return [
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
                ]),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),  ])          
                ]


        else: 
            state=2
            return [
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[0].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[1].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[2].decode()), style={'width':'300px', 'height':'200px'}),
                ]),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(initial_images[3].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[4].decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(initial_images[5].decode()), style={'width':'300px', 'height':'200px'}),  ])          
                ]



    if state==3:
        state=0
        print(selected_image)
        print(name_files_all)
        image1=base64.b64encode(open(image_folder+selected_image[0], 'rb').read())
        image2=base64.b64encode(open(image_folder+selected_image[1], 'rb').read())
        image3=base64.b64encode(open(image_folder+selected_image[2], 'rb').read())

        
        colors, perc=get_main_colors(image_folder, selected_image)
        generate_colormap(colors)


        imgcolor1=base64.b64encode(open("./dash/imagecolor0.jpg", 'rb').read())        
        imgcolor2=base64.b64encode(open("./dash/imagecolor1.jpg", 'rb').read())        
        imgcolor3=base64.b64encode(open("./dash/imagecolor2.jpg", 'rb').read())        


        print(colors, perc)
        selected_image=[]
        name_files_all=[]
        initial_images, name_files=get_images_radom(image_folder, list_images)
        name_files_all.append(name_files)

        
        return [html.Div([
                dcc.Markdown("""
                    ### Nice job    
                     The selected images to send the designer are:
                """.replace('    ', '')),]),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(image1.decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(image2.decode()), style={'width':'300px', 'height':'200px'}),
                html.Img(src='data:image/png;base64,{}'.format(image3.decode()), style={'width':'300px', 'height':'200px'}),
                ]),
                    
                html.Div([
                dcc.Markdown("""
                    **CHROMATICS: Main Colors selected**
                """.replace('    ', '')),]),                    

                html.Div([
                html.Div(['{}%'.format(int(perc[0]))]),
                html.Img(src='data:image/png;base64,{}'.format(imgcolor1.decode()), style={'width':'50px', 'height':'50px'}),
                html.Div(['{}%'.format(int(perc[1]))]),
                html.Img(src='data:image/png;base64,{}'.format(imgcolor2.decode()), style={'width':'50px', 'height':'50px'}),
                html.Div(['{}%'.format(int(perc[2]))]),
                html.Img(src='data:image/png;base64,{}'.format(imgcolor3.decode()), style={'width':'50px', 'height':'50px'}),
                ], style={'columnCount': 3}),
                
                    
                
                ]    
        

    
    
    


            
        

if __name__ == '__main__':
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"}) # to change fontstyle
    app.run_server()
