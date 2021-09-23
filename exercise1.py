import pandas as pd
import math

from utils.Node import Node


# ver como calcular la entropia del atributo pero bien, porque aca no lo hacemos
def calculate_entropy():
    positive_cases = (df[df["Creditability"] == 1].count())[0]
    negative_cases = (df[df["Creditability"] == 0].count())[0]
    total_cases = positive_cases + negative_cases
    to_return = -(positive_cases / total_cases) * math.log2(positive_cases / total_cases) - (negative_cases / total_cases) * math.log2(negative_cases / total_cases)
    #print("Positive cases: ", positive_cases, "\nNegative cases: ", negative_cases, "\nEntropy: ", to_return)
    return to_return, total_cases


def discretize_attributes():
    df["AMOUNT_TYPE"] = 0
    df["AGE_TYPE"] = 0
    df["DURATION_TYPE"] = 0

    df.loc[(df["Credit Amount"] <= 1000), ['AMOUNT_TYPE']] = 1
    df.loc[((df["Credit Amount"] <= 2000) & (df["Credit Amount"] > 1000)), ['AMOUNT_TYPE']] = 2
    df.loc[(df["Credit Amount"] > 2000), ['AMOUNT_TYPE']] = 3
    df.drop('Credit Amount', inplace=True, axis=1)

    df.loc[(df["Age (years)"] <= 25), ['AGE_TYPE']] = 1
    df.loc[((df["Age (years)"] <= 50) & (df["Age (years)"] > 25)), ['AGE_TYPE']] = 2
    df.loc[(df["Age (years)"] > 50), ['AGE_TYPE']] = 3
    df.drop('Age (years)', inplace=True, axis=1)

    df.loc[(df["Duration of Credit (month)"] <= 12), ['DURATION_TYPE']] = 1
    df.loc[((df["Duration of Credit (month)"] <= 24) & (df["Duration of Credit (month)"] > 12)), ['DURATION_TYPE']] = 2
    df.loc[(df["Duration of Credit (month)"] > 24), ['DURATION_TYPE']] = 3
    df.drop('Duration of Credit (month)', inplace=True, axis=1)
    df.rename(columns={"AMOUNT_TYPE": "Credit Amount", "AGE_TYPE": "Age", "DURATION_TYPE": "Duration of Credit"}, inplace=True)


def calculate_gain():
    dic = {}

    for column in df.columns:
        if column != "Creditability":
            dic[column] = {}
            for val_type in df[column].unique():
                dic[column][val_type] = {}
                dic[column][val_type]["positive"] = 0
                dic[column][val_type]["negative"] = 0

    for i in range(len(df)):
        for j in range(1, len(df.columns)):
            if df.iloc[i][0] == 1:
                dic[df.columns[j]][df.iloc[i][j]]["positive"] += 1
            else:
                dic[df.columns[j]][df.iloc[i][j]]["negative"] += 1

    gain_dic = {}

    for column in df.columns:
        if column != "Creditability":
            gain_dic[column] = entropy
            for val_type in dic[column].keys():
                att_entropy, att_cases = calculate_attribute_entropy(dic, column, val_type)
                gain_dic[column] -= (att_cases/total_germans)*att_entropy

    return gain_dic


def calculate_attribute_entropy(dic, column, val_type):
    positive_cases = dic[column][val_type]["positive"]
    negative_cases = dic[column][val_type]["negative"]
    total_cases = positive_cases + negative_cases
    positive_cases /= total_cases
    negative_cases /= total_cases

    if positive_cases == 0.0 or negative_cases == 0.0:
        return 0, total_cases
    else:
        return -positive_cases * math.log2(positive_cases) - negative_cases * math.log2(negative_cases), total_cases


