from django.conf import settings
from django.db import models
from djangoldp.models import Model
from djangoldp_circle.models import Circle

class Product(Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom du produit")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    externalLink = models.URLField(blank=True, null=True, verbose_name="Lien externe")
    stock = models.IntegerField(blank=True, null=True, verbose_name="Stock initial")
    price = models.IntegerField(blank=True, null=True, verbose_name="Prix")
    creationDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta(Model.Meta):
        anonymous_perms = ['view', 'add']
        rdf_type = 'sib:product'

    def __str__(self):
        return self.name

class Sale(Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom de la vente")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    startDate =  models.DateField(blank=True, null=True, verbose_name="Date de début")
    endDate = models.DateField(verbose_name="Date de fin", blank=True, null=True )
    product = models.ManyToManyField(Product, blank=True, max_length=50, verbose_name="produits", related_name="sale")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='createdSales', null=True, blank=True, on_delete=models.SET_NULL)
    creationDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    circle = models.ForeignKey(Circle, null=True, blank=True, related_name="sale", on_delete=models.SET_NULL)
    
    class Meta(Model.Meta):
        nested_fields = ['circle', 'author']
        ordering = ['startDate']
        auto_author = 'author'
        owner_field = 'author'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        owner_perms = ['inherit', 'change', 'control', 'delete']
        rdf_type = 'sib:sale'

    def __str__(self):
        return self.name