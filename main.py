from flask import Flask, render_template, request 
import io
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def picture_upload():
    try:
        text = request.files['file']
        client = vision.ImageAnnotatorClient()

        response = client.text_detection(image=text)
        texts = response.text_annotations
        print('Texts:')
        for text in texts:
            try:
                print('\n"{}"'.format(text.description))

                vertices = (['({},{})'.format(vertex.x, vertex.y)
                            for vertex in text.bounding_poly.vertices])

                print('bounds: {}'.format(','.join(vertices)))
            except:
                pass
        equ = texts[0].description.strip()
        equa = "".join(equ.split())
        print("".join(equ.split()))
        a = postfix(equa)
        b = modified_postfix(a[0], a[1])
        c = eq_eval(b, a[1])
        print(c)
        return render_template('result.html', answer = c)
    except:
        equation = request.form['eq']
        a = postfix(equation)
        b = modified_postfix(a[0], a[1])
        c = eq_eval(b, a[1])
        #print(text)
        return render_template('result.html', answer = c)

def postfix(eq):
                        
    'Initializing variables'
    stack = []
    numList = []
    digitArr = []
    digitCount = 0
    wasNum = False

    'N signifies the bottom of the stack. This can never be removed.'
    stack.append('N')

    'This function determines which operation has priority'
    def rank(c):
        if c == '^':
            return 3
        if c == '*' or c == '/':
            return 2
        if c == '+' or c == '-':
            return 1
        else:
            return -1

    for i in range(0,len(eq)):

        if eq[i] == '(':
            stack.append(eq[i])
        elif eq[i].isdigit() or eq[i] == '.':
            if wasNum == True:
                digitCount = digitCount + 1
            else:
                digitCount = 1
                wasNum = True
            numList.append(eq[i])
        elif eq[i] == ")":
            while stack[-1] != 'N' and stack[-1] != '(':
                numList.append(stack[-1])
                stack.pop()
            if stack[-1] == '(':
                stack.pop()
        else:
            wasNum = False
            digitArr.append(digitCount)
            digitCount = 0
            while stack[-1] != 'N' and (rank(eq[i]) <= rank(stack[-1])):
                numList.append(stack[-1])
                stack.pop()
            stack.append(eq[i])
    digitArr.append(digitCount)
    while stack[-1] != 'N':
        numList.append(stack[-1])
        stack.pop()

    a = [numList, digitArr]
    return a


def modified_postfix(post, digit):
    modified = []
    i = 0
    while i <= len(digit) and post != []:
        if post[0].isdigit():
            modified.append(post[0:digit[i]])
            post = post[digit[i]:]
        else:
            modified.append(post[0])
            post = post[1:]
            i=i-1
        i = i + 1
    return modified

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def eq_eval(mod, digit):
    new_post = []
    for i in range(0,len(mod)):
        new_post.append(''.join(mod[i]))
    i = 0
    while len(new_post) != 1:
        if isNum(new_post[i]) or new_post[i].isdigit():
            i=i+1
        else:
            pop1 = float(new_post[i-2])
            pop2 = float(new_post[i-1])
            op = new_post[i]
            if op == '^':
                res = pop1 ** pop2
            elif op == '*':
                res = pop1 * pop2
            elif op == '/':
                res = pop1 / pop2
            elif op == '+':
                res = pop1 + pop2
            elif op == '-':
                res = pop1 - pop2
            else:
                print("Error in operation determination")
            'WHY THIS NO WORK'
            new_post[i-2] = str(res)
            new_post.pop(i)
            new_post.pop(i-1)
            i = 0  
    return new_post

if __name__ == '__main__':
    app.run(host = "0.0.0.0")


