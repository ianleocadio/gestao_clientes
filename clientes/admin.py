from django.contrib import admin
from .models import Person, Documento, Venda, Produto
from .actions import nfe_emitida, nfe_nao_emitida


class PersonAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Dados pessoiais", {"fields": ('first_name', "last_name", "doc")}),
        ("Dados complementares",{
            "classes": ("collapse",),
            "fields": ("age", "salary", "photo")
        })
    )
    list_filter = ("age", "salary")
    list_display = ("completeName", "doc", "age", "salary", "bio", "hasPhoto")
    search_fields = ["id", "first_name"]


    def hasPhoto(self, instance):
        if instance.photo:
            return "Sim"
        else:
            return "Não"
    hasPhoto.short_description = "Possui foto ?"

    def completeName(self, instance):
        return instance.first_name + " " + instance.last_name
    completeName.short_description = "nome"

class VendaAdmin(admin.ModelAdmin):
    readonly_fields = ("valor",)
    raw_id_fields = ("pessoa",)
    autocomplete_fields = ["pessoa", "produtos"]
    list_filter = ("pessoa__doc", "desconto")
    list_display = ("id", "pessoa", "nfe_emitida", "total")
    search_fields = ("id", "pessoa__first_name", "pessoa__doc__num_doc")
    actions = [nfe_emitida, nfe_nao_emitida]
    #filter_horizontal = ["produtos"]

    def total(self, instance):
        return instance.get_total()

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "descricao", "preco")
    search_fields = ("id", "descricao")


admin.site.register(Person, PersonAdmin)
admin.site.register(Documento)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Produto, ProdutoAdmin)

admin.site.site_header = "Gestão de Clientes"
admin.site.index_title = "Administração"
admin.site.site_title = "Seja bem vindo ao Gestão de Clientes"
