import os
os.chdir('/Users/Tony/Documents/Git Folder/seelviz/Jupyter/DownsampleGraphML/')

from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly import tools
import plotly
plotly.offline.init_notebook_mode()

import numpy as np
import nibabel as nb
import networkx as nx
import pandas as pd
import re

import plotly.plotly as py
from plotly.graph_objs import *

# Change the filename below to run different graphml files
# Deliverable was Cocaine174
graphMLfilename = 'Cocaine174localeq.5000.graphml'
G = nx.read_graphml(graphMLfilename)

attributes = nx.get_node_attributes(G, 'attr')

## This finds the maximum number of edges and the densest node.

maxEdges = 0
densestNode = ""
for i in range(len(G.edges())):
    if ((len(G.edges('s' + str(i))) > maxEdges)):
        maxEdges = len(G.edges('s' + str(i)))
        densestNode = "s" + str(i)

## Find each node with a given number of edges, from 0 edges to maxEdges

## Find and store number of edges for each node in storageDict
## Key is 's1', value is number of edges
storageDict = {}

for n in G.nodes_iter():
    storageDict[n] = len(G.edges(n))

orderedNodesEdgeCounts = OrderedDict(sorted(storageDict.items(), key=lambda (key, value): int(key.split('s')[1])))

## Create ordered list to visualize data
sortedList = sorted(storageDict.values())

# Calculate basic statistics
statisticsArray = np.array(sortedList)
averageNumberEdges = np.mean(statisticsArray)
stdNumberEdges = np.std(statisticsArray)

print "average edge count:"
print averageNumberEdges
print "standard deviation edge count: "
print stdNumberEdges

# using 95th percentile as upper limit (z = 1.96)
upperLimit = averageNumberEdges + 1.96 * stdNumberEdges
print "95th percentile: "
print upperLimit

##unused

## numberEdges is used for plotting (first element is edges for 's1', etc.)
numberEdges = []
k = 0
for i in range(1, (len(G.nodes()) + 1)):
    numberEdges.append(orderedNodesEdgeCounts['s' + str(i)])
    k = k + 1

## Number of colors is maxEdges
numColors = maxEdges;

# scaledEdges = [float(numberEdges[i])/float(upperLimit) for i in range(len(numberEdges))]
scaledEdges = [float(numberEdges[i])/float(maxEdges) for i in range(len(numberEdges))]

##Tweak this to change the heat map scaling for the points.  Remove outliers.

heatMapBrain = [
        # Let null values (0.0) have color rgb(0, 0, 0)
        [0, 'rgb(0, 0, 0)'],  #black
    
        # Let first 5-10% (0.05) of the values have color rgb(204, 0, 204)
        [0.05, 'rgb(153, 0, 153)'],  #purple
        [0.1, 'rgb(153, 0, 153)'],  #purple

        # Let next 10-15% (0.05) of the values have color rgb(204, 0, 204)
        [0.1, 'rgb(204, 0, 204)'],  #purple
        [0.15, 'rgb(204, 0, 204)'],  #purple

        # Let values between 20-25% have color rgb(0, 0, 153)
        [0.15, 'rgb(0, 0, 153)'],    #blue
        [0.2, 'rgb(0, 0, 153)'],    #blue
    
        # Let values between 25-30% have color rgb(0, 0, 204)
        [0.2, 'rgb(0, 0, 204)'],    #blue
        [0.25, 'rgb(0, 0, 204)'],    #blue
    
        [0.25, 'rgb(0, 76, 153)'],    #blue
        [0.3, 'rgb(0, 76, 153)'],    #blue

        [0.3, 'rgb(0, 102, 204)'],  #light blue
        [0.35, 'rgb(0, 102, 204)'],  #light blue
    
        [0.35, 'rgb(0, 153, 153)'],  #light blue
        [0.4, 'rgb(0, 153, 153)'],  #light blue
    
        [0.4, 'rgb(0, 204, 204)'],  #light blue
        [0.45, 'rgb(0, 204, 204)'],  #light blue

        [0.45, 'rgb(0, 153, 76)'],
        [0.5, 'rgb(0, 153, 76)'],
    
        [0.5, 'rgb(0, 204, 102)'],
        [0.55, 'rgb(0, 204, 102)'],

        [0.55, 'rgb(0, 255, 0)'],
        [0.6, 'rgb(0, 255, 0)'],
    
        [0.6, 'rgb(128, 255, 0)'],
        [0.65, 'rgb(128, 255, 0)'],

        [0.65, 'rgb(255, 255, 0)'],
        [0.7, 'rgb(255, 255, 0)'],

        [0.7, 'rgb(255, 255, 102)'], #
        [0.75, 'rgb(255, 255, 102)'], #
    
        [0.75, 'rgb(255, 128, 0)'],
        [0.8, 'rgb(255, 128, 0)'],

        [0.8, 'rgb(204, 0, 0)'], #
        [0.85, 'rgb(204, 0, 0)'], #

        [0.85, 'rgb(255, 0, 0)'],
        [0.9, 'rgb(255, 0, 0)'],

        [0.9, 'rgb(255, 51, 51)'], #
        [0.95, 'rgb(255, 51, 51)'], #

        [0.95, 'rgb(255, 255, 255)'],
        [1.0, 'rgb(255, 255, 255)']
    ]

