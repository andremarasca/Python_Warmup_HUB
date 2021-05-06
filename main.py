# Definir função para leitura e estruturamento do dataset

def f_carregar_dataset(filename, header_sep, sep, header):

    # Carregar arquivo do dataset

    f = open(filename, "r", encoding='latin-1')
    dataset = f.read().split("\n")

    # Remover ultima linha (linha vazia)

    dataset.pop()

    # Construir dicionário com nomes das colunas

    dataset_header = header.split(header_sep)

    dict_dataset = {}

    for name in dataset_header:
        dict_dataset[name] = []

    # Popular dicionario

    for instancia in dataset:
        for idx, col in enumerate(instancia.split(sep)):
            dict_dataset[dataset_header[idx]].append(col)

    return dict_dataset


# Definindo acumulador

def accumulator(dict_rating, key, rating):
    if key not in dict_rating["sum"]:
        dict_rating["sum"][key] = 0
        dict_rating["quant"][key] = 0

    dict_rating["sum"][key] += float(rating)
    dict_rating["quant"][key] += 1

# Definir uma função que recebe um dict de soma e calcula a media


def mean_calculator(dict_rating):
    # Calcular a media
    for key in dict_rating["sum"]:
        dict_rating["mean"][key] = dict_rating["sum"][key] / \
            dict_rating["quant"][key]


# definir uma função para ordenar o rating


def f_sort_rating_tuple(dict_rating):
    # Ordenar o rating e devolver uma tupla ordenada em ordem crescente
    list_id = []
    list_rating = []

    for id in dict_rating["mean"]:
        list_id.append(id)
        list_rating.append(dict_rating["mean"][id])

    tuple_sorted_rating = sorted(zip(list_rating, list_id))

    return tuple_sorted_rating

# %% Exercício 1: Usuarios com médias abaixo da média global


data_header = "id|item_id|rating|timestamp"

dict_data = f_carregar_dataset(
    "../ml-100k/u.data", header_sep="|", sep="\t", header=data_header)

# transformar atributo rating de string para int

dict_data["rating"] = list(map(int, dict_data["rating"]))

# Obter rating medio global

n_instancias = len(dict_data["rating"])
rating_sum = sum(dict_data["rating"])
rating_mean = rating_sum / n_instancias

# definir uma função para calcular o rating recebendo o nome da coluna


def f_rating_estimator(atrib_name="id"):
    # Obter media de rating para cada ID da coluna recebida

    dict_rating = {"sum": {}, "quant": {}, "mean": {}}

    # Calcular soma e quantidade
    for i in range(n_instancias):
        atrib_id = dict_data[atrib_name][i]
        rating = dict_data["rating"][i]

        accumulator(dict_rating, atrib_id, rating)

    mean_calculator(dict_rating)

    return dict_rating

# Obter rating para cada user


dict_rating_user = f_rating_estimator("id")

# Ordenar o par (rating, user)

tuple_sorted_rating_user = f_sort_rating_tuple(dict_rating_user)

# Imprimir top 5 piores
for user in tuple_sorted_rating_user[0:5]:
    if user[0] < rating_mean:
        print(f"user {user[1]} rating {'%.3f' % user[0]}")

# %% Resposta dos exercícios 2 e 3: Mostrar filmes com menores rating e maiores rating

dict_rating_movie = f_rating_estimator("item_id")

tuple_sorted_rating_movie = f_sort_rating_tuple(dict_rating_movie)

# Top 5 piores
for user in tuple_sorted_rating_movie[0:5]:
    print(f"Movie {user[1]} rating {'%.3f' % user[0]}")

# Top 5 melhores
for user in tuple_sorted_rating_movie[-5:]:
    print(f"Movie {user[1]} rating {'%.3f' % user[0]}")

# %% Exercício 4 - Media de avaliação para cada genero

genres = "Action|Adventure|Animation|Children's|Comedy|Crime|Documentary|Drama|Fantasy|Film-Noir|Horror|Musical|Mystery|Romance|Sci-Fi|Thriller|War|Western"
genres = genres.split("|")

