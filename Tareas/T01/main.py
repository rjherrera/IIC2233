import loader

print(loader.usuarios['msmith2'].tope_evaluaciones(loader.cursos['FIS15233']))
print(loader.usuarios['msmith2'].tomar_curso(loader.cursos['FIS15233']))
print(loader.usuarios['vmarianov'].dar_permiso(loader.usuarios['msmith2'], loader.cursos['IEE29131']))
# print(loader.cursos['IEE2913'].requisitos)
print(loader.usuarios['msmith2'].tomar_curso(loader.cursos['IEE29131']))
print(loader.usuarios['msmith2'].cursos_aprobados)
print(loader.usuarios['msmith2'].cursos_por_tomar)