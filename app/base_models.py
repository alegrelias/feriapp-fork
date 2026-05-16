from django.db import models

class ValidableModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
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
        errors = cls.validate(**kwargs)
        if errors:
            return None, errors

        # Crea y persiste usando los argumentos desempaquetados
        instance = cls.objects.create(**kwargs)
        return instance, []

    def update(self, **kwargs) -> list[str]:
        """
        Sigue la estructura exacta del ejemplo: valida los nuevos datos 
        y si pasa, altera los atributos de la instancia y guarda.
        """
        errors = self.__class__.validate(**kwargs)
        if errors:
            return errors

        # Setea dinámicamente los campos nuevos pasados por la vista
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self.save()
        return []