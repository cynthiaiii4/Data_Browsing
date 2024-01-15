import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def FeatureXMLGenerate(features):
    numeric_features = []
    categorical_features = []

    for key, value in features.items():
        if value == '數值':
            numeric_features.append(key)
        elif value == '類別':
            categorical_features.append(key)
    categorical_features.append("規模")
    root = ET.Element("StockAnalysis")
    #displot
    graph = ET.Element("Graph")
    chart_type=ET.Element("ChartType")
    chart_type.text = "displot"
    x_element = ET.Element("X")
    x_element.text = "區間股價變化率(最高價)"
    graph.append(chart_type)
    graph.append(x_element)
    root.append(graph)

    #countplot
    graph = ET.Element("Graph")
    chart_type=ET.Element("ChartType")
    chart_type.text = "countplot"
    x_element = ET.Element("X")
    x_element.text = categorical_features[0]
    graph.append(chart_type)
    graph.append(x_element)
    root.append(graph)

    #violinplot
    graph = ET.Element("Graph")
    y_element=ET.Element("Y")
    y_element.text = "區間股價變化率(最高價)"
    graph.append(y_element)
    chart_type=ET.Element("ChartType")
    chart_type.text = "violinplot"
    graph.append(chart_type)
    x_element = ET.Element("X")
    if len(categorical_features)>2:
        x_element.text = categorical_features[1]
    else:
        x_element.text = categorical_features[0]
    graph.append(x_element)
    root.append(graph)

    #catplot
    graph = ET.Element("Graph")
    y_element=ET.Element("Y")
    y_element.text = "區間股價變化率(最高價)"
    graph.append(y_element)
    chart_type=ET.Element("ChartType")
    chart_type.text = "catplot"
    graph.append(chart_type)
    chart_parm=ET.Element("Chart_parm")
    chart_parm.text = "bar"
    graph.append(chart_parm)
    x_element = ET.Element("X")
    if len(categorical_features)>3:
        x_element.text = categorical_features[2]
    else:
        x_element.text = categorical_features[0]
    graph.append(x_element)
    root.append(graph)

    #scatter
    graph = ET.Element("Graph")
    y_element=ET.Element("Y")
    y_element.text = "區間股價變化率(最高價)"
    graph.append(y_element)
    chart_type=ET.Element("ChartType")
    chart_type.text = "scatter"
    graph.append(chart_type)
    x_element = ET.Element("X")
    x_element.text = numeric_features[2]
    graph.append(x_element)
    root.append(graph)

    #regplot
    graph = ET.Element("Graph")
    y_element=ET.Element("Y")
    y_element.text = "區間股價變化率(最高價)"
    graph.append(y_element)
    chart_type=ET.Element("ChartType")
    chart_type.text = "regplot"
    graph.append(chart_type)
    x_element = ET.Element("X")
    x_element.text = numeric_features[0]
    graph.append(x_element)
    root.append(graph)

    #bubbleplot
    if len(numeric_features)>1:
        graph = ET.Element("Graph")
        y_element=ET.Element("Y")
        y_element.text = "區間股價變化率(最高價)"
        graph.append(y_element)
        chart_type=ET.Element("ChartType")
        chart_type.text = "bubbleplot"
        graph.append(chart_type)
        x_element = ET.Element("X")
        if len(numeric_features)>3:
            x_element.text = numeric_features[3]
        else:
            x_element.text = numeric_features[0]
        graph.append(x_element)
        x_element = ET.Element("X")
        if len(numeric_features)>4:
            x_element.text = numeric_features[4]
        else:
            x_element.text = numeric_features[1]
        graph.append(x_element)
        root.append(graph)

    #pairplot
    if len(numeric_features)>3:
        graph = ET.Element("Graph")
        y_element=ET.Element("Y")
        y_element.text = "區間股價變化率(最高價)"
        graph.append(y_element)
        chart_type=ET.Element("ChartType")
        chart_type.text = "pairplot"
        graph.append(chart_type)
        x_element = ET.Element("X")
        x_element.text = numeric_features[0]
        graph.append(x_element)
        x_element = ET.Element("X")
        x_element.text = numeric_features[1]
        graph.append(x_element)
        x_element = ET.Element("X")
        x_element.text = numeric_features[2]
        graph.append(x_element)
        x_element = ET.Element("X")
        x_element.text = numeric_features[3]
        graph.append(x_element)
        root.append(graph)

    # Create a new XML tree
    tree = ET.ElementTree(root)

    xml_str = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent="  ")
    # Save the XML to a file
    with open("xml/stock_analysis.xml", "wb") as f:
        f.write(xml_str.encode('utf-8'))
