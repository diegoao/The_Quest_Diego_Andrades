from datetime import datetime

# d = datetime.strptime('xx-xx-xx', '%d-%m-%Y')
fechaActual = str(datetime.now().date())
partes = fechaActual.split("-")
fechaActual = "-".join(reversed(partes))
print(fechaActual)
