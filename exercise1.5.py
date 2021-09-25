import random

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import math
import time



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
def calculate_gain_given_attribute(attr_list, attr_value_list, current_node, tree_length, desired_tree_length):
    dic = {}

    # Los attr_value son el 1, 2, 3 y 4 del Account Balance
    # for attr_value in df[attr].unique():

    # Por cada valor de Account Balance voy a iniciar un diccionario
    # dic[attr_list[-1]] = {}
    for column in df.columns:
        if column != "Creditability" and (column not in attr_list):
            # Cada atributo que no sea ni Creditability ni Account Balance va a tener su propio diccionario.
            # Llamemos a este tributo other_attr

            dic[column] = {}
            for column_value in df[column].unique():
                # Cada valor de other_attr (por ejemplo 1, 2, 3) va a tener positivos y negativos
                # Aca los inicializo
                dic[column][column_value] = {}
                dic[column][column_value]["positive"] = 0
                dic[column][column_value]["negative"] = 0

    # Para todos los registros, quiero recorrer cada uno de sus atributos, por eso doble for
    for i in range(len(df)):
        for j in range(1, len(df.columns)):
            process_me = True

            # NO analizo las columnas de los atributos que ya tenemos dados
            if df.columns[j] not in attr_list:

                # Solo tomo los que tienen columnas de igual valor del attr_value_list
                # (esto es respetar que si es Sol->Humedad, esté considerando solo los "Sol")
                for k in range(len(attr_list)):
                    processed_attr_name = attr_list[k]
                    processed_attr_value = attr_value_list[k]
                    if df.iloc[i][processed_attr_name] != processed_attr_value:
                        process_me = False

                # Lo que si quiero ver es los posibles valores de cada atributo que no es mi attr dado
                # Cuando hacemos dic[df.iloc[i][attr]] estamos haciendo el "dado el atributo"
                # Porque la posicion df.iloc[i][attr] del dic es la posicion que corresponde a ese posible valor de attr
                # Entonces aca solamente contamos positivos y negativos
                if process_me:
                    if df.iloc[i][0] == 1:
                        dic[df.columns[j]][df.iloc[i][j]]["positive"] += 1
                    else:
                        dic[df.columns[j]][df.iloc[i][j]]["negative"] += 1

    gain_dic = {}

    # Ahora se viene la papa. Tenemos que hacer la cuenta de la entropia
    # Para cada posible valor de Account Balance (1,2,3,4) tengo que ver TODOS los demas atributos (menos Creditability)
    # Y determinar cual es el que tiene mayor ganancia

    # Entonces, para cada valor de Account Balance


    # Me calculo la entropia de ese valor (sería H(1), H(2), etc)
    attr_entropy = calculate_entropy_of_attr(attr_list, attr_value_list)
    if attr_entropy == 0:
        node_val = final_value_of(attr_list[-1], attr_value_list[-1], attr_list, attr_value_list)
        current_node.set_node_final(node_val)
        return
    # gain_dic[attr_value] = {}

    # Ahora, del diccionario generado para los valores 1,2,3,4 me levanto TODOS los nombres de atributos
    # Y con ese nombre voy a llamar a la funcion calculate_entropy_given_attr, que busca
    # TODOS los posibles valores de ese atributo y hace el calculo de entropia H(1,Hombre), H(1,Mujer),
    # Este metodo devuelve directamente la cuentita hecha con la frecuencia relativa de cada valor del
    # otro atributo, por lo que directamente la restamos y ya
    for other_attr in dic.keys():
        aux = calculate_entropy_given_attr(dic, other_attr)
        # print("ATTR_ENTROPY = ", attr_entropy, ", OTHER_ATTR_ENTROPY = ", aux)
        gain_dic[other_attr] = attr_entropy - aux

    # A esta altura, en gain_dic tengo todas las entropias de todos los atributos hijos de Account Balance
    # Voy a iterar por cada uno de estos valores, y dentro de cada uno de estos valores por cada otro atributo
    # Para ver cual de estos atributos tiene mas ganancia. El que tenga mas ganancia es un nuevo hijo de
    # Account Balance
    # for attr_value in df[attr].unique():

    # Agrego al atributo maximo como hijo de Account Balance
    new_child_name = max(gain_dic, key=gain_dic.get)
    new_node = current_node.add_child(new_child_name, attr_list[-1], attr_value_list[-1])

    # Creo una lista auxiliar para no romper la lista de atributos que tengo hasta ahora
    other_list = attr_list.copy()
    other_list.append(new_child_name)

    for other_attr_value in df[new_child_name].unique():

        if time_to_prune(attr_list, attr_value_list):
            final_child = new_node.add_child("FINAL_NODE", new_child_name, other_attr_value)
            final_value = final_value_of(new_child_name, other_attr_value, attr_list, attr_value_list)
            final_child.set_node_final(final_value)
        else:
            other_value_list = attr_value_list.copy()
            other_value_list.append(other_attr_value)

            # Recursivamente llamo esta funcion para construir el arbol
            if tree_length < desired_tree_length:
                calculate_gain_given_attribute(other_list, other_value_list, new_node, tree_length+1, desired_tree_length)

            # Si llegue al tamaño maximo del arbol, quiero que el ultimo nodo tenga una hoja por cada uno de sus
            # posibles valores. Y si es un "si" o un "no" depende de cuantos positivos y negativos tenga
            else:
                final_child = new_node.add_child("FINAL_NODE", new_child_name, other_attr_value)
                final_value = final_value_of(new_child_name, other_attr_value, attr_list, attr_value_list)
                final_child.set_node_final(final_value)


