# python3 -m venv --system-site-packages venv
# pip install tikz-python 
# requires latexmk
# Note that tikzpy also calls itself tikzpy


import tikzpy


def make_diagram():
    dia = tikzpy.TikzPicture( center=True )
    return {
        "diagram": dia,
        "style": "draw,very thick,label,outer sep=2pt",
        "rect_c": dia.rectangle_from_center,
        "rect_n": dia.rectangle_from_north,
        "rect_s": dia.rectangle_from_south,
        "rect_e": dia.rectangle_from_east,
        "rect_w": dia.rectangle_from_west,
        "rect": dia.rectangle
    }


def make_system_block( dia, shape, position, width=None, height=None, label=None ):
    constr = dia[shape]
    options = dia["style"] + ",fill=green!25,draw=green!60!black"
    if (width is not None) and (height is not None):
        my_width = width
        my_height = height
    else:
        my_width = 3
        my_height = 1.5
    retv = constr( position, width=my_width, height=my_height, options=options )
    if label is not None:
        dia["diagram"].node( retv.center, options="align=center,text=black!50!green", text=label )
    return retv


def make_web_block( dia, shape, position, width=None, height=None, label=None ):
    constr = dia[shape]
    options = dia["style"] + ",fill=gray!10,draw=black!50!gray"
    if (width is not None) and (height is not None):
        my_width = width
        my_height = height
    else:
        my_width = 3
        my_height = 2
    retv = constr( position, width=my_width, height=my_height, options=options )
    if label is not None:
        dia["diagram"].node( retv.center, options="align=center,text=black!50!gray", text=label )
    return retv


def make_data_block( dia, shape, position, width=None, height=None, label=None ):
    constr = dia[shape]
    options = dia["style"] + ",fill=orange!20,draw=orange!80,rounded corners=0.4cm"
    if (width is not None) and (height is not None):
        my_width = width
        my_height = height
    else:
        my_width = 3
        my_height = 1.5
    retv = constr( position, width=my_width, height=my_height, options=options )
    if label is not None:
        dia["diagram"].node( retv.center, options="align=center,text=black!50!orange", text=label )
    return retv


def make_kobe_block( dia, shape, position, width=None, height=None, label=None ):
    if (width is not None) and (height is not None):
        my_width = width
        my_height = height
    else:
        my_width = 3
        my_height = 2
    constr = dia[shape]
    options = dia["style"] + ",fill=blue!20,draw=blue!60"
    retv = constr( position, width=my_width, height=my_height, options=options )
    if label is not None:
        dia["diagram"].node( retv.center, options="align=center,text=black!50!blue", text=label )
    return retv


def make_kobe_wrapper( dia, shape, position, width=3.5, height=2.5, label="" ):

    retv = make_kobe_block( dia, shape, position, width, height )
    dia["diagram"].node( retv.north - (0,0.5), options="align=center,text=black!50!blue", text="KOBE Wrapper" )
    make_system_block( dia, "rect_s", retv.south + (0,0.2), label=label )
    return retv


def make_bg_wrapper( dia, objects, label=None, label_pos="NW", margins=(0.2,0.2) ):
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    for q in objects:
        if (x_max is None) or (q.right_corner.x > x_max): x_max = q.right_corner.x
        if (y_max is None) or (q.right_corner.y > y_max): y_max = q.right_corner.y
        if (x_min is None) or (q.left_corner.x < x_min): x_min = q.left_corner.x
        if (y_min is None) or (q.left_corner.y < y_min): y_min = q.left_corner.y
    (dx,dy) = margins
    x_min -= dx
    x_max += dx
    y_min -= dy
    y_max += dy
    dia["diagram"].add_command( "\\begin{pgfonlayer}{background}" )
    retv = dia["rect"]( (x_min,y_min), x_max-x_min, y_max-y_min, options="fill=gray!10" )
    if label is not None:
        if label_pos == "NW":
            dia["diagram"].node( (x_min,y_max), options="align=left,anchor=north west,text=black!50!gray", text=label )
        elif label_pos == "NE":
            dia["diagram"].node( (x_max,y_max), options="align=right,anchor=north east,text=black!50!gray", text=label )
        elif label_pos == "SE":
            dia["diagram"].node( (x_max,y_min), options="align=right,anchor=south east,text=black!50!gray", text=label )
        elif label_pos == "SW":
            dia["diagram"].node( (x_min,y_min), options="align=left,anchor=south west,text=black!50!gray", text=label )
        elif label_pos == "W":
            dia["diagram"].node( (x_min,(y_max+y_min)/2), options="align=left,anchor=west,text=black!50!gray", text=label )
        else:
            assert 1 == 0
    dia["diagram"].add_command( "\\end{pgfonlayer}" )
    return retv


