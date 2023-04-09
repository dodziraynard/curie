import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from dashboard.models import Student

from .models import Invoice, InvoiceItem


class InvoiceType(DjangoObjectType):

    class Meta:
        model = Invoice
        fields = "__all__"


class InvoiceItemType(DjangoObjectType):

    class Meta:
        model = InvoiceItem
        fields = "__all__"


class Query(graphene.ObjectType):
    all_invoices = graphene.List(InvoiceType)
    all_invoice_items = graphene.Field(InvoiceItemType)

    def resolve_all_invoices(root, info):
        return Invoice.objects.all()


class InvoiceCreationMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        description = graphene.String(required=True)
        note = graphene.String(required=True)
        status = graphene.String(required=True)
        student_id = graphene.String(required=True)
        due_date = graphene.Date()

    # This exposes the created `invoice` in the response to the mutation
    invoice = graphene.Field(InvoiceType)

    @classmethod
    def mutate(cls, root, info, description, note, status, student_id,
               due_date):
        request = info.context
        # We first make sure that the Id is valid
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            raise Exception('Invalid student Id')

        try:
            invoice = Invoice.objects.create(note=note,
                                            description=description,
                                            status=status,
                                            due_date=due_date,
                                            created_by=request.user,
                                            updated_by=request.user,
                                            student=student)
            print("invoice", invoice)
        except Exception as e:
            print("e", str(e))

        # Notice we return an instance of `Note` because the mutation expose
        # a `NoteType` in the response as seen above.
        return InvoiceCreationMutation(invoice=invoice)


class InvoiceDeletionMutation(graphene.Mutation):

    class Arguments:
        invoice_id = graphene.ID(required=True)

    # This exposes a boolean to know the status of the deletion.
    deleted = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, root, info, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise Exception('Invalid invoice Id')
        invoice.delete()
        return InvoiceDeletionMutation(deleted=True)


class Mutation(graphene.ObjectType):
    create_invoice = InvoiceCreationMutation.Field()
    delete_invoice = InvoiceDeletionMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)