# Este metodo se ejecuta y decide si ya tenemos que podar
def time_to_prune(attr_list, attr_value_list):
    aux_df = df.copy()

    # Solo me quedo con los que cumplen todos los "dado el atributo previo"
    for a in range(len(attr_list)):
        aux_df = aux_df.loc[df[attr_list[a]] == attr_value_list[a]]

    positive_cases = (aux_df[aux_df["Creditability"] == 1].count())[0]
    negative_cases = (aux_df[aux_df["Creditability"] == 0].count())[0]
    #print("Pos = ", positive_cases, ", Negative = ", negative_cases)

    if positive_cases >= 3*negative_cases or negative_cases >= 3*positive_cases:
        return True
    else:
        return False


def final_value_of(new_child_name, other_attr_value, attr_list, attr_value_list):
    aux_df = df.copy()

    # Solo me quedo con los que cumplen todos los "dado el atributo previo"
    for a in range(len(attr_list)):
        aux_df = aux_df.loc[df[attr_list[a]] == attr_value_list[a]]

    aux_df = aux_df.loc[df[new_child_name] == other_attr_value]
    positive_cases = (aux_df[aux_df["Creditability"] == 1].count())[0]
    negative_cases = (aux_df[aux_df["Creditability"] == 0].count())[0]
    if positive_cases >= negative_cases:
        return 1
    else:
        return 0


def calculate_entropy_of_attr(attr_list, attr_value_list):
    # df_positive_cases = df[df["Creditability"] == 1]
    # positive_cases = (df_positive_cases[df_positive_cases[attr] == attr_value].count())[0]
    #
    # df_negative_cases = df[df["Creditability"] == 0]
    # negative_cases = (df_negative_cases[df_negative_cases[attr] == attr_value].count())[0]
    #
    # total_cases = positive_cases + negative_cases
    # positive_cases /= total_cases
    # negative_cases /= total_cases

    aux_df = df.copy()

    # Solo me quedo con los que cumplen todos los "dado el atributo previo"
    for a in range(len(attr_list)):
        aux_df = aux_df.loc[df[attr_list[a]] == attr_value_list[a]]

    positive_cases = (aux_df[aux_df["Creditability"] == 1].count())[0]
    negative_cases = (aux_df[aux_df["Creditability"] == 0].count())[0]
    previous_entropy = 0
    total_cases = positive_cases + negative_cases

    if positive_cases != 0:
        previous_entropy += (-positive_cases / total_cases) * math.log2(positive_cases / total_cases)
    if negative_cases != 0:
        previous_entropy += (-negative_cases / total_cases) * math.log2(negative_cases / total_cases)

    return previous_entropy


def calculate_entropy_given_attr(dic, other_attr):
    attr_entropy = 0
    total_cases = 0

    # Necesito que de aca adentro salga algo del estilo 0.5 * H(1,"Hombre") + 0.5 * H(1,"Mujer")
    # Entonces por cada posible valor del otro atributo (ejemplo, "Hombre", "Mujer", etc)
    for other_attr_value in dic[other_attr].keys():
        positive_cases = dic[other_attr][other_attr_value]["positive"]
        negative_cases = dic[other_attr][other_attr_value]["negative"]
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
    # Si no tengo casos retorno 0
    if total_cases == 0:
        return 0

    attr_entropy /= total_cases

    # Devuelvo toda esa cuenta que es la entropia del atributo other_attr
    return attr_entropy


# Necesito el 70% del total de negativos
def divide_data_balanced(percentage):
    positive_df = df.drop(df[df["Creditability"] == 0].index)
    positive_df = positive_df.sample(frac=1).reset_index(drop=True)
    negative_df = df.drop(df[df["Creditability"] == 1].index)

    ret_df = negative_df.append(positive_df[:len(negative_df)])
    ret_df = ret_df.sample(frac=1).reset_index(drop=True)
    total_test_data = int(len(ret_df) * percentage)

    return ret_df[:total_test_data], ret_df[total_test_data:]