def make_componentsA( dia ):
    global sys0, sys1, sys2, orch, reporter, env, spec, data1, data2

    sys0 = make_kobe_wrapper( dia, "rect_c", (0,0), label="System 0" )
    sys1 = make_kobe_wrapper( dia, "rect_n", sys0.south - (0,0.3), label="System 1" )
    sys2 = make_kobe_wrapper( dia, "rect_n", sys1.south - (0,0.3), label="System 2" )

    top = sys0.north.y
    bottom = sys2.south.y
    delta_y = (top-bottom)/6
    delta_x = 1.5

    coords = (sys1.west.x-delta_x,sys1.west.y+delta_y)
    orch = make_kobe_block( dia, "rect_e", coords, label="KOBE \\\\ Orchestrator" )
    coords = (sys1.west.x-delta_x,sys1.west.y-delta_y)
    reporter = make_kobe_block( dia, "rect_e", coords, label="KOBE \\\\ Reporter" )

    env = make_bg_wrapper( dia, [sys0,sys1,sys2,orch,reporter], "KOBE Environment" )

    coords = (env.west.x-delta_x,orch.west.y)
    spec = make_data_block( dia, "rect_e", coords, label="Experiment \\\\ Specification" )
    coords = (env.east.x+delta_x,sys1.west.y+delta_y)
    data1 = make_data_block( dia, "rect_w", coords, label="Training \\\\ Dataset" )
    coords = (env.east.x+delta_x,sys1.west.y-delta_y)
    data2 = make_data_block( dia, "rect_w", coords, label="Testing \\\\ Workload" )


def make_diagramsA():

    dia = make_diagram()
    make_componentsA( dia )
    dia["diagram"].compile( "diagram_A1.pdf" )

    arrow_kobe = "blue!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"
    arrow_file = "orange!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"

    dia = make_diagram()
    make_componentsA( dia )
    dia["diagram"].line( spec.east, orch.west, options = arrow_file )
    dia["diagram"].line( orch.east, sys0.west, options = arrow_kobe )
    dia["diagram"].line( orch.east, sys1.west, options = arrow_kobe )
    dia["diagram"].line( orch.east, sys2.west, options = arrow_kobe )
    dia["diagram"].line( data1.west, sys0.east, options = arrow_file )
    dia["diagram"].line( data1.west, sys1.east, options = arrow_file )
    dia["diagram"].line( data1.west, sys2.east, options = arrow_file )
    dia["diagram"].compile( "diagram_A2.pdf" )

    dia = make_diagram()
    make_componentsA( dia )
    dia["diagram"].line( orch.east, sys0.west, options = arrow_kobe )
    dia["diagram"].line( orch.east, sys1.west, options = arrow_kobe )
    dia["diagram"].line( orch.east, sys2.west, options = arrow_kobe )
    dia["diagram"].line( data2.west, sys0.east, options = arrow_file )
    dia["diagram"].line( data2.west, sys1.east, options = arrow_file )
    dia["diagram"].line( data2.west, sys2.east, options = arrow_file )
    dia["diagram"].compile( "diagram_A3.pdf" )

    dia = make_diagram()
    make_componentsA( dia )
    dia["diagram"].line( sys0.west, reporter.east, options = arrow_file )
    dia["diagram"].line( sys1.west, reporter.east, options = arrow_file )
    dia["diagram"].line( sys2.west, reporter.east, options = arrow_file )
    coords = (env.west.x-1.5,reporter.west.y)
    report = make_data_block( dia, "rect_e", coords, label="Experiment \\\\ Report" )
    dia["diagram"].line( reporter.west, report.east, options = arrow_file )
    dia["diagram"].compile( "diagram_A4.pdf" )

    # write full file
    #dia["diagram"].write_tex_file( "diagrams1.tex" )
    # write tex fragment
    #dia["diagram"].write( "dia1.tex" )



def make_componentsB( dia ):
    global sys, orch, reporter, env, spec, chkpt, data1, data2

    chkpt = make_data_block( dia, "rect_c", (0,0), label="Checkpoint" )
    data1 = make_data_block( dia, "rect_n", chkpt.south - (0,0.3), label="Testing \\\\ Workload 1" )
    data2 = make_data_block( dia, "rect_n", data1.south - (0,0.3), label="Testing \\\\ Workload 1" )

    delta_x = 1.5

    sys = make_kobe_wrapper( dia, "rect_e", data1.west - (delta_x,0), label="System" )

    top = chkpt.north.y
    bottom = data2.south.y

    coords = (sys.west.x-3,top)
    orch = make_kobe_block( dia, "rect_n", coords, label="KOBE \\\\ Orchestrator" )
    coords = (sys.west.x-3,bottom)
    reporter = make_kobe_block( dia, "rect_s", coords, label="KOBE \\\\ Reporter" )

    env = make_bg_wrapper( dia, [sys,orch,reporter], "KOBE Environment", "NE" )

    coords = (env.west.x-delta_x,orch.west.y)
    spec = make_data_block( dia, "rect_e", coords, label="Experiment \\\\ Specification" )


