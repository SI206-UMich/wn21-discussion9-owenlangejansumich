from bs4 import BeautifulSoup
import re
import requests
import unittest

# Task 1: Get the URL that links to the Pokemon Charmander's webpage.
# HINT: You will have to add https://pokemondb.net to the URL retrieved using BeautifulSoup
def getCharmanderLink(soup):
    # Find generation 1 Pokemon div tag
    gen1 = soup.find(id = "gen-1").next_sibling.next_sibling
    # Find the div tag with charmander
    div_charmander = gen1.find_all('div', class_ = "infocard")[3]
    # Find the span tag where the link is located
    text_charmander = div_charmander.find('span', class_ = "infocard-lg-data text-muted")
    # Find the link for charmander
    link = text_charmander.find('a', class_ = "ent-name").get('href')

    return "https://pokemondb.net" + link

# Task 2: Get the details from the box below "Egg moves". Get all the move names and store
#         them into a list. The function should return that list of moves.
def getEggMoves(pokemon):
    url = 'https://pokemondb.net/pokedex/'+pokemon
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    parent_id = soup.find(id = "tab-moves-18")

    div_egg_moves = [i for i in parent_id.find_all('h3') if i.text == "Egg moves"][0].next_sibling.next_sibling.next_sibling.next_sibling

    return [i.find('td').text for i in div_egg_moves.find('tbody').find_all('tr')]


# Task 3: Create a regex expression that will find all the times that have these formats: @2pm @5 pm @10am
# Return a list of these times without the '@' symbol. E.g. ['2pm', '5 pm', '10am']
def findLetters(sentences):
    # initialize an empty list
    l = []

    # define the regular expression
    reg_exp = "@(1?\d(?: pm|pm|am))"

    # loop through each sentence or phrase in sentences
    for sentence in sentences:
        # find all the words that match the regular expression in each sentence
        words = re.findall(reg_exp, sentence)

        # loop through the found words and add the words to your empty list
        for word in words:
            l.append(word)


    #return the list of the last letter of all words that begin or end with a capital letter
    return l



def main():
    url = 'https://pokemondb.net/pokedex/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    getCharmanderLink(soup)
    getEggMoves('scizor')

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://pokemondb.net/pokedex/national').text, 'html.parser')

    def test_link_Charmander(self):
        self.assertEqual(getCharmanderLink(self.soup), 'https://pokemondb.net/pokedex/charmander')

    def test_egg_moves(self):
        self.assertEqual(getEggMoves('scizor'), ['Counter', 'Defog', 'Feint', 'Night Slash', 'Quick Guard'])

    def test_findLetters(self):
        self.assertEqual(findLetters(['Come eat lunch at 12','there"s a party @2pm', 'practice @7am','nothing']), ['2pm', '7am'])
        self.assertEqual(findLetters(['There is show @12pm if you want to join','I will be there @ 2pm', 'come at @3 pm will be better']), ['12pm', '3 pm'])

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)