# Construir dicionário com nomes das colunas

item_info_header = "movie_id|movie_title|release_date|video_release_date|IMDb_URL|unknown|Action|Adventure|Animation|Children's|Comedy|Crime|Documentary|Drama|Fantasy|Film-Noir|Horror|Musical|Mystery|Romance|Sci-Fi|Thriller|War|Western"

dict_item_info = f_carregar_dataset(
    "../ml-100k/u.item", header_sep="|", sep="|", header=item_info_header)


def f_rating_estimator_genre():

    # Inicializar os dicionários de contagem

    dict_rating = {"sum": {}, "quant": {}, "mean": {}}

    # Iterar informações sobre filmes calculando o rating medio de cada genero

    for idx in range(len(dict_item_info["movie_id"])):
        movie_id = dict_item_info["movie_id"][idx]
        movie_rating = dict_rating_movie["mean"][movie_id]

        for genre in genres:
            if dict_item_info[genre][idx] == '1':
                accumulator(dict_rating, genre, movie_rating)

    mean_calculator(dict_rating)

    return dict_rating

# Calcular o rating para cada genero


dict_rating_genre = f_rating_estimator_genre()

# Ordenar o par (rating, genero)

tuple_sorted_rating_genre = f_sort_rating_tuple(dict_rating_genre)

# Imprimir o rate medio de cada genero

for genre in tuple_sorted_rating_genre:
    print(f"Genre {genre[1]} rating {'%.3f' % genre[0]}")


# %% Exercicio 5 - rating por ano

def f_rating_estimator_year():

    # Inicializar os dicionários de contagem

    dict_rating = {"sum": {}, "quant": {}, "mean": {}}

    # Iterar informações sobre filmes calculando o rating medio de cada genero

    for idx in range(len(dict_item_info["movie_id"])):
        movie_id = dict_item_info["movie_id"][idx]
        movie_rating = dict_rating_movie["mean"][movie_id]
        year = dict_item_info["release_date"][idx].split("-")[-1]

        accumulator(dict_rating, year, movie_rating)

    mean_calculator(dict_rating)

    return dict_rating

# Calcular o rating para cada ano


dict_rating_year = f_rating_estimator_year()

# Ordenar o par (rating, ano)

tuple_sorted_rating_year = f_sort_rating_tuple(dict_rating_year)


# Imprimir o rate medio de cada ano

for year in tuple_sorted_rating_year:
    if year[1] != "":
        print(f"Year {year[1]} rating {'%.3f' % year[0]}")

# Imprimir o ano que teve o melhor rating

max_year = tuple_sorted_rating_year[-1]
print(f"Max year {max_year[1]} rating {'%.3f' % max_year[0]}")

# %% Exercicio 6 -
# Encontrar a média de avaliação para cada ocupação de usuário e mostrar os menores e maiores valores

user_info_header = "user_id|age|gender|occupation|zip_code"

dict_user_info = f_carregar_dataset(
    "../ml-100k/u.user", header_sep="|", sep="|", header=user_info_header)


def f_rating_estimator_ocupation():
    # Inicializar os dicionários de contagem

    dict_rating = {"sum": {}, "quant": {}, "mean": {}}

    # Iterar informações sobre usuarios calculando o rating medio de cada profissao

    for idx in range(len(dict_user_info["user_id"])):
        user_id = dict_user_info["user_id"][idx]
        user_rating = dict_rating_user["mean"][user_id]
        user_occupation = dict_user_info["occupation"][idx]

        accumulator(dict_rating, user_occupation, user_rating)

    mean_calculator(dict_rating)

    return dict_rating

# Calcular o rating para cada occupation


dict_rating_year = f_rating_estimator_ocupation()

# Ordenar o par (rating, occupation)

tuple_sorted_rating_occupation = f_sort_rating_tuple(dict_rating_year)

# Imprimir o rate medio de cada occupation

for occupation in tuple_sorted_rating_occupation:
    print(f"Occupation {occupation[1]} rating {'%.3f' % occupation[0]}")