def make_diagramsB():

    dia = make_diagram()
    make_componentsB( dia )

    arrow_kobe = "blue!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"
    arrow_file = "orange!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"

    dia = make_diagram()
    make_componentsB( dia )
    dia["diagram"].line( spec.east, orch.west, options = arrow_file )
    dia["diagram"].line( orch.east, sys.west, options = arrow_kobe )
    dia["diagram"].line( chkpt.west, sys.east, options = arrow_file )
    dia["diagram"].compile( "diagram_B1.pdf" )

    dia = make_diagram()
    make_componentsB( dia )
    dia["diagram"].line( orch.east, sys.west, options = arrow_kobe )
    dia["diagram"].line( data1.west, sys.east, options = arrow_file )
    dia["diagram"].line( sys.west, reporter.east, options = arrow_file )
    dia["diagram"].compile( "diagram_B2.pdf" )

    dia = make_diagram()
    make_componentsB( dia )
    dia["diagram"].line( orch.east, sys.west, options = arrow_kobe )
    dia["diagram"].line( data2.west, sys.east, options = arrow_file )
    dia["diagram"].line( sys.west, reporter.east, options = arrow_file )
    coords = (env.west.x-1.5,reporter.west.y)
    report = make_data_block( dia, "rect_e", coords, label="Experiment \\\\ Report" )
    dia["diagram"].line( reporter.west, report.east, options = arrow_file )
    dia["diagram"].compile( "diagram_B3.pdf" )



def make_componentsC( dia ):
    global orch, reporter, conn, env_kobe, sys, spec, data, metrics, report

    orch = make_kobe_block( dia, "rect_c", (0,0), label="KOBE \\\\ Orchestrator" )
    reporter = make_kobe_block( dia, "rect_n", orch.south - (0,1.5), label="KOBE \\\\ Reporter" )
    conn = make_kobe_block( dia, "rect_w", reporter.east + (1.5,0), label="KOBE \\\\ Connector" )
    env_kobe = make_bg_wrapper( dia, [orch,reporter,conn], "KOBE Environment", "NE" )

    sys = make_web_block( dia, "rect_w", conn.east + (1.5,0), label="System 0" )
    spec = make_data_block( dia, "rect_e", orch.west - (1.5,0), label="Experiment \\\\ Specification" )
    metrics = make_web_block( dia, "rect_n", reporter.south - (0,1), label="Metrics \\\\ Database" )
    data = make_data_block( dia, "rect_w", metrics.east + (1.5,0), label="Experiment \\\\ Workload" )
    report = make_data_block( dia, "rect_e", metrics.west - (1.5,0), label="Experiment \\\\ Reports" )


def make_diagramsC():

    arrow_kobe = "blue!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"
    arrow_file = "orange!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"
    arrow_webapi = "black!60!gray, rounded corners=7pt, ultra thick, ->, >=stealth"

    dia = make_diagram()
    make_componentsC( dia )
    dia["diagram"].line( spec.east, orch.west, options = arrow_file )
    dia["diagram"].line( orch.east, conn.north, options = arrow_kobe )
    dia["diagram"].line( data.north, conn.south, options = arrow_file )
    dia["diagram"].line( sys.west, conn.east, options = arrow_webapi )
    dia["diagram"].line( conn.west, reporter.east, options = arrow_kobe )
    dia["diagram"].line( reporter.south, metrics.north, options = arrow_webapi )
    dia["diagram"].line( metrics.west, report.east, arrow_webapi )
    dia["diagram"].compile( "diagram_C1.pdf" )



def make_componentsD( dia ):
    global orch, reporter, conn0, conn1, env, sys0, sys1, spec, data1, data2, metrics

    delta_x = 1.2

    orch = make_kobe_block( dia, "rect_c", (0,0), label="KOBE \\\\ Orchestrator" )
    reporter = make_kobe_block( dia, "rect_n", orch.south - (0,1.5), label="KOBE \\\\ Reporter" )
    conn0 = make_kobe_block( dia, "rect_w", orch.east + (2.7,0), label="KOBE \\\\ Connector" )
    conn1 = make_kobe_block( dia, "rect_w", reporter.east + (0.8,0), label="KOBE \\\\ Connector" )

    env = make_bg_wrapper( dia, [orch,reporter,conn0,conn1], "KOBE \\\\ Environment", "W" )

    coords = (env.east.x+delta_x,conn0.east.y)
    sys0 = make_web_block( dia, "rect_w", coords, label="System" )
    coords = (env.east.x+delta_x,conn1.east.y)
    sys1 = make_web_block( dia, "rect_w", coords, label="System" )

    coords = (env.west.x-delta_x,orch.west.y)
    spec = make_data_block( dia, "rect_e", coords, label="Experiment \\\\ Specification" )
    metrics = make_web_block( dia, "rect_e", reporter.west - (delta_x,0), label="Metrics \\\\ Database" )

    coords = (conn0.north.x-4,env.north.y+1)
    data1 = make_data_block( dia, "rect_s", coords, label="Training \\\\ Dataset" )
    coords = (conn0.north.x,env.north.y+1)
    data2 = make_data_block( dia, "rect_s", coords, label="Testing \\\\ Dataset" )


