from flask import Flask, jsonify ,redirect, url_for, render_template, request
from db.connect import GetConn
from mysql.connector import errorcode
app = Flask(__name__)

@app.route("/", methods = ['GET'])
def home():
    return render_template("index.html")

@app.route("/encuesta", methods = ['GET'])
def encuesta():
    return render_template("encuesta.html")

@app.route("/registro", methods = ['GET'])
def registro():
    return render_template("registro.html")

@app.route("/color", methods = ['GET'])
def color():
    return render_template("color.html")

@app.route("/depresion", methods = ['GET'])
def depresion():
    return render_template("Depresion.html")

@app.route("/<name>", methods = ['GET'])
def user(name):
    return f"Hello {name}"

@app.route("/admin", methods = ['GET'])
def admin():
    return redirect(url_for("user", name="Admin!!"))

@app.route("/registration", methods = ['POST'])
def registration():
    try:
       
        cursor , connection = GetConn()
        insert = ""
        values = ""

        if 'email' in request.json:
            query =  f'SELECT * FROM `mydb`.`people` WHERE  `email` = "{request.json["email"]}";'
            print(query);
            cursor.execute(query)
            for (idpeople , nombre ,edad ,colorFav,genero ,email, pronombre) in cursor:
                cursor.close()
                connection.close()
                return jsonify({
                    "people": {
                        "idpeople": idpeople  ,
                        "nombre": nombre  ,
                        "edad": edad  ,
                        "colorFav": colorFav ,
                        "genero": genero  ,
                        "email": email ,
                        "pronombre": pronombre 
                    },
                    "msg": "Currently the mail is already registered",
                    "msg_es": f"Actualmente ya se registro el correo"
                    }), 200

        if 'nombre' in request.json: 
            insert += "`nombre`, "
            values += f'"{request.json["nombre"]}", '
        else:
            insert += "`nombre`, "
            values += '"anonimo", '

        if 'edad' in request.json:
            insert += "`edad`, "
            values += f'"{request.json["edad"]}", ' 
       
        if 'colorFav' in request.json:
            insert += "`colorFav`, "
            values += f'"{request.json["colorFav"]}", ' 
    
        if 'genero' in request.json:
            insert += "`genero`, "
            values += f'"{request.json["genero"]}", ' 
       
        if 'email' in request.json:
            insert += "`email`, "
            values += f'"{request.json["email"]}", ' 
      
        if 'pronombre' in request.json:
            insert += "`pronombre`"
            values += f'"{request.json["pronombre"]}"' 
        else:
            insert += "`pronombre`"
            values += '" "'
        query =  f'INSERT INTO `mydb`.`people` ({insert}) values ({values}) ;'
        print(query);
        cursor.execute(query)
        info = cursor.lastrowid
        print(info);
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({
                "idpeople": info,
                "msg": "save your registration",
                "msg_es": f"se a guardado su registro"
                }), 201
    except Exception as e:
        print(e)
        return jsonify({
                "msg": "something  failed",
                "msg_es": f"algo fallo",
                "error": e
                }), 500

@app.route("/start-questionnaire", methods = ['POST'])
def start_questionnaire():
    try:

        if not 'idpeople' in request.json:
            return jsonify({
                    "msg": "'idpeople' is nesesary",
                    "msg_es": f"'idpeople' es necesario"
                    }), 401

        idpeople        = request.json['idpeople']
        idquestionnaire =  request.json['idquestionnaire'] if 'idquestionnaire' in request.json else 1
        cursor , connection = GetConn()
        query =  f'INSERT INTO `mydb`.`result` (`idpeople`, `idquestionnaire`, `testResultado`) values ({idpeople} , {idquestionnaire} , "incompleto") ;'
        print(query);
        cursor.execute(query)
        info = cursor.lastrowid
        print(info);
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
                    "idresultado": info,
                    "msg": "Save your start",
                    "msg_es": f"Se a guardado tu inicio"
                    }), 201
    except Exception as e:
        print(e)
        return jsonify({
                "msg": "something  failed",
                "msg_es": f"algo fallo",
                "error": e
                }), 500

@app.route("/end-questionnaire", methods = ['POST'])
def end_questionnaire():
    try:

        if not 'idpeople' in request.json:
            return jsonify({
                    "msg": "'idpeople' is nesesary",
                    "msg_es": f"'idpeople' es necesario"
                    }), 401

        if not 'responses' in request.json:
            return jsonify({
                    "msg": "'responses' is nesesary",
                    "msg_es": f"'responses' es necesario"
                    }), 401

        # if isinstance(request.json['responses'], list) :
        #     return jsonify({
        #             "msg": "'responses' is not a list",
        #             "msg_es": f"'responses' no es una lista"
        #             }), 401

        idpeople        = request.json['idpeople']
        idquestionnaire =  request.json['idquestionnaire'] if 'idquestionnaire' in request.json else 1
        cursor , connection = GetConn()
        if not 'idresultado'  in request.json :
            query =  f'INSERT INTO `mydb`.`result` (`idpeople`, `idquestionnaire`, `testResultado`) values ({idpeople} , {idquestionnaire} , "incompleto") ;'
            print(query);
            cursor.execute(query)
            idresultado = info = cursor.lastrowid
        else:
            idresultado =  request.json['idresultado']

        index = 1
        for response in request.json['responses']:
            query =  f'INSERT INTO `mydb`.`response` (`idpeople`, `idquestionnaire`, `idresultado`, `idrespuesta`, `respuesta`) values ({idpeople} , {idquestionnaire} , {idresultado} , {index}, "{response}") ;'
            print(query);
            cursor.execute(query)
            index += 1

        query =  f'UPDATE `mydb`.`result` SET `testResultado` = "completo" WHERE (`idresultado` = {idresultado}) and (`idpeople` = {idpeople}) and (`idquestionnaire` = {idquestionnaire});'
        print(query);
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
                    "msg": "Save your response",
                    "msg_es": f"Se a guardado tu respuesta"
                    }), 201
    except Exception as e:
        print(e)
        return jsonify({
                "msg": "something  failed",
                "msg_es": f"algo fallo",
                "error": e
                }), 500

if __name__ == "__main__":
    app.run(debug = False, host="0.0.0.0", port = 5000)
 