# def calculate_gain_given_attribute(attr, attr_list):
#     dic = {}
#
#     for attr_value in df[attr].unique():
#         # Los attr_value son el 1, 2, 3 y 4 del Account Balance
#         # Entonces los guardo como hijos del nodo padre que es Account Balance
#         parent_node.add_child(attr_value, -1)
#
#         # Por cada valor de Account Balance voy a iniciar un diccionario
#         dic[attr_value] = {}
#         for column in df.columns:
#             if column != "Creditability" and (column not in attr_list):
#                 # Cada atributo que no sea ni Creditability ni Account Balance va a tener su propio diccionario.
#                 # Llamemos a este tributo other_attr
#                 dic[attr_value][column] = {}
#                 for column_value in df[column].unique():
#                     # Cada valor de other_attr (por ejemplo 1, 2, 3) va a tener positivos y negativos
#                     # Aca los inicializo
#                     dic[attr_value][column][column_value] = {}
#                     dic[attr_value][column][column_value]["positive"] = 0
#                     dic[attr_value][column][column_value]["negative"] = 0
#
#     # Para todos los registros, quiero recorrer cada uno de sus atributos, por eso doble for
#     for i in range(len(df)):
#         for j in range(1, len(df.columns)):
#
#             # NO analizo las columnas de los atributos que ya tenemos dados
#             if df.columns[j] not in attr_list:
#
#                 # Lo que si quiero ver es los posibles valores de cada atributo que no es mi attr dado
#                 # Cuando hacemos dic[df.iloc[i][attr]] estamos haciendo el "dado el atributo"
#                 # Porque la posicion df.iloc[i][attr] del dic es la posicion que corresponde a ese posible valor de attr
#                 # Entonces aca solamente contamos positivos y negativos
#
#                 if df.iloc[i][0] == 1:
#                     dic[df.iloc[i][attr]][df.columns[j]][df.iloc[i][j]]["positive"] += 1
#                 else:
#                     dic[df.iloc[i][attr]][df.columns[j]][df.iloc[i][j]]["negative"] += 1
#
#     gain_dic = {}
#
#     # Ahora se viene la papa. Tenemos que hacer la cuenta de la entropia
#     # Para cada posible valor de Account Balance (1,2,3,4) tengo que ver TODOS los demas atributos (menos Creditability)
#     # Y determinar cual es el que tiene mayor ganancia
#
#     # Entonces, para cada valor de Account Balance
#     for attr_value in df[attr].unique():
#
#         # Me calculo la entropia de ese valor (sería H(1), H(2), etc)
#         attr_entropy = calculate_entropy_of_attr(attr, attr_value)
#         gain_dic[attr_value] = {}
#
#         # Ahora, del diccionario generado para los valores 1,2,3,4 me levanto TODOS los nombres de atributos
#         # Y con ese nombre voy a llamar a la funcion calculate_entropy_given_attr, que busca
#         # TODOS los posibles valores de ese atributo y hace el calculo de entropia H(1,Hombre), H(1,Mujer),
#         # Este metodo devuelve directamente la cuentita hecha con la frecuencia relativa de cada valor del
#         # otro atributo, por lo que directamente la restamos y ya
#         for other_attr in dic[attr_value].keys():
#             gain_dic[attr_value][other_attr] = attr_entropy - calculate_entropy_given_attr(dic, attr_value, other_attr)
#
#     return gain_dic


# Voy a hacer el ejemplo de la iteracion de este metodo con Account Balance como nodo raiz
# Es para entender bien que pasa en casa pasito
def calculate_gain_given_attribute(attr, attr_list, current_node, tree_length, desired_tree_length):
    dic = {}

    # Los attr_value son el 1, 2, 3 y 4 del Account Balance
    for attr_value in df[attr].unique():

        # Por cada valor de Account Balance voy a iniciar un diccionario
        dic[attr_value] = {}
        for column in df.columns:
            if column != "Creditability" and (column not in attr_list):
                # Cada atributo que no sea ni Creditability ni Account Balance va a tener su propio diccionario.
                # Llamemos a este tributo other_attr
                dic[attr_value][column] = {}
                for column_value in df[column].unique():
                    # Cada valor de other_attr (por ejemplo 1, 2, 3) va a tener positivos y negativos
                    # Aca los inicializo
                    dic[attr_value][column][column_value] = {}
                    dic[attr_value][column][column_value]["positive"] = 0
                    dic[attr_value][column][column_value]["negative"] = 0

    # Para todos los registros, quiero recorrer cada uno de sus atributos, por eso doble for
    for i in range(len(df)):
        for j in range(1, len(df.columns)):

            # NO analizo las columnas de los atributos que ya tenemos dados
            if df.columns[j] not in attr_list:

                # Lo que si quiero ver es los posibles valores de cada atributo que no es mi attr dado
                # Cuando hacemos dic[df.iloc[i][attr]] estamos haciendo el "dado el atributo"
                # Porque la posicion df.iloc[i][attr] del dic es la posicion que corresponde a ese posible valor de attr
                # Entonces aca solamente contamos positivos y negativos

                if df.iloc[i][0] == 1:
                    dic[df.iloc[i][attr]][df.columns[j]][df.iloc[i][j]]["positive"] += 1
                else:
                    dic[df.iloc[i][attr]][df.columns[j]][df.iloc[i][j]]["negative"] += 1

    gain_dic = {}

    # Ahora se viene la papa. Tenemos que hacer la cuenta de la entropia
    # Para cada posible valor de Account Balance (1,2,3,4) tengo que ver TODOS los demas atributos (menos Creditability)
    # Y determinar cual es el que tiene mayor ganancia

    # Entonces, para cada valor de Account Balance
    for attr_value in df[attr].unique():

        # Me calculo la entropia de ese valor (sería H(1), H(2), etc)
        attr_entropy = calculate_entropy_of_attr(attr, attr_value)
        gain_dic[attr_value] = {}

        # Ahora, del diccionario generado para los valores 1,2,3,4 me levanto TODOS los nombres de atributos
        # Y con ese nombre voy a llamar a la funcion calculate_entropy_given_attr, que busca
        # TODOS los posibles valores de ese atributo y hace el calculo de entropia H(1,Hombre), H(1,Mujer),
        # Este metodo devuelve directamente la cuentita hecha con la frecuencia relativa de cada valor del
        # otro atributo, por lo que directamente la restamos y ya
        for other_attr in dic[attr_value].keys():
            gain_dic[attr_value][other_attr] = attr_entropy - calculate_entropy_given_attr(dic, attr_value, other_attr)

    # A esta altura, en gain_dic tengo todas las entropias de todos los atributos hijos de Account Balance
    # Voy a iterar por cada uno de estos valores, y dentro de cada uno de estos valores por cada otro atributo
    # Para ver cual de estos atributos tiene mas ganancia. El que tenga mas ganancia es un nuevo hijo de
    # Account Balance
    for attr_value in df[attr].unique():
        # Agrego al atributo maximo como hijo de Account Balance
        new_child_name = max(gain_dic[attr_value], key=gain_dic[attr_value].get)
        new_node = current_node.add_child(new_child_name, attr, attr_value)
        # Creo una lista auxiliar para no romper la lista de atributos que tengo hasta ahora
        other_list = attr_list.copy()
        other_list.append(new_child_name)

        # Recursivamente llamo esta funcion para construir el arbol
        if tree_length < desired_tree_length:
            calculate_gain_given_attribute(new_child_name, other_list, new_node, tree_length+1, desired_tree_length)
        else:
            return


