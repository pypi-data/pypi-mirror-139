# TODO
#  
#  


#SECTION
import geopandas as gpd
import plotly.express as px
def mapper(
    data: gpd.GeoDataFrame,
    variable: str, 
    path_maps: str,
    aglo='amba', 
    remove_zeros=True,
    label=None, 
    colorscale_type = 'discrete', 
    colorscale=None,
    subfolder=None,
    variable_corte=None, 
    percentil=0,  
    nombre=None, 
    out='image',
    footnote=None,
    # footnote_x=0.05,
    # footnote_y=0,
    # title=None
) -> None:
    """Generador de mapas

    Args:
        @data (GeoDataFrame): base entera con los datos a graficar
        @variable (str): nombre de la variable que se quiere graficar
        @path_maps (str): Ruta de la carpeta en la que se exporta. Si se corrio la plantilla, debería llamarse path_maps
        @aglo (str, optional): Aglomerado en el que enfocar. Defaults to 'amba'.
        @remove_zeros (bool, optional): Remueve las filas con 0 (o '.') en la variable a graficar
            Si no se remueven los ceros, tarda mucho en graficar los poligonos. 
        @label (str, optional): Etiqueta que se muestra al pasar el mouse por el área pintada (solo en HTML). Defaults to None.
        @colorscale_type (str, optional): Tipo de escala de color a utilizar. Puede ser 'discrete', 'continuous' o 'map':
            'discrete' asigna un color a cada tipo, 'continuous' hace un rango. En 'map' uno define que valor equivale a que color.
            Para que sea continua, la variable tiene que ser numérica. Para ser discreta o map, la variable tiene que ser string
        @colorscale (list o dict, optional): Escala de colores a utilizar. El valor por defecto varía segun el tipo de escala. El formato depende del tipo de escala:
            discrete: list (i.e: ['#edbe2e', '#da6b1f'] )
            continuous: list. Puede tener solo los colores, o puede ser una lista de (numero, color) para definir que proporcion equivale a que color (i.e: [(0, '#5A53A4'),(0.22, '#64C0A6'),(0.44, '#E7F599'),(0.7, '#FEDE89'),(0.93, '#FB9E5A'),(1, '#A70B44')])
            map: dict. La key es la categoría y el value es el color que le correspondie (i.e: {"1": "#da6b1f", "2": "#edbe2e"})
        @subfolder (str o var, optional): Subruta de la carpeta (se puede usar el mismo valor que percentil u otro str creado). Defaults to None.
        @variable_corte (str, optional): Nombre de la variable para hacer el corte por percentil. Defaults to None.
        @percentil (int, optional): Percentil de la variable de corte. Defaults to 0.
        @nombre (str, optional): Nombre a agregar al archivo. Defaults to None.
        @out (str, optional): Tipo de mapa de salida. Puede ser 'html' o 'image'. Defaults to 'image'.
        @footnote (str, optional): Anotacion. Defaults to None.
        
    
    Raises:
        ValueError: [description]
    """  
    # @footnote_x (float, optional): Posición horizontal de la anotación (va de 0 a 1). Defaults to 0.05. 0.01 es pegado a la izquierda (0 se corta el cuadro)
    # @footnote_y (float, optional): Posición vertical de la anotación (va de 0 a 1). Defaults to 0.
    # @title (str, optinal): Título visible en el mapa. Defaults to None.
        
    
    
    import geopandas as gpd
    import pandas as pd
    import numpy as np
    import plotly.express as px

    
    #ZOOMS
    zoom_center =  {'argentina': (3.18,-39.249,-61.960),
                    'amba':      (9.34,-34.637,-58.434),
                    'cordoba':   (10.46,-31.406,-64.194),
                    'rosario':   (10.44,-32.955,-60.678),
                    'mendoza':   (11.36,-32.900,-68.829),
                    'tucuman':   (10.89,-26.819,-65.197),
                    'la_plata':  (10.49,-34.924,-57.941),
                    'mar_del_plata': (10.53,-38.006,-57.523),
                    'salta':     (12.58,-24.794,-65.403),
                    'san_juan':  (10.74,-31.548,-68.491),
                    'santa_fe':  (11.72,-31.625,-60.699)
                   }
    
    pd.options.mode.chained_assignment = None  # default='warn'
    px.set_mapbox_access_token('pk.eyJ1IjoicXVlZW5vMTEiLCJhIjoiY2tlYm81djQ1MGFuNjJzcnM1anYxczE4ZiJ9.mmgMzjhvDMlfcQFrlqWqLg')
    base = data

    #Remove Zeros
    if remove_zeros:
        if base[variable].dtype == 'object':
            base = base[base[variable] != '.']
            base = base[base[variable] != '0']
            base = base[base[variable] != 0 ]
        else:
            base[variable] = base[variable].astype(int).astype(str)[base[variable] != '0']
            base = base[base[variable] != '.']
            base = base[base[variable] != '0']
            base = base[base[variable] != 0 ]
            
    #Corte y percentil
    if not variable_corte:
        variable_corte=variable
    if not label:
        label=variable

    if percentil:
        base = data[data[variable_corte]>=percentil]
    base['uno']=1
        

    #Colorscales

    if not colorscale:
        if colorscale_type == 'discrete':
            colorscale = ['#edbe2e', '#da6b1f']
            #Escala colores ministerio:
            # colorscale=["#ffffff", "#00b0f0"]     
        elif colorscale_type == 'continuous':
            colorscale = [(0, '#5A53A4'),(0.22, '#64C0A6'),(0.44, '#E7F599'),(0.7, '#FEDE89'),(0.93, '#FB9E5A'),(1, '#A70B44')]
        elif colorscale_type == 'map':
            colorscale = {"1": "#da6b1f", "2": "#edbe2e"}
        else:
            raise ValueError('El tipo de escala de colores tiene que ser "discrete", "map" o "continuous')

    # try:
    #     base[variable] = base[variable].astype(int).astype(str)
    # except:
    #     pass

    if colorscale_type == 'discrete':
        fig = px.choropleth_mapbox(
            base,
            geojson=base.geometry,
            locations=base.index,
            color=base[variable],
            labels= {variable:label},
            zoom = zoom_center[aglo][0],
            center = {"lat": zoom_center[aglo][1], 
                      "lon": zoom_center[aglo][2]},
            color_discrete_sequence=colorscale,
            opacity=0.7,
            width= 1200,
            height= 800
        )

    elif colorscale_type == 'continuous':
        fig = px.choropleth_mapbox(
            base,
            geojson=base.geometry,
            locations=base.index,
            color=base[variable],
            labels= {variable:label},
            zoom = zoom_center[aglo][0],
            center = {"lat": zoom_center[aglo][1], 
                      "lon": zoom_center[aglo][2]},
            color_continuous_scale=colorscale,
            opacity=0.7,
            width= 1200,
            height= 800
        )

    elif colorscale_type == 'map':
        fig = px.choropleth_mapbox(
            base,
            geojson=base.geometry,
            locations=base.index,
            color=base[variable],
            labels= {variable:label},
            zoom = zoom_center[aglo][0],
            center = {"lat": zoom_center[aglo][1], 
                      "lon": zoom_center[aglo][2]},
            color_discrete_map=colorscale,
            opacity=0.7,
            width= 1200,
            height= 800
        )

    else:
        raise ValueError('El tipo de escala de colores tiene que ser "discrete", "map" o "continuous')


    fig.update_traces(marker_line_width=0)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        

    fig.update_layout(
        mapbox_style="mapbox://styles/queeno11/ckx8e3hhh1bgd14mtfqnvr9lc",
    )
    
    # Margin footnote
    if footnote:
        fig.add_annotation(
            text = str(footnote),
            x = 1,
            y = -0.07,
            xref = 'paper',
            yref = 'paper',
            xanchor = 'right',
            yanchor= 'bottom',
            font=dict(size=12, color='black'),
            align='left'
        )
        
        fig.update_layout(
            margin={'b':32}
        )
        
    #### Box footnote
    #  fig.add_annotation(
    #         text = str(footnote),
    #         x = footnote_x,
    #         y = footnote_y,
    #         xref = 'paper',
    #         yref = 'paper',
    #         xanchor = 'left',
    #         yanchor= 'bottom',
    #         font=dict(size=12, color='black'),
    #         align='left',
    #         bordercolor='gray',
    #         borderwidth=2,
    #         bgcolor= '#d5d5d5',
    #         opacity = 0.6
    #     )   

    #### Title footnote
    # if title:
    #     fig.update_layout(
    #         title_text=str(title),
    #         margin={"r":0,"l":0,"b":32, 't':32, 'autoexpand':True},
    #         title_font_size=12,
    #         title_x=0.98,
    #         title_xref='paper',
    #         title_xanchor='right'
    #     )
    
    
    
    config={'displaylogo': False,
            'toImageButtonOptions': {
                'filename': variable,
                'height': 500,
                'width': 700,
                'scale': 10 # Multiply title/legend/axis/canvas sizes by this factor
            }
    }

    if subfolder:
        path_maps += f'\\{subfolder}'
    
    #NAME
    if nombre:
        out_name = f'{path_maps}\\{str(nombre)}'
    else:
        out_name =  f'{path_maps}\\mapa_{aglo}_{str(variable_corte)}'
        
        if percentil:
            out_name += f'_percentil_{str(percentil)}'
            



    if out=='html':
        fig.write_html(out_name + '.html', config=config)
    elif out=='image':
        fig.write_image(out_name + ".png", engine='kaleido')

    pd.options.mode.chained_assignment = 'warn'  # default='warn'

    print(f'Mapa creado en {out_name}')
    # return fig