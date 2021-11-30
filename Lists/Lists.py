from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import csv
import pickle
import string

# Lista de Cidades e Países
world_cities = []
with open('world-cities.csv', encoding='latin-1', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        world_cities.append(row)

# Lista ordenada por nº de palavras
world_cities.sort(key=lambda line: len(line[0].split()), reverse=True)

# Dicionário de Países
cities = dict()

for line in world_cities:
    if line[1] in cities:
        # append the city to respective country
        cities[line[1]].append(line[0])
    else:
        # create a new array in this slot
        cities[line[1]] = [line[0]]

with open('World_Cities.p', 'wb') as fp:
    pickle.dump(cities, fp, protocol=pickle.HIGHEST_PROTOCOL)

# Lista de Países
country_M = ['USA', 'US', 'UK', 'EU']

for line in world_cities:
    land = word_tokenize(line[1])
    for row in land:
        if row not in country_M and len(row) > 3:
            country_M.append(row)

with open("Countries_upper.txt", 'w') as f:
    for row in country_M:
        f.write(str(row) + '\n')

country_m = []

for line in country_M:
    country_m.append(line.lower())

with open("Countries_lower.txt", 'w') as f:
    for row in country_m:
        f.write(str(row) + '\n')


stopW = ['a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act',
         'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against',
         'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst',
         'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway',
         'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as',
         'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became',
         'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning',
         'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond',
         'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', 'cant', 'cause',
         'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains',
         'could', 'couldnt', 'd', 'date', 'did', 'didnt', 'different', 'do', 'does', 'doesnt', 'doing', 'done',
         'dont', 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty',
         'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even',
         'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few',
         'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly',
         'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give',
         'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has',
         'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein',
         'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home',
         'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', 'ill', 'im', 'immediate', 'immediately',
         'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention',
         'inward', 'is', 'isnt', 'it', 'itd', 'itll', 'its', 'itself', 'ive', 'j', 'just', 'k', 'keep', 'keeps',
         'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter',
         'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', 'll',
         'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me',
         'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more',
         'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name',
         'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never',
         'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone',
         'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained',
         'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones',
         'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out',
         'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly',
         'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially',
         'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides',
         'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really',
         'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively',
         'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw',
         'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen',
         'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', 'shell', 'shes', 'should',
         'shouldnt', 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar',
         'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan',
         'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically',
         'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully',
         'such', 'sufficiently', 'suggest', 'sup', 'sure	t', 'take', 'taken', 'taking', 'tell', 'tends', 'th',
         'than', 'thank', 'thanks', 'thanx', 'that', 'thatll', 'thats', 'thatve', 'the', 'their', 'theirs', 'them',
         'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein',
         'therell', 'thereof', 'therere', 'theres', 'thereto', 'thereupon', 'thereve', 'these', 'they', 'theyd',
         'theyll', 'theyre', 'theyve', 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug',
         'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward',
         'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under',
         'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used',
         'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', 've', 'very',
         'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome',
         'well', 'went', 'were', 'werent', 'weve', 'what', 'whatever', 'whatll', 'whats', 'when', 'whence',
         'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever',
         'whether', 'which', 'while', 'whim', 'whither', 'who', 'who', 'whoever', 'whole', 'wholl', 'whom',
         'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont',
         'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', 'youll', 'your',
         'youre', 'yours', 'yourself', 'yourselves', 'youve', 'z', 'zero']

# remove pontuação das palavras
table = str.maketrans('', '', string.punctuation)
stopW = stopW + list(set(stopwords.words('english')))
stopW = [w.translate(table) for w in stopW]

with open("stopW.txt", 'w') as f:
    for row in stopW:
        f.write(str(row) + '\n')
