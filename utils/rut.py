import re

def validar_rut_chileno(rut: str) -> bool:
    """
    Valida el RUT chileno (con o sin guion, con o sin puntos).
    Devuelve True si es válido, False si no.
    """
    if not rut:
        return False
    rut = rut.upper().replace("-", "").replace(".", "")
    if not re.match(r"^\d{7,8}[0-9K]$", rut):
        return False
    cuerpo = rut[:-1]
    dv = rut[-1]
    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2
    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    return dv == dv_calculado