def calculate_entropy_of_attr(attr, attr_value):
    df_positive_cases = df[df["Creditability"] == 1]
    positive_cases = (df_positive_cases[df_positive_cases[attr] == attr_value].count())[0]

    df_negative_cases = df[df["Creditability"] == 0]
    negative_cases = (df_negative_cases[df_negative_cases[attr] == attr_value].count())[0]

    total_cases = positive_cases + negative_cases
    positive_cases /= total_cases
    negative_cases /= total_cases

    if positive_cases == 0.0 or negative_cases == 0.0:
        return 0
    else:
        return -positive_cases * math.log2(positive_cases) - negative_cases * math.log2(negative_cases)


def calculate_entropy_given_attr(dic, attr_value, other_attr):
    attr_entropy = 0
    total_cases = 0

    # Necesito que de aca adentro salga algo del estilo 0.5 * H(1,"Hombre") + 0.5 * H(1,"Mujer")
    # Entonces por cada posible valor del otro atributo (ejemplo, "Hombre", "Mujer", etc)
    for other_attr_value in dic[attr_value][other_attr].keys():
        positive_cases = dic[attr_value][other_attr][other_attr_value]["positive"]
        negative_cases = dic[attr_value][other_attr][other_attr_value]["negative"]
        current_cases = (positive_cases + negative_cases)

        if current_cases != 0:
            total_cases += current_cases
            previous_entropy = 0

            # Al salir de estos dos if, en previous_entropy tengo H(1,"Mujer"), H(1,"Hombre"), etc
            if positive_cases != 0:
                previous_entropy += (-positive_cases / current_cases) * math.log2(positive_cases/current_cases)
            if negative_cases != 0:
                previous_entropy += (-negative_cases / current_cases) * math.log2(negative_cases / current_cases)

            # A previous_entropy lo multiplico por los current_cases, que son la cantidad de Hombres, Mujeres, etc
            attr_entropy += previous_entropy * current_cases

    # Cuando salgo de ese for, en attr_entropy tengo 3*H(1,"Mujer") * 4*H(1,"Hombre")
    # Lo que quiero ahora es dividir por los casos totales que hay, o sea sumar la cantidad de Hombres, Mujeres, etc
    attr_entropy /= total_cases

    # Devuelvo toda esa cuenta que es la entropia del atributo other_attr
    return attr_entropy


# todo cambiar este df, ya que estamos entrenando con todo el conjunto de datos
df = pd.read_csv("resources/german_credit.csv")
discretize_attributes()
entropy, total_germans = calculate_entropy()
gain = calculate_gain()
parent_node = Node(max(gain, key=gain.get), "root", "root")
calculate_gain_given_attribute(parent_node.name, [parent_node.name], parent_node, 1, 3)
parent_node.print_node()