def divide_data(percentage):
    aux = df
    total_test_data = int(len(aux) * percentage)
    aux = aux.sample(frac=1).reset_index(drop=True)
    return aux[:total_test_data], aux[total_test_data:]


# Fijo el tiempo de salida
start_time = time.time()

# Levanto los datos y los discretizo
df = pd.read_csv("resources/german_credit.csv")
discretize_attributes()

# Separo el conjunto de entrenamiento y el de testeo
df, test_data = divide_data(0.8)

# Calculo las entropias y ganancias
entropy, total_germans = calculate_entropy()
gain = calculate_gain()
# parent_node = Node(max(gain, key=gain.get), "root", "root")
#
# # Por cada posible valor de Account Balance me hago la rama
# for val in df[parent_node.name].unique():
#     calculate_gain_given_attribute([parent_node.name], [val], parent_node, 1, 3)
#
# # Clasifico los ejemplos de test
# for n in range(len(test_data)):
#     parent_node.classify(test_data.iloc[n])
#
# print("(TEST) TOTAL CLASSIFIED: ", parent_node.total_classified, ", TOTAL_OK: ", parent_node.total_ok, ", TOTAL_CLASSIFIED_WITH_ONE = ", parent_node.total_classified_one, ", PRECISION = ", parent_node.total_ok/parent_node.total_classified)
#
# # Clasifico los ejemplos de train
# parent_node.reset()
# for n in range(len(df)):
#     parent_node.classify(df.iloc[n])
#
# print("(TRAIN) TOTAL CLASSIFIED: ", parent_node.total_classified, ", TOTAL_OK: ", parent_node.total_ok, ", TOTAL_CLASSIFIED_WITH_ONE = ", parent_node.total_classified_one, ", PRECISION = ", parent_node.total_ok/parent_node.total_classified)
#
# print("--- %s seconds ---" % (time.time() - start_time))


class Node:
    def __init__(self, value, name, isFinal = False):
        self.name = name
        self.value = value
        self.children = {}
        self.is_final = isFinal
        self.total_classified = 0
        self.true_positive = 0
        self.true_negative = 0
        self.false_negative = 0
        self.false_positive = 0
        self.classified_correct = 0
        self.total_classified_one = 0

    def print_node(self, previous="", parent_value=""):
        if self.is_final:
            print(previous, parent_value, self.value)
        else:
            print(previous, parent_value, self.value)
            previous += "\t"
            for key in self.children.keys():
                self.children[key].print_node(previous, parent_value=key)

    def classify(self, row):
        current_node = self
        depth = 0
        while True:
            if current_node.is_final:
                # print("Creditability = ", row["Creditability"], ", Classified = ", current_node.value)
                self.total_classified += 1
                if row["Creditability"] == current_node.value:
                    self.classified_correct += 1
                    if current_node.value == 1:
                        self.true_positive += 1
                    else:
                        self.true_negative += 1
                else:
                    if row["Creditability"] == 1:
                        self.false_negative += 1
                    else:
                        self.true_positive += 1
                if current_node.value == 1:
                    self.total_classified_one += 1
                if row["Creditability"] == current_node.value:
                    return True
                return False
            aux2 = row[current_node.name]
            depth += 1
            if aux2 in current_node.children:
                current_node = current_node.children[aux2]
            else:
                return False

    def reset(self):
        self.total_classified = 0
        self.true_positive = 0
        self.total_classified_one = 0


def entropy_df(df):
    positive_cases = (df[df["Creditability"] == 1].count())[0]
    negative_cases = (df[df["Creditability"] == 0].count())[0]
    total_cases = positive_cases + negative_cases
    acum = 0
    if negative_cases != 0:
        acum += -(negative_cases / total_cases) * math.log2(negative_cases / total_cases)
    if positive_cases != 0:
        acum = -(positive_cases / total_cases) * math.log2(positive_cases / total_cases)
    return acum


def gain(df, attr):
    H = entropy_df(df)
    Hs = {}
    for value in df[attr].unique():
        dfTemp = df.copy()
        dfTemp.drop(dfTemp.index[dfTemp[attr] != value], inplace=True)
        Hs[value] = entropy_df(dfTemp) * dfTemp[attr].count() / df[attr].count()
    total=H
    # todo SE PUEDE HACER CON ACUM
    for value in df[attr].unique():
           total -= Hs[value]
    return total


