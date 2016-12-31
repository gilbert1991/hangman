# from GameClient import GameClient
from NewGameClient import GameClient
from hangman import AI
from hangman import HangMan

def test_game(test_file_name, times_guess):

    # Init game client and solution
    hangman = HangMan("/Users/Gilbert/Documents/hangman/w2_.txt")

    client = GameClient()

    test_sentences = load_test_sentences(test_file_name)
    win_count = 0
    total_count = len(test_sentences)

    for i in range(0, total_count):

        print '/----------------------------------------'
        init_sent = ""
        for c in test_sentences[i]:
            init_sent += " " if not c.isalpha() else "_"

        hangman.init_hm(init_sent, times_guess)

        result = play_game(client, hangman, test_sentences[i], times_guess)

        if result == 'WIN':
            win_count += 1
        print '\________________________________________'

    print "Accuracy:\twin:{0}\ttotal:{1}\tpercentage:{2:.4f}%".format(win_count, total_count, 1.0 * win_count / total_count * 100)

def play_game(client, hm, full_string, total_number):
    result = client.create_game(full_string, total_number)
    if result['status'] == 'ERROR':
        print "Init error"

    # Game running
    while result['status'] == 'ONGOING':
        # print '/---'
        letter = hm.guess()

        result = client.guess(letter)

        hm.update_hm(result['str'],result['remain']) # TODO edge case
        # print result
        # print result['str']
        # print result['remain'], "trials left"
        # print '\___'

    if result['status'] == 'LOSE':
        print result
    # # Game terminated
    # if result['status'] == "WIN":
    #     print result['status'], result['cost']
    # else:
    #     print result['status']
    return result['status']

def load_test_sentences(fileName):
    f = open(fileName, 'r')
    test_sentences = []
    for line in f:
        test_sentences.append(line.lower())
    return test_sentences

if __name__ == "__main__":
    # full_string = raw_input("Input string:\n")
    # total_number = raw_input("Total trial number:\n")
    # full_string = "have a good day"
    # total_number = 10
    test_game('/Users/Gilbert/Documents/hangman/test.txt', 5)
    print "Test Terminated"