def make_diagramsD():

    arrow_kobe = "blue!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"
    arrow_file = "orange!80!black, rounded corners=7pt, ultra thick, ->, >=stealth"
    arrow_webapi = "black!60!gray, rounded corners=7pt, ultra thick, ->, >=stealth"

    dia = make_diagram()
    make_componentsD( dia )
    dia["diagram"].line( spec.east, orch.west, options = arrow_file )
    dia["diagram"].line( orch.east, conn0.west, options = arrow_kobe )
    delta_x = conn1.west.x-reporter.east.x
    dia["diagram"].plot_coordinates(
        [ orch.east, orch.east+(delta_x/2,0), conn1.west-(delta_x/2,0), conn1.west ],
        options = arrow_kobe )
    dia["diagram"].line( conn0.east, sys0.west, options = arrow_webapi )
    dia["diagram"].line( conn1.east, sys1.west, options = arrow_webapi )
    dia["diagram"].line( sys0.south, sys1.north, options = arrow_webapi )
    dia["diagram"].line( sys1.north, sys0.south, options = arrow_webapi )

    dia["diagram"].plot_coordinates(
        [ data1.south, (data1.south.x,env.north.y+0.5),
          (conn1.north.x,env.north.y+0.5), conn1.north ],
        options = arrow_file )
    dia["diagram"].plot_coordinates(
        [ data1.south, (data1.south.x,env.north.y+0.5),
          (conn0.north.x,env.north.y+0.5), conn0.north ],
        options = arrow_file )

    dia["diagram"].plot_relative_coordinates(
        [ conn0.south, (0,(env.south.y-conn0.south.y-0.3)),
          (reporter.south.x-conn0.south.x,0), (0,reporter.south.y-env.south.y+0.3) ],
        options = arrow_kobe
    )
    dia["diagram"].plot_relative_coordinates(
        [ conn1.south, (0,(env.south.y-conn1.south.y-0.3)),
          (reporter.south.x-conn1.south.x,0), (0,reporter.south.y-env.south.y+0.3) ],
        options = arrow_kobe
    )

    dia["diagram"].compile( "diagram_D1.pdf" )


    dia = make_diagram()
    make_componentsD( dia )
    dia["diagram"].line( orch.east, conn0.west, options = arrow_kobe )
    delta_x = conn1.west.x-reporter.east.x
    dia["diagram"].plot_coordinates(
        [ orch.east, orch.east+(delta_x/2,0), conn1.west-(delta_x/2,0), conn1.west ],
        options = arrow_kobe )
    dia["diagram"].line( conn0.east, sys0.west, options = arrow_webapi )
    dia["diagram"].line( conn1.east, sys1.west, options = arrow_webapi )
    dia["diagram"].line( sys0.south, sys1.north, options = arrow_webapi )
    dia["diagram"].line( sys1.north, sys0.south, options = arrow_webapi )

    dia["diagram"].plot_coordinates(
        [ data2.south, (data2.south.x,env.north.y+0.5),
          (conn1.north.x,env.north.y+0.5), conn1.north ],
        options = arrow_file )
    dia["diagram"].line( data2.south, conn0.north, options = arrow_file )

    dia["diagram"].plot_relative_coordinates(
        [ conn0.south, (0,(env.south.y-conn0.south.y-0.3)),
          (reporter.south.x-conn0.south.x,0), (0,reporter.south.y-env.south.y+0.3) ],
        options = arrow_kobe
    )
    dia["diagram"].plot_relative_coordinates(
        [ conn1.south, (0,(env.south.y-conn1.south.y-0.3)),
          (reporter.south.x-conn1.south.x,0), (0,reporter.south.y-env.south.y+0.3) ],
        options = arrow_kobe
    )
    
    dia["diagram"].line( reporter.west, metrics.east, options = arrow_webapi )

    dia["diagram"].compile( "diagram_D2.pdf" )


make_diagramsA()
make_diagramsB()
make_diagramsC()
make_diagramsD()
