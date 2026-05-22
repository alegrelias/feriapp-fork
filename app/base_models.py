from django.db import models

#ValidableModel herda de models.Model, cualquier clase que herede de esta es un modelo válido de Django
class ValidableModel(models.Model):
    #Meta define metadatos del modelo, en este caso define que es una clase abstracta, por lo tanto Django no va a crear una tabla de ella
    class Meta:
        abstract = True

    #convierte el metodo en uno de clase, por ej llamandolo con Ferias.validate()...
    @classmethod
    #cls es clase, kwargs son keyword arguments 
    def validate(cls, **kwargs) -> list[str]:
        """
        Debe ser sobrescrito en el modelo de negocio.
        Recibe los atributos y retorna una lista de strings con errores.
        """
        errors = []
        return errors

    @classmethod
    def new(cls, **kwargs):
        """
        Sigue la estructura exacta del ejemplo: valida y si no hay errores, crea.
        """
        #primero valida que los argumentos pasados en la creacion sean correctos
        errors = cls.validate(**kwargs)
        if errors:
            return None, errors

        # si son correctos se crea el objeto en la RAM para devolverlo en el return y se lo persiste en la base de datos simultaneamente
        instance = cls.objects.create(**kwargs)
        return instance, []

    #self porque es un metodo de instancia, el objeto ya existe
    def update(self, **kwargs) -> list[str]:
        """
        Sigue la estructura exacta del ejemplo: valida los nuevos datos 
        y si pasa, altera los atributos de la instancia y guarda.
        """
        #como validate es un metodo de clase hay que llamarlo con el atributo __class__
        errors = self.__class__.validate(**kwargs)
        if errors:
            return errors


        # Setea dinámicamente los campos nuevos pasados por la vista
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self.save()
        return []