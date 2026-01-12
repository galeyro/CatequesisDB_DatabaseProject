from django.db import models

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    lugar_nacimiento = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono_alumno = models.CharField(max_length=20, null=True, blank=True)
    info_escolar = models.CharField(max_length=255, null=True, blank=True)
    info_salud = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'Alumno'
        managed = True
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Parroquia(models.Model):
    id_parroquia = models.AutoField(primary_key=True)
    nombre_parroquia = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono_secretaria = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'Parroquia'
        managed = True

    def __str__(self):
        return self.nombre_parroquia

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nombre_perfil = models.CharField(max_length=50)

    class Meta:
        db_table = 'Perfil'
        managed = True
    
    def __str__(self):
        return self.nombre_perfil

class Usuario(models.Model):
    id_user = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, db_column='id_perfil')
    id_parroquia = models.ForeignKey(Parroquia, on_delete=models.CASCADE, db_column='id_parroquia')
    # id_catequista es nullable y circular, lo definimos como Integer o FK diferida? FK differida es mejor.
    # Pero Catequista depende de Usuario. Dejémoslo nullable.
    id_catequista = models.IntegerField(null=True, blank=True) 
    username = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=255)
    esta_activo = models.BooleanField()

    class Meta:
        db_table = 'Usuario'
        managed = True

    def __str__(self):
        return self.username

class Catequista(models.Model):
    id_catequista = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    es_joven_apoyo = models.BooleanField()
    usuario_id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Usuario_id_user')

    class Meta:
        db_table = 'Catequista'
        managed = True

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Documento(models.Model):
    id_doc = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    id_usuario_carga = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario_carga')
    fecha_carga = models.DateField()
    referencia_storage = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Documento'
        managed = True

class Sacramento(models.Model):
    id_sacramento = models.AutoField(primary_key=True)
    # id_nivel_requisito es FK a Nivel, pero Nivel depende de Sacramento? Circular.
    id_nivel_requisito = models.IntegerField(null=True, blank=True) 
    nombre_sacramento = models.CharField(max_length=100)

    class Meta:
        db_table = 'Sacramento'
        managed = True

    def __str__(self):
        return self.nombre_sacramento

class Nivel(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nombre_nivel = models.CharField(max_length=100)
    orden = models.IntegerField()
    sacramento_id_sacramento = models.ForeignKey(Sacramento, on_delete=models.CASCADE, db_column='Sacramento_id_sacramento')

    class Meta:
        db_table = 'Nivel'
        managed = True
    
    def __str__(self):
        return self.nombre_nivel

class Periodo(models.Model):
    id_periodo = models.AutoField(primary_key=True)
    nombre_periodo = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'Periodo'
        managed = True
    
    def __str__(self):
        return self.nombre_periodo

class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    id_parroquia = models.ForeignKey(Parroquia, on_delete=models.CASCADE, db_column='id_parroquia')
    id_nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, db_column='id_nivel')
    id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, db_column='id_periodo')

    class Meta:
        db_table = 'Grupo'
        managed = True

class GrupoCatequista(models.Model):
    grupo_id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='Grupo_id_grupo')
    catequista_id_catequista = models.ForeignKey(Catequista, on_delete=models.CASCADE, db_column='Catequista_id_catequista')

    class Meta:
        db_table = 'Grupo-Catequista'
        managed = True
        unique_together = (('grupo_id_grupo', 'catequista_id_catequista'),)

class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='id_grupo')
    fecha_inscripcion = models.DateField()
    estado_inscripcion = models.CharField(max_length=50)
    estado_aprobacion = models.CharField(max_length=50)
    comentarios_excepcion = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'Inscripcion'
        managed = True

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    inscripcion_id_inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, db_column='Inscripcion_id_inscripcion')
    fecha_sesion = models.DateField()
    estado = models.CharField(max_length=20)

    class Meta:
        db_table = 'Asistencia'
        managed = True

class Padrino(models.Model):
    id_padrino = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'Padrino'
        managed = True
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class InscripcionPadrino(models.Model):
    padrino_id_padrino = models.ForeignKey(Padrino, on_delete=models.CASCADE, db_column='Padrino_id_padrino')
    inscripcion_id_inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, db_column='Inscripcion_id_inscripcion')

    class Meta:
        db_table = 'Inscripcion-Padrino'
        managed = True
        unique_together = (('padrino_id_padrino', 'inscripcion_id_inscripcion'),)

class Representante(models.Model):
    id_representante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100, null=True, blank=True)
    ocupacion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'Representante'
        managed = True

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class RepresentanteAlumno(models.Model):
    representante_id_representante = models.ForeignKey(
        Representante, 
        on_delete=models.CASCADE, 
        db_column='Representante_id_representante',
        primary_key=True
    )
    alumno_id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='Alumno_id_alumno')

    class Meta:
        db_table = 'Representante-Alumno'
        managed = True
        unique_together = (('representante_id_representante', 'alumno_id_alumno'),)

class SacramentoRealizado(models.Model):
    id_alumno_sacramento = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    id_sacramento = models.ForeignKey(Sacramento, on_delete=models.CASCADE, db_column='id_sacramento')
    id_inscripcion_prep = models.ForeignKey(Inscripcion, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_inscripcion_prep')
    fecha_realizacion = models.DateField()
    comentarios = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'Sacramento_realizado'
        managed = True