def get_brain_figure(g, plot_title=''):
    """
    Returns the plotly figure object for vizualizing a 3d brain network.

    g: networkX object of brain
    """

    # grab the node positions from the graphML file
    V = nx.number_of_nodes(g)
    attributesGraph = nx.get_node_attributes(g,'attr')
    node_positions_3d = pd.DataFrame(columns=['x', 'y', 'z'], index=range(V))
    for n in g.nodes_iter():
        node_positions_3d.loc[n] = [int((re.findall('\d+', str(attributes[n])))[0]), int((re.findall('\d+', str(attributes[n])))[1]), int((re.findall('\d+', str(attributes[n])))[2])]

    # grab edge endpoints
    edge_x = []
    edge_y = []
    edge_z = []

    for e in g.edges_iter():
        source_pos = node_positions_3d.loc[e[0]]
        target_pos = node_positions_3d.loc[e[1]]
    
        edge_x += [source_pos['x'], target_pos['x'], None]
        edge_y += [source_pos['y'], target_pos['y'], None]
        edge_z += [source_pos['z'], target_pos['z'], None]

    Xlist = []
    for i in range(1, len(g.nodes()) + 1):
        Xlist.append(int((re.findall('\d+', str(attributesGraph['s' + str(i)])))[0]))

    Ylist = []
    for i in range(1, len(g.nodes()) + 1):
        Ylist.append(int((re.findall('\d+', str(attributesGraph['s' + str(i)])))[1]))

    Zlist = []
    for i in range(1, len(g.nodes()) + 1):
        Zlist.append(int((re.findall('\d+', str(attributesGraph['s' + str(i)])))[2]))
    
    # node style
    node_trace = Scatter3d(x=Xlist,
                           y=Ylist,
                           z=Zlist,
                           mode='markers',
                           # name='regions',
                           marker=Marker(symbol='dot',
                                         size=6,
                                         opacity=0,
                                         color=scaledEdges,
                                         colorscale=heatMapBrain),     
                                       # text=[str(r) for r in range(V)],
                                       # text=atlas_data['nodes'],
                           hoverinfo='text')
    # edge style
    '''edge_trace = Scatter3d(x=edge_x,
                           y=edge_y,
                           z=edge_z,
                           mode='lines',
                           line=Line(color='cyan', width=1),
                           hoverinfo='none')'''
    
    # axis style
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False)
    
    # overall layout
    layout = Layout(title=plot_title,
                    width=800,
                    height=900,
                    showlegend=False,
                    scene=Scene(xaxis=XAxis(axis),
                                yaxis=YAxis(axis),
                                zaxis=ZAxis(axis)),
                    margin=Margin(t=50),
                    hovermode='closest',
                    paper_bgcolor='rgba(1,1,1,1)',
                    plot_bgcolor='rgb(1,1,1)')

    data = Data([node_trace])
    fig = Figure(data=data, layout=layout)

    return fig

output = get_brain_figure(G, '')

outputlocation = '../../reveal/html/graphmlhtmls/'
plotly.offline.plot(output, filename = outputlocation + graphMLfilename + '.html')

# Get list of all possible number of edges, in order
setOfAllPossibleNumEdges = set(sortedList)
listOfAllPossibleNumEdges = list(setOfAllPossibleNumEdges)
#listOfAllScaledEdgeValues = [listOfAllPossibleNumEdges[i]/upperLimit for i in range(len(listOfAllPossibleNumEdges))]
listOfAllScaledEdgeValues = [listOfAllPossibleNumEdges[i]/float(maxEdges) for i in range(len(listOfAllPossibleNumEdges))]


#heatMapBrain

data = Data([
    Scatter(
        y=listOfAllPossibleNumEdges,
        marker=Marker(
            size=16,
            color=listOfAllPossibleNumEdges,
            colorbar=ColorBar(
                title='Colorbar'
            ),
            colorscale=heatMapBrain,
        ),
        mode='markers')
])

layout = Layout(title=graphMLfilename + ' false coloration scheme',
                    width=800,
                    height=900,
                    showlegend=False,
                    margin=Margin(t=50),
                    hovermode='closest',
                    xaxis=dict(
                        title='Number of Unique Colors',
                        titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#000000')
                        ),
                    yaxis=dict(
                        title='Number of Edges',
                        titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#000000')
                        ),
                    paper_bgcolor='rgba(255,255,255,255)',
                    plot_bgcolor='rgb(255,255,255)')

mapping = Figure(data=data, layout=layout)
iplot(mapping, validate=False)

outputlocation = '../../reveal/html/graphmlhtmls/'
plotly.offline.plot(mapping, filename = outputlocation + graphMLfilename + 'heatmap' + '.html')