from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

perguntas = [

    # ================= ANTIGO TESTAMENTO =================
    {"cat": "Antigo Testamento", "p": "Quem construiu a arca?", "o": ["Moisés", "Noé", "Abraão", "Davi"], "r": "Noé"},
    {"cat": "Antigo Testamento", "p": "Qual o primeiro livro da Bíblia?", "o": ["Êxodo", "Salmos", "Gênesis", "Levítico"], "r": "Gênesis"},
    {"cat": "Antigo Testamento", "p": "Quem foi jogado na cova dos leões?", "o": ["Daniel", "José", "Elias", "Isaías"], "r": "Daniel"},
    {"cat": "Antigo Testamento", "p": "Qual mar Moisés abriu?", "o": ["Morto", "Vermelho", "Caspio", "Galileia"], "r": "Vermelho"},
    {"cat": "Antigo Testamento", "p": "Quem recebeu os 10 Mandamentos?", "o": ["Josué", "Moisés", "Samuel", "Saul"], "r": "Moisés"},
    {"cat": "Antigo Testamento", "p": "Quem derrotou Golias?", "o": ["Salomão", "Sansão", "Davi", "Gideão"], "r": "Davi"},
    {"cat": "Antigo Testamento", "p": "Qual o livro mais longo da Bíblia?", "o": ["Isaías", "Salmos", "Jeremias", "Gênesis"], "r": "Salmos"},
    {"cat": "Antigo Testamento", "p": "Quantas pragas caíram no Egito?", "o": ["7", "12", "10", "3"], "r": "10"},
    {"cat": "Antigo Testamento", "p": "Quem foi vendido pelos irmãos?", "o": ["Benjamim", "José", "Isaque", "Jacó"], "r": "José"},
    {"cat": "Antigo Testamento", "p": "Quem era o homem mais forte da Bíblia?", "o": ["Sansão", "Saul", "Golias", "Davi"], "r": "Sansão"},

    # ================= NOVO TESTAMENTO =================
    {"cat": "Novo Testamento", "p": "Onde Jesus nasceu?", "o": ["Nazaré", "Belém", "Jerusalém", "Emaús"], "r": "Belém"},
    {"cat": "Novo Testamento", "p": "Qual discípulo negou Jesus 3 vezes?", "o": ["Judas", "João", "Pedro", "Tomé"], "r": "Pedro"},
    {"cat": "Novo Testamento", "p": "Qual o último livro da Bíblia?", "o": ["Judas", "Apocalipse", "Atos", "Hebreus"], "r": "Apocalipse"},
    {"cat": "Novo Testamento", "p": "Quem batizou Jesus?", "o": ["Pedro", "João Batista", "André", "Tiago"], "r": "João Batista"},
    {"cat": "Novo Testamento", "p": "Quantos apóstolos Jesus tinha?", "o": ["10", "7", "12", "40"], "r": "12"},
    {"cat": "Novo Testamento", "p": "Quem escreveu a maioria das epístolas?", "o": ["Paulo", "Pedro", "Lucas", "Mateus"], "r": "Paulo"},
    {"cat": "Novo Testamento", "p": "Quem traiu Jesus por 30 moedas?", "o": ["Pedro", "Judas Iscariotes", "Barrabás", "Pilatos"], "r": "Judas Iscariotes"},
    {"cat": "Novo Testamento", "p": "Qual o primeiro milagre de Jesus?", "o": ["Andar na água", "Cura de cego", "Bodas de Caná", "Multiplicação"], "r": "Bodas de Caná"},
    {"cat": "Novo Testamento", "p": "Quem era o cobrador de impostos?", "o": ["Mateus", "Lucas", "Tiago", "João"], "r": "Mateus"},
    {"cat": "Novo Testamento", "p": "Quem subiu em uma árvore para ver Jesus?", "o": ["Lázaro", "Zaqueu", "Bartimeu", "Nicodemos"], "r": "Zaqueu"},

    # ================= SACRAMENTOS =================
    {"cat": "Sacramentos", "p": "Qual o primeiro sacramento?", "o": ["Eucaristia", "Batismo", "Crisma", "Confissão"], "r": "Batismo"},
    {"cat": "Sacramentos", "p": "Qual sacramento perdoa os pecados?", "o": ["Ordem", "Unção", "Penitência", "Batismo"], "r": "Penitência"},
    {"cat": "Sacramentos", "p": "O Matrimônio é um sacramento de quê?", "o": ["Iniciação", "Cura", "Serviço", "Penitência"], "r": "Serviço"},
    {"cat": "Sacramentos", "p": "Qual sacramento confirma o Batismo?", "o": ["Eucaristia", "Crisma", "Ordem", "Missa"], "r": "Crisma"},
    {"cat": "Sacramentos", "p": "Quantos são os sacramentos?", "o": ["3", "5", "7", "10"], "r": "7"},

    # ================= SANTOS =================
    {"cat": "Santos", "p": "Quem é o Santo das causas impossíveis?", "o": ["Sto Expedito", "Sto Antônio", "S. Judas Tadeu", "S. Bento"], "r": "S. Judas Tadeu"},
    {"cat": "Santos", "p": "Quem escreveu a Suma Teológica?", "o": ["S. Agostinho", "Sto Tomás de Aquino", "S. Bento", "S. Francisco"], "r": "Sto Tomás de Aquino"},
    {"cat": "Santos", "p": "Quem fundou a Ordem dos Franciscanos?", "o": ["S. Domingos", "S. Francisco de Assis", "S. Bruno", "S. Bento"], "r": "S. Francisco de Assis"},
    {"cat": "Santos", "p": "Quem é a 'Flor do Carmelo'?", "o": ["Sta Rita", "Sta Teresinha", "Sta Teresa de Ávila", "Sta Clara"], "r": "Sta Teresinha"},
    {"cat": "Santos", "p": "Quem expulsou demônios e fundou mosteiros?", "o": ["S. Bento", "S. Jorge", "S. Patrício", "S. Roque"], "r": "S. Bento"},
    {"cat": "Santos", "p": "Quem é a padroeira do Brasil?", "o": ["Sta Rita", "N. Sra Aparecida", "Sta Dulce", "Sta Luzia"], "r": "N. Sra Aparecida"},
    {"cat": "Santos", "p": "Quem converteu-se após ler as Escrituras?", "o": ["S. Paulo", "S. Agostinho", "S. Francisco", "S. Inácio"], "r": "S. Agostinho"},
    {"cat": "Santos", "p": "Qual santo lutou contra um dragão?", "o": ["S. Miguel", "S. Jorge", "S. Sebastião", "S. Expedito"], "r": "S. Jorge"},
    {"cat": "Santos", "p": "Quem é o Santo casamenteiro?", "o": ["S. José", "Sto Antônio", "S. Valentim", "S. Pedro"], "r": "Sto Antônio"},
    {"cat": "Santos", "p": "Quem é o padroeiro dos animais?", "o": ["S. Roque", "S. Francisco de Assis", "S. Lázaro", "S. João"], "r": "S. Francisco de Assis"},

    # ================= MISSA =================
    {"cat": "Missa", "p": "Qual a primeira parte da Missa?", "o": ["Eucarística", "Ritos Iniciais", "Liturgia da Palavra", "Ofertório"], "r": "Ritos Iniciais"},
    {"cat": "Missa", "p": "Onde fica guardada a Eucaristia?", "o": ["Altar", "Sacrário", "Ambão", "Pia"], "r": "Sacrário"},
    {"cat": "Missa", "p": "Quando o pão vira Corpo de Cristo?", "o": ["Ofertório", "Consagração", "Comunhão", "Pai Nosso"], "r": "Consagração"},
    {"cat": "Missa", "p": "Livro que contém as leituras da Missa?", "o": ["Bíblia", "Missal", "Lecionário", "Catecismo"], "r": "Lecionário"},
    {"cat": "Missa", "p": "O que significa a palavra Eucaristia?", "o": ["Sacrifício", "Ação de Graças", "Comunhão", "Ceia"], "r": "Ação de Graças"},
]

pontos = 0
pergunta_atual_index = 0

@app.route('/')
def index():
    global pontos, pergunta_atual_index
    pontos = 0
    pergunta_atual_index = 0
    return render_template('index.html')

@app.route('/api/proxima_pergunta')
def proxima_pergunta():
    global pergunta_atual_index
    if pergunta_atual_index < len(perguntas):
        p = perguntas[pergunta_atual_index]
        return jsonify({
            "pergunta": p["p"],
            "opcoes": p["o"],
            "cat": p["cat"],
            "index": pergunta_atual_index + 1,
            "total": len(perguntas)
        })
    return jsonify({"finalizado": True, "pontos": pontos})

@app.route('/api/verificar_resposta', methods=['POST'])
def verificar_resposta():
    global pontos, pergunta_atual_index
    data = request.json
    if data.get('resposta') == perguntas[pergunta_atual_index]["r"]:
        pontos += 1
    pergunta_atual_index += 1
    return jsonify({"pontos_atuais": pontos})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)