def create_tree_rec(df_cut, number=-1, podas=False):
    if df_cut["Creditability"].nunique() == 1:
        return Node(1 if df_cut["Creditability"].unique() == 1 else 0, "Creditability", isFinal=True)
    if df_cut.columns.nunique() == 2:
        positives = (df_cut[df_cut["Creditability"] == 1].count())[0]
        negatives = (df_cut[df_cut["Creditability"] == 0].count())[0]
        if positives < negatives:
            return Node(1, "Creditability", isFinal=True)
        return Node(0, "Creditability", isFinal=True)

    gain_map = {}
    for attr in df_cut.columns:
        if attr != "Creditability":
            gain_map[attr] = gain(df_cut, attr)
    max_gain_attr = max(gain_map, key=gain_map.get)

    if podas:
        if df_cut["Creditability"].count() < 20:
            positives = (df_cut[df_cut["Creditability"] == 1].count())[0]
            negatives = (df_cut[df_cut["Creditability"] == 0].count())[0]
            if positives > negatives:
                return Node(1, "Creditability", isFinal=True)
            return Node(0, "Creditability", isFinal=True)
        positives = (df_cut[df_cut["Creditability"] == 1].count())[0]
        negatives = (df_cut[df_cut["Creditability"] == 0].count())[0]

        if positives/negatives > 3 or negatives/positives > 3:
            if positives > negatives:
                return Node(1, "Creditability", isFinal=True)
            return Node(0, "Creditability", isFinal=True)

    this_node = Node(number, max_gain_attr)
    for value in df_cut[max_gain_attr].unique():
        dfTemp = df_cut.copy()
        dfTemp.drop(dfTemp.index[dfTemp[max_gain_attr] != value], inplace=True)
        this_node.children[value] = (create_tree_rec(dfTemp, value, podas=True))

    for value in df[max_gain_attr].unique():
        if value not in df_cut[max_gain_attr].unique():
            positives = (df_cut[df_cut["Creditability"] == 1].count())[0]
            negatives = (df_cut[df_cut["Creditability"] == 0].count())[0]
            if positives > negatives:
                this_node.children[value] = Node(1, "Creditability", isFinal=True)
            else:
                this_node.children[value] = Node(0, "Creditability", isFinal=True)

    return this_node

def confusion_matrix(node):
    array = [[0, 0], [0, 0]]
    array[0][0] = node.true_positive
    array[1][0] = node.false_negative
    array[0][1] = node.false_positive
    array[1][1] = node.true_negative
    df_cm = pd.DataFrame(array, index=["Positive", "Negative"],
                         columns=["Positive", "Negative"])
    ax = plt.figure(figsize=(10, 7))
    sn.heatmap(df_cm, annot=True, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Ground Truth")
    plt.show()
    return array


tree = create_tree_rec(df, podas=True)
tree.print_node()


for n in range(len(test_data)):
    val = tree.classify(test_data.iloc[n])
confusion_matrix(tree)


print("(TEST) TOTAL CLASSIFIED: ", tree.total_classified, ", TOTAL_OK: ", tree.classified_correct,
      ", TOTAL_CLASSIFIED_WITH_ONE = ", tree.total_classified_one, ", PRECISION = ", tree.classified_correct / tree.total_classified)

# Clasifico los ejemplos de train
tree.reset()
for n in range(len(df)):
    val = tree.classify(df.iloc[n])

print("(TRAIN) TOTAL CLASSIFIED: ", tree.total_classified, ", TOTAL_OK: ", tree.true_positive,
      ", TRUE POSITIVES = ", tree.true_positive, ", PRECISION = ", tree.classified_correct / tree.total_classified)

random_forest = []
tree_amount = 5
for k in range(tree_amount):
    dfTemp = df.copy()
    dfTemp = dfTemp.sample(frac=0.6, replace=True)
    random_forest.insert(k, create_tree_rec(dfTemp, podas=True))

print("RANDOM FOREST CREATED")

true_positive = 0
false_negative = 0
false_positive = 0
true_negative = 0
total_classified, total_ok, total_classified_one = 0, 0, 0

for n in range(len(test_data)):
    positives, negatives = 0, 0
    for k in range(tree_amount):
        result = random_forest[k].classify(test_data.iloc[n])
        if result:
            positives += 1
        else:
            negatives += 1
    total_classified += 1
    if positives > negatives:
        total_classified_one += 1
    if test_data.iloc[n]["Creditability"] == (1 if positives > negatives else 0):
        total_ok += 1
        if test_data.iloc[n]["Creditability"] == 1:
            true_positive += 1
        else:
            true_negative += 1
    else:
        if test_data.iloc[n]["Creditability"] == 1:
            false_negative += 1
        else:
            false_positive += 1

print("(RANDOM FOREST) TOTAL CLASSIFIED: ", total_classified, ", TOTAL_OK: ", total_ok, ", TOTAL_CLASSIFIED_WITH_ONE = "
      , total_classified_one, ", PRECISION = ", total_ok/total_classified)

tmp = Node("asd", 1)
tmp.true_positive = true_positive
tmp.false_negative = false_negative
tmp.false_positive = false_positive
tmp.true_negative = true_negative
confusion_matrix(tmp)

# print(gain)
