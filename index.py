import pyodbc
from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form


@app.route('/')
def form():
    return render_template('form.html')

# define a route for the action of the form, for example '/usuario/'


@app.route('/usuario', methods=['POST'])
def usuario():

    # validate the received values
    perid = str(request.form['input_PER_ID'])
    #tipodoc = str(request.form['input_tipo_de_documento'])
    doc = str(request.form['input_numero_de_documento'])

    print("Conectando a la base de datos...")
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    server = '52.247.114.74'
    database = 'DBE_PME'
    username = 'reporte.movilidad'
    password = 'Nw3y0rk_/*4323'

    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                                  server + ';DATABASE='+database+';UID='+username+';PWD=' + password)
        print("Conectado")
    except:
        print("No conectado")

    cursor = conexion.cursor()
    try:
        query=("execute SP_Query_Maestro_Simat @SP_PRO_ID_Type=2, @SP_PRO_Id_Registry_Documento= ? , @SP_PRO_Id_Registry_PER_ID= ? ")

        val=(doc, perid)
        cursor.execute(query, val)

        persona = cursor.fetchone()

        #print(persona)

        tipodoc = str(persona[9])
        localidad = str(persona[1])
        colegio = str(persona[4])
        jornada = str(persona[8])
        consecutivo= str(persona[5])
        options = {"01": "A", "02": "B", "03": "C", "04": "D", "05": "E", "06": "F", "07": "G", "08": "H"}
        sede = (options[str(consecutivo[-2:])])
        primerapellido = str(persona[11])
        segundoapellido = str(persona[12])
        primernombre = str(persona[13])
        segundonombre = str(persona[14])
        fechanacimiento = str(persona[15])
        sexo = str(persona[17])
        curso = str(persona[21])
        discapacidad = str(persona[24])
        etnia = str(persona[25])
        estado_validacion = str(persona[29])
        validacion= str(persona[30])
        fecha_validacion = str(persona[31])



        cursor.close()
        conexion.close()

        return render_template('resultados.html', perid=perid, tipodoc=tipodoc, doc=doc, localidad=localidad, colegio=colegio, jornada=jornada, sede=sede, primerapellido=primerapellido, segundoapellido=segundoapellido, primernombre=primernombre, segundonombre=segundonombre, fechanacimiento=fechanacimiento, sexo=sexo, curso=curso, discapacidad=discapacidad, etnia=etnia, estado_validacion=estado_validacion, validacion=validacion, fecha_validacion=fecha_validacion)
    
    except Exception as err:
        return "<h1>El usuario no existe "+ perid +" " + doc+ "</h1><h3>" + format(err) + "</h3>"

if __name__ == "__main__":
    app.run(debug=True)
