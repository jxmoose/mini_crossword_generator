from flask import Flask, render_template, request
from .crossword import crossword_gen
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', name='index', message = '')

@app.route("/crossword", methods=['POST'])
def crossword():
    word = request.form['word']
    if (len(word) != 5):
        return render_template('index.html', name='index', message = "WRONG LENGTH")
    c = crossword_gen(word)
    c.add_across()
    c.add_down()
    c.add_across()
    c.add_down()
    c.add_across()
    c.add_down()
    c.generate_clues()
    print(c.across_clues)
    print(c.down_clues)
    a = c.across_clues
    d = c.down_clues
    aw = c.across
    dw = c.down
    return render_template('index.html', name='index', \
        a0= "1. " + a[0], a1= "6. " + a[1], a2= "7. " + a[2], a3= "8. " + a[3] , \
        d0= "1. " + d[0], d1= "2. " + d[1], d2= "3. " + d[2], d3= "4. " + d[3] , \
        l1=aw[0][0], l2=aw[0][1], l3=aw[0][2],l4=aw[0][3],l5=aw[0][4], \
        l6=aw[1][0], l7=aw[1][1], l8=aw[1][2], l9=aw[1][3], l10=aw[1][4], \
        l11=aw[2][0], l12=aw[2][1], l13=aw[2][2], l14=aw[2][3], l15=aw[2][4], \
        l16=aw[3][0], l17=aw[3][1], l18=aw[3][2], l19=aw[3][3], l20=aw[3][4], \
        l21=dw[0][4], l22=dw[1][4], l23=dw[2][4], l24=dw[3][4], \
        word1 = "Across:", word2 = "Down:", n1="1", n2="2", n3="3", n4="4", n5="5", n6="6", n7="7", n8="8", n9="9"
    )
        
