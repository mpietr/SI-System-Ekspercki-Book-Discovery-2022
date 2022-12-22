import clips
import PySimpleGUI as sg

sg.theme('TealMono')

DEBUG = False

MAX = 4
WIDTH = 600
HEIGHT = 300

env = clips.Environment()

env.load('books.clp')
env.reset()
env.run()

msg_template = env.find_template('message')

message = dict(list(msg_template.facts())[0])

if DEBUG:
    print(message)

BUTTON_KEYS = ['button0', 'button1', 'button2', 'button3', 'button4']
TEXT_KEYS = ['text0', 'text1', 'text2', 'text3', 'text4']

options = message['answers']
s = len(options)

radio_buttons = [[sg.Radio('', 1, key=BUTTON_KEYS[i], visible=(i < 3), default=(i == -1)),
                  sg.Text(options[i] if i < 3 else '', pad=(0, 0), font='Any 11', key=TEXT_KEYS[i])] for i in
                 range(MAX)]

layout = [
    [sg.Text(message['question'], font=('Helvetica', 18), key='q')],
    radio_buttons,
    [sg.Button('Submit')]
]

window = sg.Window("2022 Book Discovery", layout, size=(WIDTH, HEIGHT))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Submit':
        if len([x for x, y in values.items() if y is True]) > 0:
            value = [x for x, y in values.items() if y is True][0]
            env.assert_string('({} "{}")'.format(message['name'], message['answers'][BUTTON_KEYS.index(value)]))
            env.run()

            message_list = list(msg_template.facts())

            if message_list:
                message = dict(message_list[0])
                if DEBUG:
                    print(message)
                window['q'].update(value=message['question'])

                options = message['answers']
                n = len(options)

                for i in range(MAX):
                    window[BUTTON_KEYS[i]].update(value=False)
                    if DEBUG:
                        print(n, i)
                    if i < n:
                        window[BUTTON_KEYS[i]].update(visible=True)
                        window[TEXT_KEYS[i]].update(value=options[i], visible=True)
                        if DEBUG:
                            print(TEXT_KEYS[i], options[i])
                            print("visible")
                    else:
                        window[TEXT_KEYS[i]].update(visible=False)
                        window[BUTTON_KEYS[i]].update(visible=False)
                        if DEBUG:
                            print("invisible")
            else:
                window.close()
                break

env.run()
res_template = env.find_template('book')

try:
    result = dict(list(res_template.facts())[0])
except IndexError:
    exit()

result_layout = [
    [sg.Text(result['title'], font='Any 20', pad=(10, 10))],
    [sg.Text(result['author'], font='Any 15')],
    [sg.Button("Close", size=(10, 2), pad=(30, 30))]
]

result_window = sg.Window("Discovered book", result_layout, size=(WIDTH, 200), element_justification='c')

while True:
    event, values = result_window.read()
    if event == sg.WINDOW_CLOSED or event == "Close":
        break