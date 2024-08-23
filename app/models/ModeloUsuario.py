from .entities.Usuario import Usuario
from .entities.TipoUsuario import TipoUsuario


class ModeloUsuario():

    @classmethod
    def login(self, db, usuario):

        try:
            cursor = db.connect.cursor()
            sql = """SELECT id, usuario, password, correo 
                    FROM usuario WHERE usuario = '{0}' AND password = '{1}'""".format(usuario.usuario, usuario.password)
            cursor.execute(sql)
            data = cursor.fetchone()

            if data != None:
                usuario_logeado = Usuario(
                    data[0], data[1], None, None, None, data[3], None, None)
                return usuario_logeado
            else:
                return None
        except Exception as ex:
            raise Exception(ex)







        # try:
        #     cursor = db.connect.cursor()
        #     sql = """SELECT id, usuario, password, correo 
        #             FROM usuario WHERE usuario = '{0}'""".format(usuario.usuario)
        #     cursor.execute(sql)
        #     data = cursor.fetchone()
        #     if data != None:
        #         coincide = Usuario.verificar_password(
        #             data[2], usuario.password)
        #         if coincide:
                    
        #             usuario_logeado = Usuario(
        #                 data[0], data[1], None, None, None, data[3], None, None)
        #             return usuario_logeado
        #         else:
        #             return None
        #     else:
        #         return None
        # except Exception as ex:
        #     raise Exception(ex)

    @classmethod
    def obtener_por_id(self, db, id):
        try:
            cursor = db.connect.cursor()
            sql = """SELECT USU.id, USU.usuario, TIP.id, TIP.nombre
                    FROM usuario USU JOIN tipousuario TIP ON USU.tipousuario_id = TIP.id
                    WHERE USU.id = {0}""".format(id)
            cursor.execute(sql)
            data = cursor.fetchone()
            tipousuario = TipoUsuario(data[2], data[3])
            usuario_logeado = Usuario(
                data[0], data[1], None, None, None, None, None, tipousuario)
            return usuario_logeado
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def obtener_gmail(self, db, id):
        print("Id recibido: ", id)
        try:
            cursor = db.connect.cursor()
            sql = """SELECT correo FROM usuario WHERE id = {0}""".format(id)
            cursor.execute(sql)
            data = cursor.fetchone()
            
            print(data[0])
            # tipousuario = TipoUsuario(data[2], data[3])
            # usuario_logeado = Usuario(
            #     data[0], data[1], None, None, None, None, None, tipousuario)
            return data[0]
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def registrar_usuario(self, db, usuario):
        try:
            hash= Usuario.generar_password(usuario.password)
            
            print(hash)
            cursor = db.connection.cursor()
            sql = """ INSERT INTO usuario (id, usuario, password, nombre, 
                        domicilio, correo, telefono, tipousuario_id) 
                        VALUES (NULL, '{0}', '{1}', '{2}', '{3}', '{4}', {5}, 2);""".format(
                        usuario.usuario, hash, usuario.nombre, usuario.domicilio, 
                        usuario.correo, usuario.telefono, usuario.tipousuario)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
